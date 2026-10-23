# Oracle timing

Standalone random-access timing programs for the three manufactured
oracle tables. Each program memory-maps one complete table and reads the
complete row for uniformly random 32-bit states.

- `time_oracle_center.py` — OracleCenter.bin, 9 bytes per row
- `time_oracle_left.py` — OracleLeft.bin, 2 bytes per row
- `time_oracle_right.py` — OracleRight.bin, 2 bytes per row

The programs use only the Python standard library. On the author's
Windows machine they default to the corresponding file under
`O:\oracle`; `--file` overrides the path. A program refuses to run if
the file does not have the exact size of a complete table.

Each run makes a null-baseline pass and three oracle passes over
20,000 random states by default:

1. **null baseline** — the same states and loop, but the pass sums a
   constant dummy row instead of reading the table;
2. **first-touch A** — the first set of states, in whatever cache state
   the operating system already has;
3. **warm repeat A** — the same states again, normally served largely
   from the OS page cache;
4. **first-touch B** — a second set of random states, as a check on the
   first-touch result.

Each oracle pass reports both its raw time and a null-corrected
estimate obtained by subtracting the null-baseline time. The corrected
figure estimates the incremental cost of the table access on that
machine; it does not remove storage-stack costs, and a page fault is
not perfectly additive, so it should not be treated as an exact
physical constant.

The first-touch passes are not guaranteed to be completely cold: the OS
may already hold some pages in cache. `--samples` and `--seed` can be
used to change the workload.

```cmd
py oracle\timing\time_oracle_center.py
py oracle\timing\time_oracle_left.py
py oracle\timing\time_oracle_right.py
```
