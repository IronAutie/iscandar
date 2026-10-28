#!/usr/bin/env python3
"""oracle_smoke_test.py: run the allocator with the manufactured oracle
tables of Appendix D driving the Nano and Tiny bullets directly.

The shipped Nano and Tiny bullets compute their oracle answers inline.
This test substitutes bullets that read the manufactured tables
(OracleCenter.bin, OracleLeft.bin, OracleRight.bin) through mmap, and
checks four things:

  1. Anchors: the three desk-check words from the monograph read back
     from the tables exactly as recorded.
  2. Nano differential: the table bullet and the shipped bullet agree
     on every probed row (status and sector), over random row states.
  3. Tiny differential: the table bullet (dual-pass, edge runs) and
     the shipped bullet (first eligible run, then the tail) are
     compared; agreements and disagreements are counted and reported.
  4. Engine run: the real Engine, with the table bullets chambered,
     allocates a seeded stream of Nano and Tiny requests through the
     real gears. Every placement is checked against a shadow map for
     overlap, the counters must reconcile at the end, and the whole
     stream is run twice in separate processes: the outcomes must be
     identical (determinism).

Usage:
  python oracle_smoke_test.py [--oracles DIR]

The tables default to O:\\oracle on Windows and to
~/workspace/iscandar/oracles elsewhere. Nothing in the engine is
modified; the substitution happens inside this test process only.
"""

from __future__ import annotations

import argparse
import mmap
import os
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from Geometry import Geometry          # noqa: E402
from Mode import Mode                  # noqa: E402
from Nano import Nano                  # noqa: E402
from Tiny import Tiny                  # noqa: E402
from Status import Status              # noqa: E402

FAIL_BYTE = 255
CENTER_BYTES = (1 << 32) * 9
EDGE_BYTES = (1 << 32) * 2


def default_oracle_dir() -> Path:
    if os.name == "nt":
        return Path(r"O:\oracle")
    return Path.home() / "workspace" / "iscandar" / "oracles"


class OracleTables:
    """The three manufactured tables, memory-mapped and size-checked."""

    def __init__(self, folder: Path):
        self.center = self._open(folder / "OracleCenter.bin", CENTER_BYTES)
        self.left = self._open(folder / "OracleLeft.bin", EDGE_BYTES)
        self.right = self._open(folder / "OracleRight.bin", EDGE_BYTES)

    @staticmethod
    def _open(path: Path, expected: int) -> mmap.mmap:
        size = path.stat().st_size
        if size != expected:
            raise SystemExit(
                f"FAIL: {path} has {size} bytes, expected {expected}")
        f = open(path, "rb")
        return mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    def center_at(self, s: int, length: int) -> int:
        """Leftmost start position (Motorola, 0 = MSB) of a clear run
        of `length` bits in row state s, or 255. Column 0 is unused;
        columns 1..8 hold lengths 1..8."""
        return self.center[s * 9 + length]

    def left_at(self, s: int) -> tuple[int, int]:
        """(trailing run length from the low end, 32 - length);
        (255, 0) when the low bit is occupied."""
        off = s * 2
        return self.left[off], self.left[off + 1]

    def right_at(self, s: int) -> tuple[int, int]:
        """(leading run length from the high end, 0);
        (255, 0) when the high bit is occupied."""
        off = s * 2
        return self.right[off], self.right[off + 1]


TABLES: OracleTables | None = None


class NanoTable(Nano):
    """Nano bullet whose probe is a Center Oracle table lookup."""

    def __call__(self, plane, row, request, ctx, sector_out):
        global_row = plane * Geometry.ARITY + row
        if not 0 <= global_row <= 1023:
            return Status.NANO_FAIL
        if request not in self.range():
            return Status.NANO_FAIL
        pos = TABLES.center_at(ctx[global_row], request)
        if pos == FAIL_BYTE:
            return Status.NANO_FAIL
        sector_out[0] = 32 - request - pos
        return Status.GEAR_SUCCESS


