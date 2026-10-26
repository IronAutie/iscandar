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
  orcid: 0000-0000-0000-0000
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

# References
