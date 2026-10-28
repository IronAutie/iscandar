#!/usr/bin/env python3
"""test_graphs.py: regenerate the monograph's two measured graphs from
the published Gaussian Two records, and verify them.

The figures in the paper (Figure E, label fig:performance_final_archive,
and the superimposed plot, label fig:superimposed_plot) were built from
the per-allocation records of the Gaussian Two run. This test rebuilds
both figure blocks from those records alone, coordinate by coordinate,
asserts the headline facts from the data (successful allocation counts,
stall rows, stall occupancies), and, when given the paper's source,
diffs the regenerated blocks against the shipped ones line by line.
It also writes the regenerated figures, wrapped in markdown, to a text
file ready to drop into the paper source.

Usage:
  python test_graphs.py [--records DIR] [--reference MAIN.tex]
                        [--out graphs.md]

Defaults: records in results/gaussian-two beside this file; no
reference (facts and regeneration only); output graphs.md beside
this file.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
POOL = 32768


def load_records(folder: Path, name: str) -> list[dict]:
    with open(folder / f"records_{name}.csv", newline="") as f:
        return list(csv.DictReader(f))


def successful(rows: list[dict]) -> list[dict]:
    return [r for r in rows if r["type"] == "alloc" and r["success"] == "ok"]


def stall_row(rows: list[dict]) -> dict:
    for r in rows:
        if r["success"] == "stall":
            return r
    raise SystemExit("FAIL: no stall row in the records")


def one_decimal(text: str) -> float:
    return round(float(text) + 1e-9, 1)


def coords_lines(points: list[tuple], indent: str = "            ") -> str:
    lines = []
    for i in range(0, len(points), 5):
        chunk = points[i:i + 5]
        lines.append(indent + " ".join(f"({x},{y})" for x, y in chunk))
    return "\n".join(lines)


FIGURE_E = r"""\begin{figure}[ht]
\centering
\begin{tikzpicture}
\begin{axis}[
    title={Figure E: Iscandar Performance Profile (Gaussian Two, Measured)},
    xlabel={Heap Occupancy [Sectors]},
    ylabel={Touches per Allocation},
    xmin=0, xmax=32768,
    ymin=0, ymax=70,
    xtick={0, 8192, 16384, 24576, 32768},
    ytick={0, 10, 20, 30, 40, 50, 60, 70},
    scaled x ticks=false,
    x tick label style={/pgf/number format/fixed, /pgf/number format/1000 sep={,}},
    grid=major,
    legend pos=north west,
    width=11cm,
    height=7cm,
]
\addplot[only marks, blue, mark=*, mark size=1.2pt, opacity=0.7] coordinates {
@@COORDS_E@@
};
\addlegendentry{Iscandar touches (measured)}
\node[anchor=north west, font=\footnotesize] at (axis cs: 1000, 68) {stall at op @@STALL_OP@@: @@ISC_PCT@@\% physical = @@ISC_PCT@@\% logical};
\end{axis}
\end{tikzpicture}
\caption{Measured touches per allocation against physical occupancy for the Gaussian Two profile (seed 1; requests of 1 to 1{,}023 sectors). The run ends where the allocator stalls, at @@ISC_PCT@@\% physical occupancy, which for Iscandar is also its logical occupancy: the fit is exact.}
\label{fig:performance_final_archive}
\end{figure}"""

SUPERIMPOSED = r"""\begin{figure}[H]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            title={Touches vs. Logical Occupancy: Iscandar and Buddy (Gaussian Two)},
            xlabel={Logical Occupancy [\%]},
            ylabel={Touches per Allocation},
            xmin=0, xmax=100,
            ymin=0, ymax=70,
            xtick={0, 20, 40, 60, 80, 100},
            ytick={0, 10, 20, 30, 40, 50, 60, 70},
            grid=major,
            legend pos=north west,
            width=11cm,
            height=7cm,
        ]
        \addplot[only marks, blue, mark=*, mark size=1.2pt, opacity=0.7] coordinates {
@@COORDS_S_ISC@@
        };
        \addlegendentry{Iscandar touches (measured)}
        \addplot[only marks, red, mark=square*, mark size=1.5pt, opacity=0.6] coordinates {
@@COORDS_S_BUDDY@@
        };
        \addlegendentry{Buddy touches (measured)}
        \draw[red, dashed, thin] (axis cs: @@BUD_PCT@@, 0) -- (axis cs: @@BUD_PCT@@, 15);
        \draw[blue, dashed, thin] (axis cs: @@ISC_PCT@@, 0) -- (axis cs: @@ISC_PCT@@, 65);
        \node[anchor=north east, font=\footnotesize] at (axis cs: 62, 17) {Buddy stalls at @@BUD_PCT@@\% logical};
        \node[anchor=north east, font=\footnotesize] at (axis cs: 99, 68) {Iscandar stalls at @@ISC_PCT@@\%};
        \end{axis}
    \end{tikzpicture}
    \caption{Both allocators on the identical Gaussian Two request stream, touches per allocation against logical occupancy: the share of the pool carrying useful work. Buddy is cheaper per operation, and its trace ends at @@BUD_PCT@@\% logical (@@BUD_PHYS@@\% physical, the difference burned as rounding). Iscandar pays more touches per allocation and carries the stream to @@ISC_PCT@@\%.}
    \label{fig:superimposed_plot}
