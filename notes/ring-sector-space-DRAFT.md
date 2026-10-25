# Ring sector space (DRAFT — future idea, not implemented)

Status (user, 2026-10-24): the ring is saved for another day. It is
a future idea, not for now. Nothing in this note is implemented:
no C driver change, no shim change, no commit, no push. Rotate
(08db207) remains the pushed tip; the sticky-start change remains
working-tree only.

## The idea (his, 2026-10-24 — "a really absurd idea")

The pointers the engine returns are a representation rather than a
pointer itself, addressing a sector space that right now is linear.
What if it wasn't?

The space becomes a ring, not a line. Intervals are modular
(mod 32768) uniformly — not a privilege for the final plane, but
the absence of edges everywhere. Any block, run, or sequence
crossing the end of space wraps around to the beginning, at every
level: row to row, plane to plane, last to first. The final plane
is just where wrapping becomes visible, since a block starting
anywhere else never crosses the boundary and cannot tell the
difference.

This is distinct from rotated search, and the distinction matters.
Rotated search makes the sweep order circular. The ring makes the
space itself circular. Different layers, both circular now,
deliberately. (An earlier misreading conflated the two; the user
corrected it: rotated search is NOT a wrap-around address space.
The ring is the wrap-around address space, proposed separately
and deliberately.)

## The pointer does not change

MPUPointer format is unchanged: start plus count, born virtual.
A block at 32764 with count 8 is invalid linearly and valid on a
ring, and nothing in the representation tells you which. The
wrapping lives in interpretation (guard, commit, run arithmetic),
not in the pointer. That separation is the born-virtual payoff:
since the pointer was never a machine address, changing the
space's topology does not change the pointer's shape.

## What changes (analysis, endorsed by the user as doable)

- Overrun guard relaxes: instead of start plus count staying
  under 32768, only count stays under 32768, and the interval
  wraps modulo 32768.
- Commit splits a boundary block into at most two linear
  intervals, the tail at the top plus the head at the bottom.
  At most twice the work for those blocks; the bound survives.
- Runs become modular intervals. Boundary cases reuse patterns
  already in the design: a Nano block wrapping past the last
  row's end becomes a cross-row join like Small, and a
  multi-plane wrap behaves like Huge crossing planes.
- Search and run detection must be ring-aware, not just commit.
  A free run made of the tail of the last row plus the head of
  the first row is one run, and the allocator has to see it that
  way when deciding what fits. Largest-free must be computed
  modularly, or EXHAUST lies. If commit allows wraps but the
  probes only see linear runs, the ring benefit never
  materializes.
- Counters do not change: they count sectors, not positions.
- Determinism survives: the bound gains at most a constant
  factor. Energy: boundary blocks cost a split commit; typical
  blocks are unaffected.

## Payoff

The top of space stops being special. Under linear semantics the
final block is truncated by whatever space remains, so block
sizes are not uniform near the end. On a ring, any position can
start a block of any length up to the free space, since the block
just continues at the bottom. Wrap validity then depends on the
beginning being free, which check-then-set already handles: an
overlap is FAIL_OVERLAY, correctly.

## Tempering (his estimate)

The ring may buy only about 5% reclaim, judging by Rotate
(rolling planes) — a tempering estimate, not a measurement. The
ring only pays when the only fitting run wraps: tail free plus
head free, neither alone enough. Every other placement is
identical to linear. In the Nano domain that is a sliver: a start
in the final 7 sectors plus split free space, only at high
occupancy when alternatives are gone. At first-fit-low's stall,
580 sectors were free but the max run was 3; the binding
constraint there is fragmentation everywhere, not the boundary.
A wrap-merged run might buy one or a few more placements, not
points. Rolling planes is a fair indication of the shape of the
payoff: Rotate's circularity bought motion in bulk and cost
capacity (2.34 points). Circularity buys elegance and quiet,
not bulk capacity.

The payoff grows with block size. For Huge blocks, which span
planes, boundary-crossing is common rather than rare, so the
ring's reclaim scales up with the block. In Nano it is a sliver;
as a Large and Huge story it could be more.

## The door it opens

The ring opens the door to virtual pointer management of
non-linear memory spaces — the larger subject, esoteric by the
user's own word. Once the pointer is a representation rather
than a machine address, the space it manages does not have to
be a line. Rings, hierarchies (Beam of Cubes, Map of Beams,
Pool of Maps), distributed pools: all fall under managing
symbols over structures that are not intervals. Nearly all
allocator theory assumes a linear address space; a
representation-first pointer is the tool that does not need
that assumption. The ring is one instance; the management
theory is the subject.

## Open questions

- Anything that treats 32767 as an edge or sentinel needs
  re-examination, since a ring has no edge.
- Ring-aware probe and oracle details: how Center, Left, and
  Right report runs that cross the space boundary (tail-plus-
  head as one run).
- How the ring composes with the other driver rules (Rotate,
  sticky-start, camping) and with the 98% plane-skip proposal —
  not yet considered.
