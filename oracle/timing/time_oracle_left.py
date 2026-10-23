#!/usr/bin/env python3
"""Time random row lookups in OracleLeft.bin through mmap.

Each lookup reads the complete 2-byte row for one uniformly random
32-bit occupancy state.  The script reports three passes:

* first-touch A: the A states, in the cache state in which they are found;
* warm repeat A: the same A states again, normally served from the OS
  page cache after the first pass;
* first-touch B: a second, disjoint set of random states.

Only the standard library is used.  State generation, opening the file,
and creating the mmap are outside the timed sections.
"""

from __future__ import annotations

import argparse
import mmap
import os
import random
import sys
import time
from pathlib import Path

ORACLE_NAME = "OracleLeft.bin"
ROW_WIDTH = 2
EXPECTED_SIZE = (1 << 32) * ROW_WIDTH
DEFAULT_SAMPLES = 20_000
DEFAULT_SEED = 20261022


def default_file() -> Path:
    if os.name == "nt":
        return Path(r"O:\oracle") / ORACLE_NAME
    return Path(__file__).resolve().parent / ORACLE_NAME


def time_pass(table: mmap.mmap, states: list[int]) -> tuple[float, int]:
    """Read one complete row for every state; return seconds and checksum."""
    checksum = 0
    started = time.perf_counter_ns()
    for state in states:
        offset = state * ROW_WIDTH
        checksum = (checksum + sum(table[offset : offset + ROW_WIDTH])) & 0xFFFFFFFFFFFFFFFF
    elapsed_ns = time.perf_counter_ns() - started
    return elapsed_ns / 1_000_000_000, checksum


def report(label: str, seconds: float, samples: int, checksum: int) -> None:
    microseconds = seconds * 1_000_000 / samples
    rate = samples / seconds if seconds else float("inf")
    print(
        f"{label:16s} {seconds:9.3f} s  "
        f"{microseconds:11.1f} us/lookup  "
        f"{rate:12.1f} lookups/s  checksum {checksum}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--file",
        type=Path,
        default=default_file(),
        help=f"oracle file to time (default: {default_file()})",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=DEFAULT_SAMPLES,
        help=f"random states per pass (default: {DEFAULT_SAMPLES})",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help=f"random seed (default: {DEFAULT_SEED})",
    )
    args = parser.parse_args(argv)

    if args.samples <= 0:
        parser.error("--samples must be positive")

    path = args.file.expanduser()
    if not path.is_file():
        print(f"error: oracle file not found: {path}", file=sys.stderr)
        return 2

    actual_size = path.stat().st_size
    if actual_size != EXPECTED_SIZE:
        print(
            f"error: {path} has {actual_size} bytes; "
            f"a complete {ORACLE_NAME} has {EXPECTED_SIZE} bytes",
            file=sys.stderr,
        )
        return 2

    rng = random.Random(args.seed)
    states_a = [rng.getrandbits(32) for _ in range(args.samples)]
    states_b = [rng.getrandbits(32) for _ in range(args.samples)]

    print(f"Oracle:       {ORACLE_NAME}")
    print(f"File:         {path}")
    print(f"Row width:    {ROW_WIDTH} bytes")
    print(f"Samples/pass: {args.samples}")
    print(f"Seed:         {args.seed}")
    print("Method:       random full-row lookups through mmap")
    print()

    with path.open("rb") as handle:
        table = mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            first_seconds, first_checksum = time_pass(table, states_a)
            warm_seconds, warm_checksum = time_pass(table, states_a)
            new_seconds, new_checksum = time_pass(table, states_b)
        finally:
            table.close()

    report("first-touch A", first_seconds, args.samples, first_checksum)
    report("warm repeat A", warm_seconds, args.samples, warm_checksum)
    report("first-touch B", new_seconds, args.samples, new_checksum)
    if warm_checksum != first_checksum:
        print("error: warm-pass checksum does not match the first pass", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
