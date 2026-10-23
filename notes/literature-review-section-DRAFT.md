# Literature review — DRAFT section for the paper

Drafted 2026-10-22 from the prior-art sweep (report:
research_notes/iscandar-prior-art-sweep-20261022-1244/report.md).
The oracle paragraph was completed 2026-10-22 from the second sweep
(iscandar-oracle-prior-art). Not yet inserted into any paper version.

AUTHOR'S FRAMING (user, 2026-10-22, keep verbatim in spirit): the
oracle is NOT the innovation. It is an anticipation of the buddy
system's own action, an existing O(1) engine dropped in so that
placement does not degrade the radix innovation, which is the actual
contribution and is itself O(1). The radix and its coordinates carry
the claim; the oracle carries one sentence: placement steering is held
at O(1) by an existing technique so nothing in the machinery costs
more than the design it serves.

---

## Related work

The buddy system originates with Knowlton (1965) and is treated
canonically by Knuth. Peterson and Norman (1977) survey the family and
its non-binary members: weighted buddy systems, whose split ratios
follow a series such as 2, 3, 4, 6, 8, 12; Fibonacci and generalized
Fibonacci buddies, which split a block unevenly into the two preceding
sizes; and double buddies, two interleaved binary series. Non-binary
splitting is therefore old. What the literature does not appear to
contain is a buddy system of uniform arbitrary radix, still less one
whose radix may differ per level (mixed radix); Wilson et al.'s survey
of dynamic storage allocation (1961–1995) records none.

Brent (1989) is the closest machinery to the present design: a binary
segment tree whose internal nodes hold the largest free block in their
segment, so allocation descends by the aggregates and updates them up
the path, with no free-list search. The differences are structural.
Brent's nodes store maxima for a first-fit policy over arbitrary sizes;
the present design stores occupancy counters under a mutual-agreement
invariant, performs buddy splitting, and decides coalescence by
reconciling counters along the allocation path rather than by
inspecting maxima, tags, or neighbours.

Constant-time allocation has been claimed before, on different
mechanisms. Half-Fit (Ogasawara 1995) was the first constant-time
allocator, and TLSF (Masmano et al. 2004; 2008) makes the claim
precise: a worst case known in advance and independent of application
data. TLSF is a segregated-fit allocator, not a buddy system; it
locates blocks by searching two levels of bitmaps with find-first-set
instructions, and coalesces through boundary tags. The present design
replaces that bounded search with oracle placement (Section [x]) and
states its bound as k·A for unrolled fixed-width scans, a bound in the
architecture's parameters rather than in the machine word.

Placement without search, at the price of refused placements, also
has a precedent, and the price has a name. Ogasawara's Half-Fit (1995)
"finds a free block without searching on a free list or tree,"
accepting in exchange extra unusable memory, which he calls
"incomplete memory use." TLSF inherits the stance: its authors
describe an "incomplete search policy," exhibit a case in which a
fitting block in the previous segregated list is skipped and the
request therefore fails, and explicitly reject adding an exact-search
fallback, because the worst-case response time would no longer be
bounded. The present design accepts the same bargain, stated the same
way: an oracle may refuse a placement that search would have found,
and the refusal is the price of the bound. The differences are of
keying and of bookkeeping. Half-Fit's and TLSF's decisions are keyed
by request size; the oracle here is keyed by the heap's
occupancy-counter state and returns a placement in a buddy tree. And
where incomplete memory use is fragmentation accepted into the books,
here the counters keep the books exact: oracle imperfection costs
placements, never consistency. In the learning-augmented algorithms
literature, an oracle or prediction advises an algorithm that retains
a fallback and is hardened against bad advice (Lykouris and
Vassilvitskii 2018); the stance here is the inverse: the oracle
decides, and the counters, not a fallback search, are the safeguard.
Bélády's optimal replacement (1966), formalized by Aho, Denning, and
Ullman (1971) as a function of state and the entire future reference
string, is an oracle used as a benchmark, never as a mechanism.

On addressing: in binary buddy systems each bit of an offset records
one level of the tree, and a block's buddy is its address with one bit
flipped (Wilson et al., §3.7). That addressing is the all-2s special
case of the mixed-radix coordinate scheme used here, in which a
block's position, size class, and parentage are digits of a single
mixed-radix number, read off by the encode and decode identities. No
allocator was found that uses mixed-radix coordinates as its steering
representation.

Hardware memory managers have been built before: Agun and Chang
(2003) implement a modified buddy system in reconfigurable hardware,
where combinational gate trees locate free blocks in a bitmap. The
present design differs in kind and in purpose: it is a specification
rather than an implementation, its per-level A-wide counter scans are
presented as parallel comparators for an arbitrary or mixed radix, and
its k·A bound is read as pipeline depth.

To the author's knowledge, no published allocator combines all of: a
uniform or mixed radix; mixed-radix coordinate steering; an occupancy
counter ladder with coalescence by reconciliation; oracle placement in
place of search; a worst case stated as an unrolled-scan bound; and a
reading of the design as a parallel-silicon specification. The
provenance note (Section [y]) explains why this combination could
arise independently: the 1998 design was developed without access to
any of the literature cited here.