\end{figure}"""


def build_blocks(isc_rows, bud_rows) -> tuple[str, str, dict]:
    isc_ok = successful(isc_rows)
    bud_ok = successful(bud_rows)
    isc_stall = stall_row(isc_rows)
    bud_stall = stall_row(bud_rows)

    facts = {
        "isc_ok": len(isc_ok),
        "bud_ok": len(bud_ok),
        "isc_stall_op": int(isc_stall["op"]) + 1,
        "isc_pct": one_decimal(isc_stall["logical_pct"]),
        "isc_phys": one_decimal(isc_stall["physical_pct"]),
        "bud_pct": one_decimal(bud_stall["logical_pct"]),
        "bud_phys": one_decimal(bud_stall["physical_pct"]),
    }

    fig_e_points = [
        (int(round(float(r["physical_pct"]) / 100.0 * POOL)),
         int(r["accesses"]))
        for r in isc_ok
    ]
    sup_isc = [(one_decimal(r["logical_pct"]), int(r["accesses"]))
               for r in isc_ok]
    sup_bud = [(one_decimal(r["logical_pct"]), int(r["accesses"]))
               for r in bud_ok]

    def fmt(pairs):
        return [(f"{x:.1f}" if isinstance(x, float) else str(x), y)
                for x, y in pairs]

    subs = {
        "@@STALL_OP@@": str(facts["isc_stall_op"]),
        "@@ISC_PCT@@": f"{facts['isc_pct']:.1f}",
        "@@BUD_PCT@@": f"{facts['bud_pct']:.1f}",
        "@@BUD_PHYS@@": f"{facts['bud_phys']:.1f}",
    }
    fig_e = FIGURE_E.replace("@@COORDS_E@@", coords_lines(fig_e_points))
    sup = SUPERIMPOSED.replace(
        "@@COORDS_S_ISC@@", coords_lines(fmt(sup_isc))).replace(
        "@@COORDS_S_BUDDY@@", coords_lines(fmt(sup_bud)))
    for key, value in subs.items():
        fig_e = fig_e.replace(key, value)
        sup = sup.replace(key, value)
    return fig_e, sup, facts


def extract_block(tex: str, label: str) -> str | None:
    i = tex.find(label)
    if i < 0:
        return None
    start = tex.rfind("\\begin{figure}", 0, i)
    end = tex.find("\\end{figure}", i) + len("\\end{figure}")
    return tex[start:end]


def normalized(block: str) -> list[str]:
    return [line.rstrip() for line in block.strip().splitlines()]


def diff_blocks(name: str, generated: str, reference: str) -> bool:
    gen, ref = normalized(generated), normalized(reference)
    if gen == ref:
        print(f"  PASS  {name}: regenerated block matches the shipped "
              f"figure exactly ({len(gen)} lines)")
        return True
    print(f"  FAIL  {name}: {len(gen)} generated lines vs "
          f"{len(ref)} shipped lines")
    for n, (a, b) in enumerate(zip(gen, ref)):
        if a != b:
            print(f"    first difference at line {n + 1}:")
            print(f"      generated: {a}")
            print(f"      shipped:   {b}")
            break
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", type=Path,
                    default=HERE / "results" / "gaussian-two")
    ap.add_argument("--reference", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=HERE / "graphs.md")
    args = ap.parse_args()

    isc_rows = load_records(args.records, "iscandar")
    bud_rows = load_records(args.records, "buddy")
    fig_e, sup, facts = build_blocks(isc_rows, bud_rows)

    print("Graph regeneration test: Gaussian Two records to paper figures")
    print("Facts asserted from the records themselves:")
    ok = True
    checks = [
        ("Iscandar successful allocations", facts["isc_ok"], 66),
        ("Buddy successful allocations", facts["bud_ok"], 38),
        ("Iscandar stall operation (1-based)", facts["isc_stall_op"], 74),
        ("Iscandar stall logical %", facts["isc_pct"], 96.5),
        ("Iscandar stall physical %", facts["isc_phys"], 96.5),
        ("Buddy stall logical %", facts["bud_pct"], 62.2),
        ("Buddy stall physical %", facts["bud_phys"], 99.2),
    ]
    for name, got, want in checks:
        good = got == want
        ok = ok and good
        print(f"  {'PASS' if good else 'FAIL'}  {name}: {got}")

    if args.reference:
        tex = args.reference.read_text()
        print("Diff against the shipped paper source:")
        for label, block in (("fig:performance_final_archive", fig_e),
                             ("fig:superimposed_plot", sup)):
            ref = extract_block(tex, label)
            if ref is None:
                print(f"  FAIL  {label}: not found in the reference")
                ok = False
            else:
                ok = diff_blocks(label, block, ref) and ok

    md = "\n".join([
        "# Gaussian Two graphs, regenerated from the published records",
        "",
        "Generated by test_graphs.py from results/gaussian-two/"
        "records_iscandar.csv and records_buddy.csv (the Gaussian Two "
        "run, seed 1). Every coordinate below is computed from those "
        "records; nothing is hand-plotted. Facts asserted by the test: "
        f"Iscandar {facts['isc_ok']} successful allocations, stalling "
        f"at operation {facts['isc_stall_op']} at {facts['isc_pct']:.1f}% "
        f"logical = {facts['isc_phys']:.1f}% physical; Buddy "
        f"{facts['bud_ok']} successful allocations, stalling at "
        f"{facts['bud_pct']:.1f}% logical ({facts['bud_phys']:.1f}% "
        "physical).",
        "",
        "## Figure E (fig:performance_final_archive)",
        "",
        "```latex",
        fig_e,
        "```",
        "",
        "## Superimposed plot (fig:superimposed_plot)",
        "",
        "```latex",
        sup,
        "```",
        "",
    ])
    args.out.write_text(md)
    print(f"Markdown written to {args.out}")
    print("GRAPH TEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