class TinyTable(Tiny):
    """Tiny bullet whose probes are Left and Right Oracle lookups:
    the low edge run first (eligible at 9 or more, as in the shipped
    bullet), then the tail run at the high edge as the second bite."""

    def __call__(self, plane, row, request, ctx, sector_out):
        global_row = plane * Geometry.ARITY + row
        if not 0 <= global_row <= 1023:
            return Status.TINY_FAIL
        if request not in self.range():
            return Status.TINY_FAIL
        s = ctx[global_row]
        low_len, _ = TABLES.left_at(s)
        if low_len != FAIL_BYTE and low_len >= 9:
            if low_len >= request:
                sector_out[0] = 0
                return Status.GEAR_SUCCESS
            # Eligible but short: second bite.
        tail_len, _ = TABLES.right_at(s)
        if tail_len != FAIL_BYTE and tail_len >= request:
            sector_out[0] = 32 - request
            return Status.GEAR_SUCCESS
        return Status.TINY_FAIL


def check_anchors() -> bool:
    ok = True
    cases = [
        ("Center 0xF1FE7FFF L=5 acquits (255)",
         TABLES.center_at(0xF1FE7FFF, 5), 255),
        ("Center 0xCFC1F1FC L=5 convicts at 10",
         TABLES.center_at(0xCFC1F1FC, 5), 10),
        ("Left   0xE007F800 is (11, 21)",
         TABLES.left_at(0xE007F800), (11, 21)),
        ("Right  0xE007F800 is blocked (255, 0)",
         TABLES.right_at(0xE007F800), (255, 0)),
    ]
    for name, got, want in cases:
        good = got == want
        ok = ok and good
        print(f"  {'PASS' if good else 'FAIL'}  {name}: got {got}")
    return ok


def bullet_differential() -> tuple[bool, bool]:
    rng = random.Random(20261028)
    words = [rng.getrandbits(32) for _ in range(4000)]
    # Structured states: empty, full, alternating, single runs.
    words += [0, 0xFFFFFFFF, 0xAAAAAAAA, 0x55555555]
    for start in range(32):
        for length in (1, 5, 9, 17, 32):
            w = 0
            for i in range(start, min(32, start + length)):
                w |= 1 << i
            words.append(w)
    ctx = [0] * 1024
    cell = [None]

    nano_bad = 0
    nano_total = 0
    shipped_nano, table_nano = Nano(), NanoTable()
    for w in words:
        ctx[0] = w
        for length in range(1, 9):
            nano_total += 1
            cell[0] = None
            a = shipped_nano(0, 0, length, ctx, cell)
            va = cell[0]
            cell[0] = None
            b = table_nano(0, 0, length, ctx, cell)
            vb = cell[0]
            if a != b or (a == Status.GEAR_SUCCESS and va != vb):
                nano_bad += 1
                if nano_bad <= 3:
                    print(f"  Nano mismatch: word {w:#010x} L={length} "
                          f"shipped ({a}, {va}) table ({b}, {vb})")
    print(f"  Nano: {nano_total - nano_bad}/{nano_total} probes agree")
    nano_ok = nano_bad == 0

    tiny_same = 0
    tiny_diff = 0
    examples = []
    shipped_tiny, table_tiny = Tiny(), TinyTable()
    for w in words:
        ctx[0] = w
        for length in range(9, 33):
            cell[0] = None
            a = shipped_tiny(0, 0, length, ctx, cell)
            va = cell[0]
            cell[0] = None
            b = table_tiny(0, 0, length, ctx, cell)
            vb = cell[0]
            if a == b and (a != Status.GEAR_SUCCESS or va == vb):
                tiny_same += 1
            else:
                tiny_diff += 1
                if len(examples) < 3:
                    examples.append((w, length, a, va, b, vb))
    print(f"  Tiny: {tiny_same} probes agree, {tiny_diff} differ "
          f"(the shipped bullet also scans interior runs; "
          f"the table bullet sees the two edge runs only)")
    for w, length, a, va, b, vb in examples:
        print(f"    example: word {w:#010x} L={length} "
              f"shipped ({a}, {va}) table ({b}, {vb})")
    return nano_ok, True


