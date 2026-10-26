---
title: 'iscandar: A Drop-in Memory Allocator with Bounded Variance via Fractal Virtual Coordinate Mapping'
tags:
- C
- Python
- memory allocation
- deterministic systems
- virtual coordinates
authors:
- name: Andrew Jonathan Fine
  orcid: 0009-0001-2312-380X
  affiliation: 1
affiliations:
- name: Independent Researcher in Computer Architecture
  index: 1
date: 25 October 2026
bibliography: paper.bib
---

# Summary

`iscandar` is a drop-in replacement memory allocator designed for deterministic memory management. Implemented as a hybrid Python and C architecture, it responds to memory allocation requests by mapping sectors to a series of 32-bit virtual pointers constructed at a scale of 4 bytes per sector allocated. The allocator targets a controlled 5-sigma variance in sector map touches per allocation, providing predictable performance bounds backed by an integrated oracle testing and verification framework.

# Statement of Need

General-purpose memory allocators prioritize average-case throughput often at the expense of strict variance bounds and inspectability, making them difficult to analyze in deterministic or constrained environments. `iscandar` addresses this need by providing an open-source, drop-in replacement for `malloc` that bounds sector map touch variance within 5-sigma limits [@fine2026iscandar]. By explicitly pairing high-level validation routines with low-level C drivers, `iscandar` gives researchers and systems engineers a transparent, verifiable memory allocation architecture for testing and deployment [@wilson1995dynamic; @masmano2008implementation].

# State of the Field & Software Design

Standard C memory allocators (such as `jemalloc` or `ptmalloc`) operate primarily as black-box subroutines optimized for general throughput, offering limited real-time inspectability into internal sector allocations without substantial profiling overhead [@berger2000hoard; @evans2006scalable].

`iscandar` exposes runtime status symbols and explicit monitoring hooks within its C API (`status.h`). This design allows embedded diagnostic tooling, C test scripts, and outer-loop orchestration frameworks to inspect, control, and trace memory allocation state changes in real time.

# Architecture & Design

`iscandar` implements memory allocation via a multidimensional (k=3) fractal virtual coordinate mapping, overlaid as a bijection upon a linear (A=32) sector space kept in memory [@mandelbrot1982fractal; @bentley1975multidimensional]. By mapping linear allocation requests onto this fractal coordinate space, the architecture constrains sector map touches to a controlled 5-sigma variance [@montgomery2019introduction].

The codebase couples high-level Python components for spatial modeling and verification with performance-critical C drivers handling the underlying sector state. Status symbols are explicitly exposed via `status.h`, allowing external C and Python scripts to monitor, step through, and validate allocation progress in real time.

# Acknowledgements

To Jennifer: Everything. Always. Forever.

# AI Usage Disclosure

In early 2026, at his therapist's suggestion to ease the PTSD from a project he was forced to walk away from in 1998, the author transcribed his designs for the memory allocator he had made into drawings and charts, using his own notation and pseudocode. Gemini identified that work as noteworthy, taught him the proper mathematical notation to turn those notes into the skeleton of an academic paper, and then conducted a literature search showing its dependence on fundamental concepts from his schooling and work. Gemini also informed him that the company he had worked for had gone defunct, and that after the lapse period he had therefore inherited the copyright as the original author. Gemini never directly generated the Overleaf files; the author typed phrases directly into the LaTeX and accepted suggestions for formatting.

Due to hallucinations Gemini suffered attempting to generate and test proper APL, the author turned to Muse to generate C and Python instead, into a testable and modular system. The core design, equations, and mathematics remain the author's, and he reviewed, edited, and validated the resulting work.

Note on versions: the author was not a sophisticated user of AI at the time, so the exact Gemini model version was not recorded, and is not in the Overleaf history. The earliest Overleaf Iscandar paper is dated 7 April 2026. By now he has learned to use AIs as bound demons for routine tasks.

Starting dates, supported by evidence on Overleaf: Gemini's work on this paper began with the Overleaf project "Iscandar", created 7 April 2026. Muse's work began early last week, give or take, in mid-October 2026.

The original hand drawings are in the FractalClosedMemory wiki, Table of Drawings, Chapters 1–3. They are the author's link to the 16-bit oracles for the Intel 80188 and Motorola 68332.

# References
