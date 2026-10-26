# iscandar

*A Drop-in Memory Allocator with Bounded Variance via Fractal Virtual Coordinate Mapping*

---

## Overview

**iscandar** is an open-source, high-reliability memory allocation architecture designed for deterministic real-time systems, embedded environments, and high-assurance compute tasks. Built upon a fixed-depth ($k=3$), high-radix ($A=32$) fractal coordinate map, **iscandar** replaces traditional stochastic heap searching with geometric coordinate resolution.

Designed natively as a **Visual Studio Code project**, **iscandar** integrates structured workspace tasks (`.vscode/tasks.json`) to streamline building, testing, and running your development workflow.

---

## Architecture & Design Highlights

* **3D Fractal Coordinate Space ($k=3, A=32$):** Maps a 32,768-sector linear memory arena into a 32×32×32 fractal lattice ($Cube \to Plane \to Row \to Sector$).
* **Deterministic Resolution ($O(1)$ Bounds):** Replaces variable-length pointer searches with bitwise coordinate resolution and direct Table Look-Up (TLU) sweeps, avoiding traditional bit-scanning.
* **Dual C / Python Stack:** Core drivers and allocation loops are written in pure ISO C for performance, coupled with high-level Python models for spatial verification, testing, and structural orchestration.
* **Runtime Inspectability:** Exposes explicit runtime state and diagnostic status codes via `status.h` for outer-loop orchestration and hardware test rigs.

---

## Repository Structure

```text
iscandar/
├── allocator.py            # Main Python allocation engine & spatial coordinator
├── Bijection.py            # Coordinate transformation bijections
├── Coordinate.py           # Virtual 3D coordinate vector definitions
├── Modes.py / Mode.py      # Execution mode controls
├── Status.py               # Python wrapper for status codes
├── status.h                # C header defining runtime status codes & flags
│
├── Commit.c / Commit.h     # Sector commitment and state transition kernels
├── Mark.c                  # Sector marking and allocation logic
├── Unmark.c                # Deallocation and coalescence logic
├── Geometry.py             # Geometric layout and boundary rules
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
│
├── oracle/                 # Ground-truth reference drivers & test generators
│   ├── creators/           # Direct TLU oracle generation scripts (replacing bit scans)
│   └── timing/             # Latency & variance benchmark harnesses
│
├── paper/                  # Manuscript source and build artifacts
│   └── Iscandar_24b.pdf    # Monograph specification document
└── notes/                  # Design doctrine, JOSS framing, and architecture notes
```
