# Nano handler — source map for the first limb

Everything the author's Nano decision needs, gathered in one place so the
"thicket of APL" doesn't have to be re-hacked on the night. This is an
index of his own sources, not new code. The handler itself is his to
author; the doctrine it must satisfy lives in
`notes/driver-doctrine-2026-10-23.md`.

Source: `~/workspace/iscandar-history/main.tex` (the paper), plus the
Command chat 2026-10-23.

## Dispatch: the decision table (main.tex, DecisionTable dfns)

```
⍝ --- Tier Mapping via Byte-Arity ---
⍝ B: 8, R: 32, P: 1024, C: 32768

Table ← C ⍴ ⊂##.Heuristic.Null

Table[1+⍳B] ← ⊂##.Heuristic.Nano        ⍝ L in 1..8 → Nano
Table[B+⍳(R-B)] ← ⊂##.Heuristic.Tiny
Table[R+⍳R] ← ⊂##.Heuristic.Small
Table[(2×R)+⍳(P-(2×R))] ← ⊂##.Heuristic.Large
Table[P+⍳(C-P)] ← ⊂##.Heuristic.Huge
Table[C] ← ⊂##.Heuristic.Cube
```

Resolve's range guard: `1 ≤ s ≤ C` (32768), else `STATUS_FAILURE`.

## Mechanism: §8.4.2 "The Nano Resolution (L ≤ A/4)"

- **Domain:** the bit-lattice within a single word or sub-word segment of a
  Row — requests of 1 to 8 bits (A/4 when A=32).
- **Mechanism:** isolate a single byte-aligned segment of the Row to
  extract a *Seed Polytope*; ignore higher-level boundary conditions,
  focus on high-speed intra-byte contiguity.
- **Geometric event:** an *Intersection of Atomic (Seed) Polytopes*.
- **Resolution:** the **Center Oracle** intersects the current Row's
  bit-pattern with the requested length L, mapping the pattern to an
  exact fit of available sectors — a seed polytope of 1 to 8 bits, to be
  joined with other polytopes later. "Deterministic single-cycle
  intersection… evaluated via the row driver logic detailed in
  Listing 17 (HeuristicNano.apl)."

## The APL to replace: Listing 17, HeuristicNano.apl (verbatim)

```apl
:Namespace Heuristic
  :Namespace HeuristicNano
    ⍝ --- Constants ---
    OK ← CONSTANT.STATUS_SUCCESS
    FAIL ← CONSTANT.STATUS_FAILURE
    LIMIT ← 1023

    ⍝ --- Function: SectorChecker ---
    ⍝ Args: (Row Offset L)
    ∇ Result ← SectorChecker Args;Row;Offset;L
      ∇ Result ← SectorChecker Args;GlobalRow;X;S;P
      (Row Offset L) ← Args
      GlobalRow ← Row + Offset

      ⍝ Boundary Check
      →(GlobalRow > LIMIT)/FAIL_EXIT

      X ← Cube.Rows[GlobalRow]
      S ← X.sectors

      ⍝ 2D Indexing: Use Oracle as bit scan
      P ← Oracle.Center[S;L]

      →(P < 0)/FAIL_EXIT
      Result ← OK P ⋄ →END

      FAIL_EXIT:
        Result ← FAIL 0
      END:
    ∇

    ⍝ --- Function: Main ---
    ∇ Result ← Main L;Offset
      Offset ← 0
      Result ← SectorChecker RowsDriver.Run
               PlanesDriver.Run (Offset L)
    ∇
  :EndNamespace
:EndNamespace
```

Reading: `Main` composes `RowsDriver.Run` with `PlanesDriver.Run` around
the `SectorChecker` probe; the probe reads the row's sector pattern `S`,
indexes `Oracle.Center[S;L]`, and returns `OK P` (a Coordinate) or
`FAIL 0`. The new caller wraps whatever Coordinate comes back into an
MPUPointer (settled tonight).

## The path: §10 Desk Check, "The Nano Path (L ≤ A/4)"

1. **Admissibility (Gate 3):** Global Registrar fetches the 16-bit register
   at the Apex sector address; single-cycle comparison against Γ_Apex to
   permit or fast-fail.
2. **Steering (Gates 2, 1):** Rotational Steering Vector (R⃗) selects a
   candidate Plane and Row, bypassing saturated volumes via PMASK/RMASK
   metadata sentinels — no bit-level interrogation.
3. **Nano:** isolate the byte-aligned segment of the Row; index the
   **Center Oracle** for a single-pass intersection; the atomic
   intersection maps the Row's bit-pattern to an exact fit of available
   sectors.
4. **Lattice Commitment:** the run maps to a pointer of bit offset and
   length; occupancy state commits to the local metadata registers; the
   system returns the resolved wrapped pointer.

"Whether the system uses an Oracle to resolve a request through a
single-cycle Nano intersection or a dual-pass Tiny probe, the execution
path length is fixed."

## Oracle shape (already built, not to be re-derived)

- `Oracle.Center` = OracleCenter.bin: **2³² rows × 9 bytes**
  = 38,654,705,664 bytes, generated and verified 2026-10-22 (fresh-process
  `mmap` readback against literal transcriptions of the paper's listing
  formulas — all OK). See `notes/oracle-manufacture-notes.md`.
- `P ← Oracle.Center[S;L]` is a single memory-mapped row read for the
  32-bit occupancy state S and length L. Row already carries
  WIDTH=A=32, MASK=(1≪A)−1 (committed 2026-10-23, e0c9f26); Plane is a
  dict of 32 zero Rows with sparse reads (c178520); Cube = A³ = 32,768
  bits, one occupancy bit per sector of the 128 KiB pool.

## Status codes

`STATUS.FAIL_NANO ← 4` (STATUS namespace, main.tex ~line 1411).
`SUCCESS ← 0`.

## Sockets left open (not decided yet)

- **Failure's shape.** Explicitly left open in the 2026-10-23 session:
  the new caller wraps a Coordinate into an MPUPointer, but what
  Failure *is* (the value, the type, where it surfaces) is still to be
  pinned before Nano goes on the patient.
- Γ updates live in exactly one place, outside the checker — standing
  rule, reaffirmed tonight.
- The paper's own `[?]` placeholders (§4.2 ×2), "Figure??" (§11.3),
  duplicated sentence (§5.2), and the two "Axiom V" → Axiom IV slips are
  logged for a later fix pass on his order; the paper stays untouched
  until then. Not blockers for the handler.
