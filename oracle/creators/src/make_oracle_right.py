#!/usr/bin/env python3
"""Manufacture OracleRight.bin — the Right Oracle of Appendix D.

Python re-issue of the paper's Listing 7. The file format is unchanged.

Format: 2^32 rows x 2 bytes (8,589,934,592 bytes, 8 GiB), one row per
32-bit occupancy state S, rows in ascending S order.

Bit numbering is Motorola: Bit 0 is the MSB (leftmost), Bit 31 the LSB
(rightmost). A set bit is occupied, a clear bit is free.

As written in Listing 7, the Right Oracle reports the free run that
starts at the MSB (the leading run, counted from the left edge):

- If S & 0x80000000 != 0 (MSB occupied): Byte A = 255 (blocked),
  Byte B = 0.
- Else: Byte A = r, the length of the leading run of clear bits counted
  from the MSB downward; Byte B = 0 always.

The APL side resolves with (Length StartPos) = row S.

The file is written block by block and never held in memory; it is meant
to be memory-mapped, not loaded. Use --start/--states to manufacture in
pieces, and --verify to check the row logic against the paper's
spot-check states without writing anything.
"""

import argparse
import os
import sys

STATES = 1 << 32          # one row per 32-bit occupancy state
ROW_BYTES = 2             # Byte A (length), Byte B (start position)
BLOCKED = 255             # 0xFF sentinel: the run's edge bit is occupied
MSB = 0x80000000          # Bit 0 in Motorola numbering
BLOCK = 1 << 20           # rows per write block


def right_row(state):
    """Return the 2-byte Right row for occupancy state `state`."""
    if state & MSB:                     # MSB occupied: blocked
        return bytes((BLOCKED, 0))
    r = 0                               # leading run of clear bits
    while r < 32 and not (state << r) & MSB:
        r += 1
    return bytes((r, 0))


# Spot-check rows from the paper's formulas (see --verify).
SPOT_CHECKS = {
    0x00000000: (32, 0),                # whole word free
    0xFFFFFFFF: (BLOCKED, 0),           # MSB occupied
    0x00000001: (31, 0),                # 31 clear bits lead the LSB
    0x80000000: (BLOCKED, 0),           # MSB occupied
}


def verify():
    ok = True
    for state, expected in sorted(SPOT_CHECKS.items()):
        got = tuple(right_row(state))
        status = "ok" if got == expected else "MISMATCH"
        if got != expected:
            ok = False
        print(f"S=0x{state:08X}  got {got}  expected {expected}  {status}")
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
                block += right_row(state)
            f.write(block)
            done += n
            print(f"{start + done} / {start + count} states", file=sys.stderr)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=(os.path.join(r"O:\oracle", "OracleRight.bin") if os.name == "nt" else "OracleRight.bin"),
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