def engine_stream(mode: str, out_path: Path) -> None:
    """One engine run in its own process (the gears carry static
    rotation state, so separate processes keep runs comparable)."""
    from allocator import Engine
    from MPUPointer import MPUPointer

    engine = Engine()
    if mode == "table":
        nano_t, tiny_t = NanoTable(), TinyTable()
        for length in nano_t.range():
            engine.modes[length] = nano_t
        for length in tiny_t.range():
            engine.modes[length] = tiny_t
        engine.modes.nano = nano_t
        engine.modes.tiny = tiny_t

    rng = random.Random(20261028)
    requests = [rng.randint(1, 32) for _ in range(500)]
    shadow = bytearray(Cube_sectors())
    lines = []
    placed_sectors = 0
    overlaps = 0
    for request in requests:
        result = engine(request)
        if isinstance(result, MPUPointer):
            start, count = result.start, result.count
            lines.append(f"P {start} {count}")
            for i in range(start, start + count):
                if shadow[i]:
                    overlaps += 1
                shadow[i] = 1
            placed_sectors += count
        else:
            lines.append(f"F {result}")
    lines.append(f"overall {engine.count_overall} "
                 f"placed {placed_sectors} overlaps {overlaps}")
    out_path.write_text("\n".join(lines) + "\n")


def Cube_sectors() -> int:
    from Cube import Cube
    return Cube.SECTORS_PER_CUBE


def check_engine(folder: Path) -> bool:
    runs = {}
    for name in ("table_a", "table_b", "stock"):
        out = folder / f"oracle_smoke_{name}.txt"
        mode = "stock" if name == "stock" else "table"
        proc = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()),
             "--engine-run", mode, "--out", str(out)],
            capture_output=True, text=True)
        if proc.returncode != 0:
            print(proc.stdout)
            print(proc.stderr)
            print(f"  FAIL  engine run {name} exited {proc.returncode}")
            return False
        runs[name] = out.read_text()

    ok = True
    deterministic = runs["table_a"] == runs["table_b"]
    print(f"  {'PASS' if deterministic else 'FAIL'}  "
          f"table-driven stream is deterministic across two processes")
    ok = ok and deterministic

    tail = runs["table_a"].strip().splitlines()[-1]
    overall = int(tail.split()[1])
    placed = int(tail.split()[3])
    overlaps = int(tail.split()[5])
    valid = overlaps == 0 and overall == placed
    print(f"  {'PASS' if valid else 'FAIL'}  "
          f"no placement overlaps; counters reconcile "
          f"(overall {overall} == placed {placed}, overlaps {overlaps})")
    ok = ok and valid

    stock_lines = runs["stock"].splitlines()
    table_lines = runs["table_a"].splitlines()
    same = sum(1 for a, b in zip(stock_lines, table_lines) if a == b)
    print(f"  info  stock and table streams agree on "
          f"{same}/{len(table_lines)} lines "
          f"(Tiny edge cases may place differently, by design)")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--oracles", type=Path, default=None)
    ap.add_argument("--engine-run", choices=("stock", "table"),
                    default=None)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    global TABLES
    TABLES = OracleTables(args.oracles or default_oracle_dir())

    if args.engine_run:
        engine_stream(args.engine_run, args.out)
        return 0

    print("Oracle smoke test: allocator driven by the manufactured tables")
    print("Anchors (desk-check words against the tables):")
    ok = check_anchors()
    print("Bullet differentials (table bullets vs shipped bullets):")
    nano_ok, _ = bullet_differential()
    ok = ok and nano_ok
    print("Engine stream (table bullets chambered, real gears):")
    ok = check_engine(Path(__file__).resolve().parent) and ok
    print("ORACLE SMOKE TEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
