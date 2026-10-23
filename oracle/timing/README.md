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

Each run makes three passes over 20,000 random states by default:

1. **first-touch A** — the first set of states, in whatever cache state
   the operating system already has;
2. **warm repeat A** — the same states again, normally served largely
   from the OS page cache;
3. **first-touch B** — a second set of random states, as a check on the
   first-touch result.

The first-touch passes are not guaranteed to be completely cold: the OS
may already hold some pages in cache. `--samples` and `--seed` can be
used to change the workload.

```cmd
py oracle\timing\time_oracle_center.py
py oracle\timing\time_oracle_left.py
py oracle\timing\time_oracle_right.py
```
