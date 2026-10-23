# Iscandar — Python Engine

The working code repository for **Iscandar**, a deterministic memory
allocator: an extension of buddy systems to arbitrary radix (radix 32,
depth 3 in the reference configuration), by Andrew Jonathan Fine.

The radix design is the contribution, and it is itself O(1). The oracles
are not the innovation: an oracle is an anticipation of the buddy system's
own action — an existing O(1) engine dropped in so that placement does not
degrade the radix design. Oracles replace search: where a conventional
allocator examines candidates, Iscandar consults a table keyed by the
counter state that returns the placement directly. The counters keep the
books, so an imperfect oracle costs placements, never consistency.

## Layout

- `paper/` — the paper. `Iscandar_24b.pdf` is the latest copy the author
  has access to (50 pages, rendered 2026-06-01). The paper stands as-is.
  - Version history of the paper: https://github.com/IronAutie/iscandar-history
  - The paper's listings as a standalone repo: https://github.com/IronAutie/iscandar-listings
- `code/oracles/` — `create_oracles.py`, the Python procedure that
  manufactures the oracle tables as bitwise files, from the math as
  specified in Appendix D of the paper. (The paper's APL oracle access
  files are being replaced with Python equivalents; the `.bin` layouts
  are unchanged.)
- `notes/` — design and manufacture notes, including the oracle
  manufacture desk-check brief and the draft literature/independence
  notes.

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

Slow to create, once, in advance; afterwards every lookup is a single
memory-mapped read. The first full set was generated and verified on
2026-10-22: fresh-process `mmap` readback of all three files against
literal transcriptions of the paper's listing formulas, on edge-case and
random states — all checks passed.

## Provenance

The design was developed in 1998 as proprietary industry work, without
access to the published literature, and was reconstructed from the
author's memory in 2026, after the copyright in the original work had
lapsed; parts of it therefore duplicate published results independently
(see the independence note in `notes/` and in the history repo's README).
Assistance disclosure, in the author's framing: Gemini assisted with
literature search, grammar, and organizing; the argument and the
assembly are the author's.

## Status

The Python engine — Iscandar implemented beside a simulated buddy
allocator, identical traces through both, comparing Iscandar's flat
k×A per-operation cost against the buddy system's degradation with
occupancy and fragmentation — is the author's current work, in progress.
