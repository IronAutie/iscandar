# Testing design (user notes, 2026-10-24)

Scope: Nano range only for now, requests 1 to 8 sectors. Tiny, Small,
Large, and Huge are still stubs; their ranges join the comparison later.

## Baseline and arena

Baseline: plain binary buddy, the classic one. Same arena for both
allocators: 32,768 sectors, 16 bytes each, 512 KiB total.

## Metric

Occupancy as percent of memory capacity, as a fair assessment of system
stability. Occupied sectors divided by 32,768, tracked after every
allocation and free, both allocators fed the identical request stream.

Report both occupancies, because the gap between them is the story:
logical occupancy (what was actually asked for) and physical occupancy
(what the allocator actually consumed). Iscandar places exactly, so for
it the two are the same. Buddy rounds a 5-sector request up to 8, so its
physical occupancy runs higher than its logical occupancy, and the gap
is its internal fragmentation, measured, not hidden.

Supporting numbers: largest free block (or run), first-failure point,
and reuse distance (operations between a free and the reuse of those
same sectors).

## Trace

Seeded, identical for both allocators. Allocations are referenced by ID,
not by raw pointer, because the two allocators place the same request at
different addresses: allocate size 5 as ID 7, later free ID 7, and each
allocator maps the ID to its own pointer. Then both get the identical
alloc and free order.

Churn: deallocate random live pointers. Sequential frees are too kind;
they let buddy coalesce neatly and hide fragmentation. Random frees are
what fragments a real system. Drive occupancy up to a target level, then
churn it there with random frees, and also drive it to failure.

## Thesis: instant memory reuse within limits

The real effect of Iscandar will be instant memory reuse within limits.
The moment a block is freed, its sectors are placeable again on the very
next fitting allocation. No coalescing pass, no waiting for neighbors to
merge, no search through a tree to rediscover the space. The counters
are updated at free time, so the next search sees the freed run
immediately, in one probe, and takes it.

Limits, stated honestly: the request has to fit the mode's range (Nano
1 to 8 for now); there has to be remaining capacity overall (the apex
gate); and for Nano the freed run has to sit inside a single row, since
that is the Nano placement shape. Inside those limits, reuse is
immediate. Outside them, it is the next mode's job or a genuine failure,
not a delay.

For Iscandar, reuse distance should be one, whenever a fitting request
follows a free. For buddy it stretches, and under churn it stretches
until failure.

## Report spine: start with the graph

Lead with the color stress graph, a timeline colored by state: green
while buddy is placing freely, yellow as stress builds, red as it nears
the edge, then a hard failure mark where its first allocation fails.
Iscandar's line runs alongside on the same timeline.

The comparison graphs hang off buddy's transitions instead of standing
alone. At the op where buddy turns yellow, a snapshot: both occupancies,
both largest free blocks, both maps. Same again at red, and again at
failure, with Iscandar's state at that same op shown next to buddy's.

Color bands, first calibration, tunable after the first real trace, not
engine facts: green below 70 percent, yellow 70 to 90, red above 90,
failure as its own marker.

## Views

Iscandar: 32 plane strips colored by plane occupancy percent, with a
per-plane sector map (32 rows by 32 sectors, 1,024 cells) as a drill-down
for any plane. The map shows placement against spec, overlays, and
fragmentation; it is the check that catches the benign mirror error,
which GammaCheck cannot see.

Buddy: no planes, only the tree, so do not force planes onto it. Its
spatial view is the tree flattened into one long bar, segmented into its
current blocks (sizes 1, 2, 4, 8, up to 32,768; tree depth 15 for this
arena), colored free or occupied. A healthy buddy shows long free
segments; a stressed one shows a choppy bar of small alternating pieces.

Optional aligned view: slice buddy's linear bar into 32 display bands of
1,024 sectors each and color each band by occupancy, so it can sit next
to Iscandar's 32 plane strips. Label it honestly as display only: those
bands are not buddy structure, just a ruler laid over its arena.

Shared headline for both, needing no planes at all: overall occupancy
percent over time, logical versus physical, largest free, first
failure.

## Claim sharpness (for publication, not for the design)

The universal form ("no other allocator can promise instant reuse")
needs narrowing before a referee sees it. Free-list allocators and
TLSF-style segregated-fit allocators also reuse a freed block on the
next fitting request, in their own narrower sense. What is distinctive
here, and what the comparison demonstrates, is the combination, all at
once, under churn: instant reuse with exact fit, bounded deterministic
cost, and no coalescing pass. Buddy cannot promise that combination;
that is the comparison that holds.
