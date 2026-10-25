# Rotate theory (committed, tagged, pushed — the keeper)

Status (user, 2026-10-24): Rotate faithfully implements all he
set out to do in 1998. It is the pushed tip (commit 08db207,
tag Rotate, remote main and tag both 08db207). This note records
the theory and its measurements. It does not change the code.

## The rule

Rotated search vectors, from the 1998 design (memory allocator
for RTOSes on the Intel 80188 and Motorola 68332, proprietary
industry work, recovered in 2026 after the copyright lapsed).
The user's words: nobody on God's green earth would use that as
an allocation data structure. The rotated search is the alien
part.

The rule: a function-local static start inside planes_gear,
+1 per entry (failures included), wrapping 31 -> 0. The driver
walks 32 guarded unrolled lane statements from start, wrapping
back to lane 0, so every lane is tried exactly once and
GEAR_EXHAUST still means the whole cube was searched. Advance
at entry: the first sweep after the change starts at lane 1
(a disclosed choice; the phase question is formally open — see
below).

Implementation: 32 lane procedures + pointer table + unrolled
cursor driver ((*lane++)(args), no loop), failure mapping (a)
exact preservation (a lane collapses any row-handler non-success
into GEAR_EXHAUST). Lanes were untouched by the later sticky
and camping experiments, which changed the driver only.
Single-threaded working assumption (embedded origin), so the
function-local static is acceptable. C90 style for VS2010;
gcc-verified on this VM. The CIC cl build is still owed:
Rotate is pushed but not cl-built (see below).

## Linear space, rotated search — the distinction that matters

Rotate keeps the space linear and rotates only the search
order. Intervals do not wrap; the overrun guard stays start
plus count under 32768; commit stays linear; pointers stay
linear. The circularity is in the order of searching, not in
the space.

This is the correction the user made when an earlier reading
conflated the two: rotated search is NOT a wrap-around address
space. The wrap-around address space is a separate, future
idea — the ring (notes/ring-sector-space-DRAFT.md) — where the
space itself is circular. Rotate is present and committed;
the ring is future and unimplemented. Do not merge them.

## Gates (verified, not a bug)

Every lane bypasses a plane with inadequate total count whole:
remaining = 1024 - count_planes[N]; request > remaining means
return GEAR_EXHAUST, one gate read, no trial; boundary exact
(remaining == request is tried). RowsCheck mirrors it. The
shim is identical. Caveat by design: gates see totals, not
arrangement — a plane with adequate total room but fragmented
rows is still tried and can acquit. Gates bypass inadequate
COUNT; probes discover inadequate ARRANGEMENT.

## Measurements (seed 1, identical traces, GammaCheck green)

Sprint (ramp 85%, churn 5000, push 20000, cap 100000):
- Buddy stalls op 6059 (ramp), logical 83.67%, physical
  100.00% — a capacity stall from rounding (mean request 4.5
  vs mean block 5.375, ratio about 1.194).
- Rotate Iscandar stalls op 12029 (push), 95.89%, largest free
  5, margin 5970 ops over buddy.
- Comparison: first-fit-low stalls 12191 at 98.23%, largest
  free 3, margin 6132; sticky stalls 11903 at 94.17%,
  largest free 7, margin 5844; camping stalls 11898 at
  94.10%, largest free 7, margin 5839.
- Motion (alloc accesses): Rotate mean 3.27, var 1.28, median
  3, max 45 (vs first-fit-low 6.12/78.24/75; sticky
  3.16/0.34/10; camping 3.16/0.33/10). Bands near-flat far
  longer than first-fit-low (85-90%: 3.87 vs 21.85; 90-95%:
  4.54 vs 18.22).
- Gate reads (alloc): Rotate mean 19.73 (vs first-fit-low
  149.58; sticky 19.70; camping 19.70).
- Total touches (accesses + gates, the energy proxy):
  Rotate 23.00 (vs first-fit-low about 155.7; sticky 22.86;
  camping 22.86).
- Reuse: Rotate 2627 reused, mean 700.30, median 286, min 1
  (vs first-fit-low 2782/493.75/20; sticky 2119/1644.27/1496;
  camping 2114/1644.31/1502).

