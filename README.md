# iscandar

*A Drop-in Memory Allocator with Bounded Variance via Fractal Virtual Coordinate Mapping*

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
│   └── Iscandar_24b.pdf    # Monograph specification document
├── code/oracles/           # Oracle table manufacture (create_oracles.py)
├── oracle/creators/src/    # Oracle creators, independent of engine code
└── notes/                  # Design doctrine, JOSS framing, and architecture notes
```

- `paper/` — the paper. `Iscandar_24b.pdf` is the latest copy the author has access to (50 pages, rendered 2026-06-01). The paper stands as-is.
  - Version history of the paper: https://github.com/IronAutie/iscandar-history
  - The paper's listings as a standalone repo: https://github.com/IronAutie/iscandar-listings
- `code/oracles/` — `create_oracles.py`, the Python procedure that manufactures the oracle tables as bitwise files, from the math as specified in Appendix D of the paper. (The paper's APL oracle access files are being replaced with Python equivalents; the `.bin` layouts are unchanged.)
- `oracle/creators/src/` — the oracle creators' home, independent of the engine code: the paper's three generator listings plus the production creator, with a README saying which is which.
- `notes/` — design and manufacture notes, including the oracle manufacture desk-check brief and the draft literature/independence notes.

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

Assistance disclosure, in the author's framing: Gemini assisted with literature search, grammar, and organizing; the argument and the assembly are the author's.

---

## Original hand drawings

The original hand drawings are in the [FractalClosedMemory wiki](https://github.com/IronAutie/FractalClosedMemory/wiki/DRAWINGS) — Table of Drawings, Chapters 1–3. They are the author's link to the 16-bit oracles for the Intel 80188 and Motorola 68332.

---

## Status

The Python engine — Iscandar implemented beside a simulated buddy allocator, identical traces through both, comparing Iscandar's flat k×A per-operation cost against the buddy system's degradation with occupancy and fragmentation — is the author's current work, in progress.

As of the JOSS prep in October 2026, Nano, Tiny, Small, Cube, Error, and Nothing search modes are implemented; Large and Huge remain to be specified.

---

## Dedication

To Jennifer: Everything. Always. Forever.

## License

Software in this repository is licensed under the MIT License, see `LICENSE`.

The paper and documentation in this repository are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
