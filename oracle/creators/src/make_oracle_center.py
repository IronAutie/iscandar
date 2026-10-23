#!/usr/bin/env python3
"""Manufacture OracleCenter.bin — the Center Oracle of Appendix D.

Python re-issue of the paper's Listing 5. The file format is unchanged.

Format: 2^32 rows x 9 bytes (38,654,705,664 bytes, 36 GiB), one row per
32-bit occupancy state S, rows in ascending S order.

Bit numbering is Motorola: Bit 0 is the MSB (leftmost), Bit 31 the LSB
(rightmost). A set bit is occupied, a clear bit is free.

Row S, byte k (k = 0..8) is the position of the requested allocation
length k:

- k = 0 is redundant and always 0.
- For k >= 1: the leftmost position pos in 0..(32-k) such that the k
  consecutive bits starting at pos are all clear in S ("closest to left"
  packing, first hit wins), or 255 (0xFF) if there is no such run.

  Mask, as written in Listing 5:  (2^k - 1) << (32 - k - pos);
  hit iff (S & mask) == 0.

The file is written block by block and never held in memory; it is meant
to be memory-mapped, not loaded. Use --start/--states to manufacture in
pieces, and --verify to check the row logic against the paper's
spot-check states without writing anything.
"""

import argparse
import os
import sys

STATES = 1 << 32          # one row per 32-bit occupancy state
ROW_BYTES = 9             # one byte per requested length k = 0..8
MAX_K = 8                 # largest requested length in the table
FAIL = 255                # 0xFF sentinel: no run of the requested length
BLOCK = 1 << 20           # rows per write block


def center_row(state):
    """Return the 9-byte Center row for occupancy state `state`."""
    row = bytearray(ROW_BYTES)      # byte 0 (k = 0) stays 0
    for k in range(1, MAX_K + 1):
        run = (1 << k) - 1
        found = FAIL
        for pos in range(0, 32 - k + 1):
            mask = run << (32 - k - pos)
            if state & mask == 0:
                found = pos
                break               # first hit wins
        row[k] = found
    return bytes(row)


# Spot-check rows from the paper's formulas (see --verify).
SPOT_CHECKS = {
    0x00000000: bytes([0, 0, 0, 0, 0, 0, 0, 0, 0]),          # pos 0, every k
    0xFFFFFFFF: bytes([0] + [FAIL] * MAX_K),                 # no room at all
}


def verify():
    ok = True
    for state, expected in sorted(SPOT_CHECKS.items()):
        got = center_row(state)
        status = "ok" if got == expected else "MISMATCH"
        if got != expected:
            ok = False
        print(f"S=0x{state:08X}  got {list(got)}  "
              f"expected {list(expected)}  {status}")
    return ok


def manufacture(out_path, start, count):
    mode = "r+b" if start else "wb"
    with open(out_path, mode) as f:
        f.seek(start * ROW_BYTES)
        done = 0
        while done < count:
            n = min(BLOCK, count - done)
            block = bytearray()
            for state in range(start + done, start + done + n):
                block += center_row(state)
            f.write(block)
            done += n
            print(f"{start + done} / {start + count} states", file=sys.stderr)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=(os.path.join(r"O:\oracle", "OracleCenter.bin") if os.name == "nt" else "OracleCenter.bin"),
                    help="output file (default: the pinned O: oracle folder on Windows)")
    ap.add_argument("--start", type=int, default=0,
                    help="first state to write (default: 0)")
    ap.add_argument("--states", type=int, default=STATES,
                    help="number of states to write (default: all 2^32)")
    ap.add_argument("--verify", action="store_true",
                    help="check row logic against the spot-check states; "
                         "write nothing")
    args = ap.parse_args(argv)

    if args.verify:
        return 0 if verify() else 1
    if not (0 <= args.start and 0 < args.states
            and args.start + args.states <= STATES):
        ap.error("require 0 <= start, 0 < states, start + states <= 2^32")
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    manufacture(args.out, args.start, args.states)
    return 0


if __name__ == "__main__":
    sys.exit(main())
