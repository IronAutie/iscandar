# Oracle creators

The source of every program that manufactures the Iscandar oracle tables,
kept in one place, independent of the engine code. All four implement the
math as specified in Appendix D of the paper (Motorola bit numbering:
bit 0 is the most significant / leftmost bit; a set bit is occupied; the
row index is the full 32-bit occupancy state). The `.bin` layouts are as
specified in the paper.

## The paper's generator listings

Streaming, listing-faithful generators — one per oracle. These also live
in the standalone listings repo (IronAutie/iscandar-listings).

- `make_oracle_center.py` — OracleCenter.bin: 2^32 rows × 9 bytes
- `make_oracle_left.py` — OracleLeft.bin: 2^32 rows × 2 bytes
- `make_oracle_right.py` — OracleRight.bin: 2^32 rows × 2 bytes

Each supports `--verify` (the paper's spot-check rows) and
`--start`/`--states` for partial generation.

## The production creator

- `create_oracles.py` — the vectorised NumPy creator (all three tables,
  plus a `selftest` subcommand that reads finished files back by `mmap`
  and checks them against literal transcriptions of the paper's listing
  formulas). This is the program that manufactured the first full set of
  tables on 2026-10-22: OracleCenter.bin (38,654,705,664 bytes),
  OracleLeft.bin and OracleRight.bin (8,589,934,592 bytes each),
  verified ALL OK on edge-case and random states.

```
python3 create_oracles.py all --outdir <dir>
python3 create_oracles.py selftest --outdir <dir>
```

Open author's-call items, recorded as desk-check questions in
`notes/oracle-manufacture-notes.md`: the Left/Right naming cross in the
paper's listings (Listing 6 "Left" computes the run ending at the right
edge; Listing 7 "Right" the run starting at the left edge), and whether
the Center table's k ceiling of 8 is the intended ceiling.
