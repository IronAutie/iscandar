#!/usr/bin/env python3
"""
create_oracles.py — manufacture the Iscandar oracle tables as bitwise files.

Implements Appendix D ("Oracle Manufacture") of Iscandar_24b.pdf, in Python
(replacing the paper's APL access files and PowerShell manufacture listings,
per the author's instruction, 2026-10-22).

Each file is a raw byte table indexed by the full 32-bit occupancy state S:
row S begins at byte offset S * row_width. The files are meant to be read as
memory by a Python process: np.memmap(path, dtype=np.uint8).reshape(2**32, W)
or mmap + index arithmetic. No header, no padding — exactly as the paper's
APL ⎕MAP layouts assume.

Bit numbering is Motorola, as in the paper: Bit 0 = MSB (leftmost),
Bit 31 = LSB (rightmost). A set bit is occupied, a clear bit is free.

  OracleCenter.bin  2^32 rows x 9 bytes.
      Column k = 0..8 is a requested allocation length. Column 0 is always 0.
      For k >= 1 the byte is the leftmost position pos in 0..(32-k) where k
      consecutive bits are all clear, i.e. (S & ((2^k - 1) << (32-k-pos))) == 0,
      first hit wins; 255 (0xFF) if no such run exists.
  OracleLeft.bin    2^32 rows x 2 bytes.
      The trailing free run (ends at the LSB). If S & 1: (255, 0) blocked.
      Else (r, 32 - r), r = length of the trailing run of clear bits,
      counted from the LSB upward.
  OracleRight.bin   2^32 rows x 2 bytes.
      The leading free run (starts at the MSB). If S & 0x80000000: (255, 0)
      blocked. Else (r, 0), r = length of the leading run of clear bits,
      counted from the MSB downward.

The chunk functions are vectorised transcriptions of the same math the
paper's listings compute one state at a time. A literal, listing-faithful
reference implementation is kept below (ref_center / ref_left / ref_right);
`--selftest` checks the vectorised code, and an already-created file read
back through mmap, against it.

Usage:
  python3 create_oracles.py all [--outdir DIR] [--chunk N]
  python3 create_oracles.py center|left|right [--outdir DIR]
  python3 create_oracles.py selftest [--outdir DIR]
  python3 create_oracles.py all --rows 100000 --outdir /tmp/test   # partial, for tests
"""

import argparse
import os
import sys
import time

import numpy as np

ROWS = 1 << 32
FAIL = 255


# Default home of the tables: the author's pinned O: drive on Windows
# (the letter is pinned in Disk Management so it cannot drift). On other
# platforms the tables default to this script's own folder.
# --outdir always overrides.
DEFAULT_OUTDIR = (r"O:\oracle" if os.name == "nt"
                  else os.path.dirname(os.path.abspath(__file__)))


# --------------------------------------------------------------------------
# Vectorised chunk builders (S is a uint32 numpy array of consecutive states)
# --------------------------------------------------------------------------

def center_chunk(S):
    """Return an (len(S), 9) uint8 array per the Center spec above."""
    n = S.shape[0]
    # run_end[:, p] = length of the run of clear bits ending at position p
    # (position 0 = MSB). One pass, left to right.
    run = np.zeros((n, 32), dtype=np.uint8)
    cur = np.zeros(n, dtype=np.uint8)
    for p in range(32):
        bit = ((S >> np.uint32(31 - p)) & np.uint32(1)).astype(np.uint8)
        cur = np.where(bit == 0, cur + np.uint8(1), np.uint8(0)).astype(np.uint8)
        run[:, p] = cur
    out = np.zeros((n, 9), dtype=np.uint8)  # column 0 stays 0
    for k in range(1, 9):
        # A run of length k starting at pos p exists iff run_end[p+k-1] >= k.
        window = run[:, k - 1:]                      # p = 0 .. 32-k
        cond = window >= np.uint8(k)
        has = cond.any(axis=1)
        first = cond.argmax(axis=1).astype(np.uint8)
        out[:, k] = np.where(has, first, np.uint8(FAIL))
    return out


def _run_lengths(S, shifts):
    """Count consecutive clear bits of S, visiting value-bit positions in the
    order given by `shifts` (shift amounts into the uint32). Returns uint8
    counts; counting stops permanently at the first set bit visited."""
    n = S.shape[0]
    r = np.zeros(n, dtype=np.uint8)
    counting = np.ones(n, dtype=bool)
    for sh in shifts:
        bit = ((S >> np.uint32(sh)) & np.uint32(1)).astype(bool)
        counting &= ~bit
        r += counting.astype(np.uint8)
    return r


def left_chunk(S):
    """Return an (len(S), 2) uint8 array per the Left (trailing run) spec."""
    r = _run_lengths(S, range(0, 32))                # LSB upward
    blocked = (S & np.uint32(1)).astype(bool)
    a = np.where(blocked, np.uint8(FAIL), r)
    b = np.where(blocked, np.uint8(0), (np.uint8(32) - r).astype(np.uint8))
    return np.stack([a, b], axis=1).astype(np.uint8)


def right_chunk(S):
    """Return an (len(S), 2) uint8 array per the Right (leading run) spec."""
    r = _run_lengths(S, range(31, -1, -1))           # MSB downward
    blocked = ((S >> np.uint32(31)) & np.uint32(1)).astype(bool)
    a = np.where(blocked, np.uint8(FAIL), r)
    b = np.zeros_like(a)
    return np.stack([a, b], axis=1).astype(np.uint8)


