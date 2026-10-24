# Driver doctrine — settled 2026-10-23 (his words, his rules)

Recorded from the Command chat, 2026-10-23 ~09:30–09:45 PDT, while the
engine's handlers were being designed. These are the author's decisions,
not proposals. The "next thrilling episode" (Nano) builds on them.

## The currency

- **"speed is irrelevant. determinism is our real goal."**
- **"we can invest speed without needing to hoard it."** A full sweep is
  an *investment*: cycles spent openly, returning a fixed work profile.
  A cut is *hoarding*: saving cycles we never needed, paying with a work
  profile that moves with the data. Speed is capital here, not treasure —
  spend it on certainty.

## The shape

- Drivers are **unrolled, one statement per lane**. "It will look ugly,
  but then we have replaced the scan with something in theory more
  deterministic, to support the paper." The Python stops imitating the
  drivers and *becomes* the drivers, transcribed — code and proof with
  the same shape.
- **No cut (no premature return).** Skipped probes buy speed, the one
  currency not being spent. Full sweep: executed probe count is the
  width, whatever the cube holds. Cut: executed probe count becomes the
  first-fit position, so the work depends on the occupancy pattern —
  a hostile reader gets to say "early-exit scan" again. If an optimized
  variant ever wants the cut, it must prove equivalence by differential
  testing and wear the label "optimization," not "specification."
- **Probes fire unconditionally** — every lane, exactly once — with
  selection *after* the sweep. Guarding each probe with "only if nothing
  found yet" keeps the statement count fixed but lets the probe count
  vary with the data. First acceptance wins for selection either way.
- **One semantics, no options.** The driver always sweeps the full width
  and takes the first hit by fixed priority — comparators plus a
  priority encoder, in software form. No "exit when found" knob: the
  driver must refuse that flag, or search comes back in through the side
  door.
- **Probes stay pure.** A probe checks and reports; it never commits.
  Γ updates in exactly one place, outside the checker. (His standing
  rule, reaffirmed tonight.)
- **Hierarchy composes.** The wide scans don't need a 1,024-statement
  body: an unrolled 32-lane driver over planes, each lane running the
  unrolled 32-lane driver over rows. A² lanes, two 32-statement bodies,
  the APL's composition kept intact.

## The invariant (stated in words, next to the loops)

**Trip count depends on A and k only — never on heap size, occupancy,
fragmentation, or allocation history.** An unconditional fixed scan is
not search; an "advance until found" loop would be. Readers must not
have to infer this from unrolled code alone.

## The road sign

The unrolled block is **"a silicon expansion road sign."** A road sign
doesn't pave the road — it tells the traveler where the road widens:
*here* the lanes become comparators, *here* the width becomes area,
*here* first-acceptance becomes a priority encoder. Roll it into a loop
or cut it short and you haven't optimized the code — you've taken the
sign down.

## What the tests assert

Operation counts and outcomes — probe counts identical across different
cube fillings, identical requests returning identical pointers — and
**never timings**. A reviewer can't argue with a count.

## Retracted in the same session

An earlier sketch in this session proposed `driver(width, probe)` as a
`for` loop with a callable probe per lane. Corrected same-session by
the author: not a loop at all — unrolled statements. The loop sketch is
dead; this file supersedes it.