Abuse (70% logical steady, 50,000 steady ops, 55,062 executed):
- No stall either engine. End states identical across rules:
  largest free 32, total free 10310, physical 68.54%.
- Largest-free steady trend: Rotate flat 32 at every steady
  op (first-fit-low also flat 32; sticky dips to 27, mean
  31.81, 2254 of 50000 records below 32).
- Motion steady (alloc accesses): Rotate mean 4.48, var 3.12,
  median 4, max 14 (vs first-fit-low 19.26/301.75/14/98;
  sticky 3.70/1.08/3/12).
- Gate reads steady: Rotate mean 14.17 (vs first-fit-low
  269.09; sticky 18.87).
- Total touches steady: Rotate 18.66 (vs first-fit-low
  288.35; sticky 22.58).
- Reuse steady: Rotate 24098 reused, mean 887.74, median 284
  (vs first-fit-low 24634/160.72/16; sticky
  22748/3662.31/3578). Rotate reuse is stable across regimes
  (sprint 286, abuse 284); sticky degrades fivefold under
  churn (1496 to 3578).

Cross-checks: rotated shim vs C driver, 38/38 paired calls
match (phase walk, gate skips, wrap targets, 20 random).
Rotation tests pass (phase sequence 1..31,0,1; wrap finds
before-start room; advance on failure; gate skip; last
wrapped lane).

## Disadvantages (honest)

- Earlier stall than first-fit-low: 95.89% vs 98.23% (2.34
  points). Mechanism: first-fit-low's late advantage was the
  pristine reserve (clean high rows convicting to 98.23%);
  rotation fragments every row evenly, so no reserve remains.
- Slower reuse than first-fit-low: median 286 vs 20 (sprint),
  284 vs 16 (abuse). Freed space waits for the rotation to
  return and win first-fit.
- Fatter sprint access tail than sticky: max 45 vs 10,
  var 1.28 vs 0.34, though the means tie near 3.2.
- Sprint total touches tie with sticky (23.00 vs 22.86 —
  sticky by a hair).

A prior prediction was wrong and is owned here: rotation was
predicted to cost more firings at high occupancy. It is
quieter, not louder. The same evenness that spends the reserve
avoids acquittal walks.

## Advantages (why they overcome)

- Energy under churn, the embedded steady state: 18.66 total
  touches vs first-fit-low's 288.35 (about 15x quieter) and
  vs sticky's 22.58 (Rotate wins churn energy).
- Quiet motion and even wear: fragments evenly, no pristine
  reserve but no hot plane either; variance far below
  first-fit-low.
- Determinism: bounded sweep (A, k only), full cycle,
  EXHAUST cube-true; no split/coalesce, no tree walks.
- Abuse resistance: largest-free flat 32 at 70%/50k (ties
  first-fit-low, beats sticky's dips).
- Reuse stability across regimes (286 to 284), vs sticky's
  degradation.
- Simplicity: a blind +1 per entry, no outcome-conditional
  logic (vs sticky's conditional stay-or-advance, camping's
  jump to conviction).
- Faithfulness: implements the 1998 design as set out.

Scoreboard (user, 2026-10-24): on embedded, energy and
determinism are the prize; pristine-ness is smoke. On that
scoreboard the stall-point loss to first-fit-low is not
decisive, and Rotate wins where it counts: churn energy,
quiet motion, abuse resistance, determinism. Verdict
(2026-10-24): some disadvantages, but enough advantages
overcome. Rotate is the keeper.

## Open and owed

- CIC verification: real cl build via the updated
  build_gears.bat, DLL load, and an Engine.mark / Gears.scan
  end-to-end run through the real gears. Unverifiable from
  this VM. The harness shim must never be mistaken for this.
- Phase question (formally open): advance-at-entry means the
  first committed sweep starts at lane 1. Whether the 1998
  design started at 0 first is unanswered; the correction was
  invited and never given. Moot unless Rotate is ever revised.
- Failure mapping (b) (fail fast on GEAR_FAIL) remains
  available for any driver variant, never picked.
- The 98% plane-skip proposal (request-independent gate) is a
  separate idea, not part of Rotate; whether it composes with
  Rotate is unconsidered.