BUILDERS = {
    "center": ("OracleCenter.bin", 9, center_chunk),
    "left": ("OracleLeft.bin", 2, left_chunk),
    "right": ("OracleRight.bin", 2, right_chunk),
}


def generate(name, outdir, rows=ROWS, chunk=1 << 21):
    filename, width, builder = BUILDERS[name]
    path = os.path.join(outdir, filename)
    os.makedirs(outdir, exist_ok=True)
    total_bytes = rows * width
    print(f"[{name}] creating {path}: {rows:,} rows x {width} B = {total_bytes:,} bytes",
          flush=True)
    t0 = time.time()
    done = 0
    with open(path, "wb") as f:
        while done < rows:
            n = min(chunk, rows - done)
            S = np.arange(done, done + n, dtype=np.uint64).astype(np.uint32)
            f.write(builder(S).tobytes())
            done += n
            if done % (chunk * 64) == 0 or done == rows:
                pct = 100.0 * done / rows
                print(f"[{name}] {pct:5.1f}%  ({done:,}/{rows:,} rows, "
                      f"{time.time() - t0:.0f}s)", flush=True)
    size = os.path.getsize(path)
    assert size == total_bytes, f"{path}: wrote {size}, expected {total_bytes}"
    print(f"[{name}] done: {path} ({size:,} bytes) in {time.time() - t0:.0f}s", flush=True)
    return path


# --------------------------------------------------------------------------
# Literal reference implementations — the paper's listings, one state at a
# time, kept for verification. Slow by design; used only on samples.
# --------------------------------------------------------------------------

def ref_center(S):
    row = [0]
    for k in range(1, 9):
        found = FAIL
        for pos in range(0, 32 - k + 1):
            mask = ((1 << k) - 1) << (32 - k - pos)
            if S & mask == 0:
                found = pos
                break
        row.append(found)
    return row


def ref_left(S):
    if S & 1:
        return [FAIL, 0]
    r = 0
    for i in range(32):
        if S & (1 << i) == 0:
            r += 1
        else:
            break
    return [r, 32 - r]


def ref_right(S):
    if S & 0x80000000:
        return [FAIL, 0]
    r = 0
    for i in range(31, -1, -1):
        if S & (1 << i) == 0:
            r += 1
        else:
            break
    return [r, 0]


REFS = {"center": ref_center, "left": ref_left, "right": ref_right}

SAMPLES = [0x00000000, 0x00000001, 0x00000002, 0x80000000, 0xFFFFFFFF,
           0xFFFFFFFE, 0x7FFFFFFF, 0xAAAAAAAA, 0x55555555, 0x0000FFFF,
           0xFFFF0000, 0x00FF00FF, 0x12345678, 0xDEADBEEF, 0x000001FF,
           0xFF800000, 0x01010101, 0x80808080]


def selftest(outdir):
    rng = np.random.default_rng(20261022)
    states = SAMPLES + [int(x) for x in rng.integers(0, 1 << 32, size=2000,
                                                     dtype=np.uint64)]
    S = np.array(states, dtype=np.uint32)
    ok = True
    # 1) vectorised builders vs literal listings
    for name, (_, width, builder) in BUILDERS.items():
        got = builder(S)
        for i, s in enumerate(states):
            want = REFS[name](int(s))
            if list(got[i]) != want:
                print(f"SELFTEST FAIL {name} S=0x{int(s):08X}: got {list(got[i])}, want {want}")
                ok = False
        print(f"[selftest] builder {name}: {len(states)} states OK" if ok else
              f"[selftest] builder {name}: FAILURES above")
    # 2) any full-size files present in outdir, read back as memory via mmap
    for name, (filename, width, _) in BUILDERS.items():
        path = os.path.join(outdir, filename)
        if not os.path.exists(path):
            print(f"[selftest] {filename}: not present in {outdir}, skipped")
            continue
        if os.path.getsize(path) != ROWS * width:
            print(f"[selftest] {filename}: size {os.path.getsize(path)} != {ROWS * width}, skipped")
            continue
        table = np.memmap(path, dtype=np.uint8, mode="r").reshape(ROWS, width)
        for s in states:
            want = REFS[name](int(s))
            if list(table[int(s)]) != want:
                print(f"SELFTEST FAIL file {filename} S=0x{int(s):08X}: "
                      f"got {list(table[int(s)])}, want {want}")
                ok = False
        print(f"[selftest] file {filename}: mmap readback OK")
    print("[selftest] " + ("ALL OK" if ok else "FAILURES — see above"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("which", choices=["center", "left", "right", "all", "selftest"])
    ap.add_argument("--outdir", default=DEFAULT_OUTDIR)
    ap.add_argument("--rows", type=int, default=ROWS,
                    help="rows to write (default: full 2^32; smaller only for tests)")
    ap.add_argument("--chunk", type=int, default=1 << 21)
    args = ap.parse_args(argv)

    if args.which == "selftest":
        return selftest(args.outdir)
    names = ["center", "left", "right"] if args.which == "all" else [args.which]
    for name in names:
        generate(name, args.outdir, rows=args.rows, chunk=args.chunk)
    return 0


if __name__ == "__main__":
    sys.exit(main())
