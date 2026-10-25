# JOSS lead framing (2026-10-25)

Author direction (his words, 2026-10-25): "We should lead with something
like that to JOSS." The "that" is the variance story for the embedded
and space audience, developed 2026-10-25 from the Nano Rotate report
with variances. This note saves the framing for the JOSS paper. The
paper itself (paper.md) is NOT drafted here: the engine is unfinished
(Tiny built, Small/Large/Huge pending) and JOSS scaffolding awaits the
author's word per his standing rule.

## Candidate lead (the shape, not final copy)

Flight software often bans dynamic allocation after initialization,
because malloc's timing is unpredictable. Iscandar is a dynamic
allocator that behaves like static allocation: a fixed 512 KiB pool,
no growth, and for the first 80% of the fill every allocation costs
exactly 3 sector-word reads. Not on average. Exactly. The same op
sequence always gives the same placements, the same costs, and the
same stall point, so ground testing reproduces flight behavior. That
is the thing no malloc can promise.

## Why it lands

- Variance is what a real-time system provisions for. A mean is a
  press release; a deadline is budgeted on the worst case.
- Buddy's mean is 4.00, but you cannot budget 4. You budget 28, the
  max, because its variance is about 8 from the very first band.
  Median 2, mean 4, max 28: fourteen times the typical cost must sit
  in the budget, or a deadline is eaten.
- Iscandar Rotate: typical equals max equals 3 for 80% of the fill.
  You budget exactly what you pay. Nothing wasted on the tail.

## Evidence (Nano Rotate, seed-1-rotated, seed 1, Nano range)

- Iscandar alloc accesses: variance 0.00 in every 5-point physical
  band from 0 to 80% (mean exactly 3.00); overall mean 3.27,
  variance 1.28, median 3, max 45, n 9,491.
- Buddy alloc accesses: variance 7.03 to 9.78 in every 5-point band
  from 0 to 100% physical, starting in the 0-5% band before any
  fragmentation exists; overall mean 4.00, variance 8.07, median 2,
  max 28, n 6,059.
- Stalls: buddy op 6,059 (ramp, 83.67% logical, 99.997% physical);
  Iscandar op 12,029 (push, 95.89% logical and physical). Margin
  5,970 ops, +12.22 logical points. GammaCheck green.

## Mechanism (one line each)

- Iscandar variance 0: Rotate spreads evenly, so the first lane tried
  has room and convicts on the first try (3 accesses on a successful
  alloc = 1 probe firing + 2), and the probe reads one word no matter
  what size was requested. Cost does not depend on the request.
- Buddy variance always: cost varies with request size (split depth)
  from the first request, in an empty arena. The variance is
  structural, not a load phenomenon.

## Boundaries (must stay in the paper, not just the pitch)

- The zero-variance region ends at 80%. Past that the tail grows:
  0.91, 1.96, 5.16, and 68.01 in the partial last band (n 67, Rotate
  stalls at 95.89%). The claim is "zero variance for the first 80%
  of the fill, bounded tail after," not "zero variance always."
- Gate reads are a separate series with their own variance (Rotate
  Nano: mean 19.73, variance 524.06, max 927 against the 1059 bound).
  They are counter reads, bounded and state-determined, not the
  probe's work.
- Total touches: buddy still wins (Nano Rotate total 23.00 vs buddy
  4.00). The claim is predictability, not fewer touches. Do not
  sell it as an energy win on this evidence.
- The audience that banned dynamic allocation is the point: the
  static pool (512 KiB, no growth) already matches flight discipline;
  the variance story answers the objection that got malloc banned.

## Update (2026-10-25): Tiny Rotate qualifies the pitch

Tiny-rotated race (seed-1-tiny-rotated, sizes 9..32): accesses variance
still exactly 0.00 (every alloc 3, every band 3.00/0.00), gate reads
flattened 463.20 to 25.26 mean as predicted, but Iscandar stalls op
1355, three ops into churn (84.97%), versus Tiny-FFL op 6447 after
surviving 5000 churn ops. Rotate's even spread plus Tiny's
first-run-only probe destroys large runs everywhere; FFL's pristine
high rows carry it through churn. Gate-walk variance is large in the
tail (overall 3217.05; 80-85% band 37551.98; stall sweep 1057, the
bound). So the variance pitch is strongest in Nano (Rotate: late
stall 95.89% plus near-zero variance). For Tiny the choice is FFL
(churn survival, variance 0.40) versus Rotate (perfect probe variance
0.00, churn-fragile). Do not sell Rotate's variance as mode-free.
The "exactly 3" claim is the probe's series; the gate series is
separate, bounded, and wild in the tail.

## Update (2026-10-25): Tiny sticky, hypothesis failed

Tiny-sticky race (seed-1-tiny-sticky, sizes 9..32): stalls op 1379,
27 ops into churn (85.10%), versus Rotate op 1355 and FFL op 6447.
Accesses variance 0.00073 (mean 3.0007, a single 4-access alloc in
1366); gates mean 22.22, variance 1612.94, max 1038. The stay-put
hypothesis failed: sticky does NOT avoid Rotate's Tiny churn stall.
Reading: only the pinned start (FFL, restart at plane 0 every call)
re-tries low-plane holes first every call. Any advancing start
(Rotate blind +1, sticky ratchet +1 on start-plane failure) drifts
forward and strands low-plane holes behind it, and the Tiny probe
(first-run + tail only) cannot see a stranded middle hole, so the
stall is a count stall (0 probe firings, full 1057 sweep) for both.
Nano survives spreading because Center finds a run anywhere in the
word, with no first-run restriction. For Tiny, variance does not
separate the rules (Rotate 0.00, sticky 0.00073, FFL 0.40, all tiny);
churn survival does, and only FFL has it.

## Update (2026-10-25): Tiny camp, near-twin of sticky

Tiny-camp race (seed-1-tiny-camp): stalls at the exact same op as
sticky (1379, churn, 85.10%, same stall record); accesses variance
exactly 0.00; gates mean 21.07, variance 357.88, max 408 (lowest of
the advancing rules). Camp vs sticky CSVs differ in only 6
churn-tail records. Jumping to conviction strands like ratcheting:
the Tiny family is complete, and only the pinned start survives
churn. Pack-first (advance only on full) remains the untested rule
shape that packs like FFL.
