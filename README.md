# iscandar

*A Drop-in Memory Allocator with Bounded Variance via Fractal Virtual Coordinate Mapping*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23748412.svg)](https://doi.org/10.5281/zenodo.23748412)

---

## Overview

**iscandar** is a deterministic memory allocation architecture designed for deterministic real-time systems, embedded environments, and high-assurance compute tasks. Built upon a fixed-depth ($k=3$), high-radix ($A=32$) fractal coordinate map, **iscandar** replaces traditional stochastic heap searching with geometric coordinate resolution.

It is an extension of buddy systems to arbitrary radix (radix 32, depth 3 in the reference configuration), by Andrew Jonathan Fine.

The repository includes structured Visual Studio Code workspace tasks (`.vscode/tasks.json`) for building the C drivers.

---

## Architecture & Design Highlights

* **3D Fractal Coordinate Space ($k=3, A=32$):** Maps a 32,768-sector linear memory arena into a 32×32×32 fractal lattice ($Cube \to Plane \to Row \to Sector$).
* **Deterministic Resolution ($O(1)$ Bounds):** Replaces variable-length pointer searches with bitwise coordinate resolution and direct Table Look-Up (TLU) sweeps, avoiding traditional bit-scanning.
* **Dual C / Python Stack:** Core drivers and allocation loops are written in pure ISO C for performance, coupled with high-level Python models for spatial verification, testing, and structural orchestration.
* **Runtime Inspectability:** Exposes explicit runtime state and diagnostic status codes via `status.h` for outer-loop orchestration and hardware test rigs.

The radix design is the contribution, and it is itself O(1). The oracles are not the innovation: an oracle is an anticipation of the buddy system's own action — an existing O(1) engine dropped in so that placement does not degrade the radix design. Oracles replace search: where a conventional allocator examines candidates, Iscandar consults a table keyed by the counter state that returns the placement directly. The counters keep the books, so an imperfect oracle costs placements, never consistency.

---

## Repository Structure

```text
iscandar/
├── allocator.py            # Main Python allocation engine & spatial coordinator
├── Bijection.py            # Coordinate transformation bijections
├── Coordinate.py           # Virtual 3D coordinate vector definitions
├── Geometry.py             # Geometric layout and boundary rules
├── Modes.py / Mode.py      # Execution mode controls
├── Nano.py / Tiny.py / Small.py / Large.py / Huge.py / Cube.py / Error.py / Nothing.py
│                           # Size-tier search modes
├── Status.py               # Python wrapper for status codes
├── status.h                # C header defining runtime status codes & flags
│
├── Commit.c / Commit.h     # Sector commitment and state transition kernels
├── Mark.c                  # Sector marking and allocation logic
├── Unmark.c                # Deallocation and coalescence logic
├── MPUPointer.py           # Hardware memory protection unit abstractions
│
├── PlaneSmallDriver.c      # Plane-level allocation driver
├── PairsRowDriver.c        # Row-level pair driver
├── PlanesCheck.c           # C validation suite for plane logic
├── RowsCheck.c             # C validation suite for row logic
├── CubeCheck.py            # Python verification script for Cube boundaries
├── GammaCheck.py           # Occupancy counter (Γ) integrity checker
│
├── build.bat               # Windows build script for C components
├── build_gears.bat         # Secondary build script for extended driver modules
├── gen_status.py           # Code generator for status headers
├── paper.md / paper.bib    # JOSS paper draft and bibliography
│
├── paper/                  # Manuscript source and build artifacts
│   └── Iscandar-45-final.pdf    # Finished monograph (current rendering; the Iscandar-44 rendering is kept beside it)
├── code/oracles/           # Oracle table manufacture (create_oracles.py)
├── oracle/creators/src/    # Oracle creators, independent of engine code
└── notes/                  # Design doctrine, JOSS framing, and architecture notes
```

- `paper/` — the paper. `Iscandar-45-final.pdf` is the finished monograph (20 pages, final rendering 2026-10-28): the measured figures regenerated from the published run records, and the acknowledgements. The same PDF also sits at the repository root. It supersedes the `Iscandar-44-final.pdf` rendering (19 pages, 2026-10-27), which is kept beside it, and the earlier `Iscandar_24b.pdf` draft that lived here.
  - Version history of the paper: https://github.com/IronAutie/iscandar-history
  - The paper's listings as a standalone repo: https://github.com/IronAutie/iscandar-listings
- `code/oracles/` — `create_oracles.py`, the Python procedure that manufactures the oracle tables as bitwise files, from the math as specified in Appendix D of the paper. (The paper's APL oracle access files are being replaced with Python equivalents; the `.bin` layouts are unchanged.)
- `oracle/creators/src/` — the oracle creators' home, independent of the engine code: the paper's three generator listings plus the production creator, with a README saying which is which.
- `notes/` — design and manufacture notes, including the oracle manufacture desk-check brief and the draft literature/independence notes.

---

## Building and verifying (Windows)

The C gears build into a single DLL, RowsCheck.dll, loaded by Gears.py through ctypes.

Prerequisites:

- A C compiler. The bench uses Visual C++ 10 (the compiler in Visual Studio 2010), with VS Code as the editor, for embedded development; the gears are plain C90-era C, and any compiler should work. Build with the x64 toolset if your Python is 64-bit, x86 if it is 32-bit: the DLL and the Python must match.
- Python 3.13. The only third-party package is bitstruct (`python -m pip install bitstruct`); the counters use the standard library's array module.

Build and run the acceptance suite, from the engine folder:

```
vcvarsall.bat amd64
build_gears.bat
python test_engine.py
```

build_gears.bat first regenerates status.h from Status.py, then compiles all eleven C files into RowsCheck.dll. The acceptance suite runs 22 tests.

Two further verifications:

- `python oracle_smoke_test.py` runs the allocator end to end with the manufactured oracle tables driving the Nano and Tiny bullets (the tables default to O:\oracle on Windows). It checks the desk-check anchors, diffs the table bullets against the shipped bullets probe by probe, and runs a 500-request stream checked for determinism, placement overlaps, and counter reconciliation.
- `python test_graphs.py` regenerates the monograph's two measured figures from the published records in results/gaussian-two and writes them, wrapped in markdown, to graphs.md, asserting the headline facts from the records themselves.

A note on where the tables live: compiling is not the whole setup. The three oracle tables total about 52 GiB and are not committed, and the smoke test needs them in place. The practical arrangement is an external SSD on a USB port (a PNY CS900 serves well) with the drive letter O: assigned to it, and an oracle folder at its root. The creators, the timing scripts, and the smoke test all default to O:\oracle on Windows.

One build note: every entry point the DLL exposes must carry `__declspec(dllexport)` in its definition. Without it, `cl /LD` keeps the function private and Gears.py fails at import. (Mark.c and Unmark.c once lost their markers; the smoke test is what caught it.)

Provenance of this verification: the engine, the oracle manufacture, and the run records were developed off site. The finished artifacts were then imported to an ordinary Windows 11 laptop (a Lenovo IdeaPad) and built and tested there under real-world conditions, as the appendix at the end of this README records, step by step. The results in this repository are the ones that survived that import unchanged.

---

## The oracle files

The tables are generated data and are **not committed** (52 GiB total).
Regenerate them with the kept creator:

```
python3 code/oracles/create_oracles.py all --outdir data/oracles
python3 code/oracles/create_oracles.py selftest --outdir data/oracles
```

- `OracleCenter.bin` — 2^32 rows × 9 bytes = 38,654,705,664 bytes
- `OracleLeft.bin` — 2^32 rows × 2 bytes = 8,589,934,592 bytes
- `OracleRight.bin` — 2^32 rows × 2 bytes = 8,589,934,592 bytes

Slow to create, once, in advance; afterwards every lookup is a single memory-mapped read. The first full set was generated and verified on 2026-10-22: fresh-process `mmap` readback of all three files against literal transcriptions of the paper's listing formulas, on edge-case and random states — all checks passed.

---

## Provenance

The design was developed in 1998 as proprietary industry work, without access to the published literature, and was reconstructed from the author's memory in 2026, after the copyright in the original work had lapsed; parts of it therefore duplicate published results independently (see the independence note in `notes/` and in the history repo's README).

Assistance disclosure, in the author's framing: Gemini assisted with literature search, grammar, and organizing; the argument and the assembly are the author's. Muse assisted under the author's direction with source code checking, test file generation, and result generation (the oracle manufacture and timing runs, and the record-generated figures of the monograph, among them). The core design, equations, and mathematics remain the author's, and he reviewed, edited, and validated the resulting work.

---

## Original hand drawings

The original hand drawings are in the [FractalClosedMemory wiki](https://github.com/IronAutie/FractalClosedMemory/wiki/DRAWINGS) — Table of Drawings, Chapters 1–3. They are the author's link to the 16-bit oracles for the Intel 80188 and Motorola 68332.

---

## Status

The Python engine is complete: all search modes — Nothing, Nano, Tiny, Small, Large, Huge, Cube, and Error — are implemented and covered by the acceptance test suite in `test_engine.py`. Large and Huge each carry a second pass for split-edge spans, so a placement is found whenever a contiguous free run of the request exists.

Measured comparisons against a classic binary buddy allocator on identical seeded traces — occupancy, rounding waste, cost stability, and survival under six RTOS-shaped load profiles — are in `results/`, with the per-operation records beside the reports. A Windows (Visual Studio 2010) build-and-test verification of the C drivers at the author's bench remains the last step before a versioned release.

---

## Dedication

To Jennifer: Everything. Always. Forever.

## License

Software in this repository is licensed under the MIT License, see `LICENSE`.

The paper and documentation in this repository are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).

---

## Iscandar project setup: commands run on the CIC laptop
Session of Wed 2026-10-28, in the order given, beginning from the project pull.
Working folder throughout: C:\Users\IronAutie\iscandar\engine
Kept at the author's request; new commands this session get appended as they are given.

### 1. Project pull

```
git pull
git log --oneline -3
```

Fast-forward bde2ffc..9c4bedc (103 files). HEAD confirmed as:
9c4bedc (HEAD -> main, origin/main, origin/HEAD), then 289c484, then f87e906.

### 2. First build (x86) and the bitstruct gap

```
vcvarsall.bat x86
build_gears.bat
python test_engine.py
```

Build clean: gen_status.py regenerated status.h (22 codes), all eleven
C files compiled, RowsCheck.dll linked. The test run stopped at import:
ModuleNotFoundError: No module named 'bitstruct' (an environment gap,
not a code failure). Remedy:

```
python -m pip install bitstruct
```

bitstruct 8.24.0; its wheel (cp313-win_amd64) proved the laptop Python
is 64-bit, so the DLL must be built for x64.

### 3. Rebuild for x64 and the acceptance run

```
vcvarsall.bat amd64
build_gears.bat
python test_engine.py
```

Result: Ran 22 tests in 12.539s, OK.
(Note, established later the same day: the acceptance suite never
imports Gears, so it does not itself exercise the DLL. The first true
end-to-end DLL run was the oracle smoke test, step 5.)

### 4. Oracle tables verified against O:\oracle

```
python oracle\timing\time_oracle_left.py
python oracle\timing\time_oracle_right.py
python oracle\timing\time_oracle_center.py
```

Seed 20261022, 20000 samples per pass. Warm null-corrected:
Left 0.4 us/lookup (2,627,948/s), Right 0.4 (2,667,912/s),
Center 0.4 (2,510,513/s). Repeat-pass checksums identical to
first-pass checksums for all three tables.

### 5. Oracle smoke test (allocator driven by the manufactured tables)

oracle_smoke_test.py saved into the engine folder, then:

```
python oracle_smoke_test.py
```

First run: anchors and bullet differentials passed; the engine leg
failed at Gears.py line 128, AttributeError: function 'mark_sectors'
not found. Cause: Mark.c and Unmark.c defined mark_sectors and
unmark_sectors without __declspec(dllexport), so cl /LD never exported
them (gcc exports everything by default, which is why the VM build
masked it). Fix, one word in each file:

Mark.c, find:
```
int32_t mark_sectors(uint32_t *sectors, uint32_t *count_rows,
```
paste:
```
__declspec(dllexport) int32_t mark_sectors(uint32_t *sectors, uint32_t *count_rows,
```

Unmark.c, find:
```
int32_t unmark_sectors(uint32_t *sectors, uint32_t *count_rows,
```
paste:
```
__declspec(dllexport) int32_t unmark_sectors(uint32_t *sectors, uint32_t *count_rows,
```

Then, in the amd64 window:

```
build_gears.bat
python oracle_smoke_test.py
```

Result: ORACLE SMOKE TEST: PASS. Anchors 4/4; Nano table vs shipped
bullet 33,312/33,312 probes; Tiny 99,380 agree, 556 differ (interior
runs only); 500-request stream deterministic across two processes,
zero overlaps, counters reconcile at 8,279. Every figure identical
to the VM validation run.

### 6. Graph regeneration test (figures from the published records)

test_graphs.py saved into the engine folder, then:

```
python test_graphs.py
notepad graphs.md
```

Result: GRAPH TEST: PASS. Seven facts asserted from the records
themselves; graphs.md written in the engine folder holding both
monograph figures as LaTeX blocks in markdown fences. Figure E is
identical to the shipped Iscandar 44 figure. The superimposed plot
carries the records-true traces (the shipped Buddy trace had been
smoothed in x by a plotting error; the shipped Iscandar points at
75.0 and 92.3 read 74.9 and 92.4 from the records). The author is
pasting these replacements into the paper.

### Streamlined order for a fresh machine

```
git pull
python -m pip install bitstruct
vcvarsall.bat amd64
build_gears.bat
python test_engine.py
python oracle_smoke_test.py
python test_graphs.py
```
