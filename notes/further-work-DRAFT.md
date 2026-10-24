# Further work: the three rungs (author's framing, 2026-10-23)

Saved at the author's direction. His words, lightly arranged.

The design unfolds in three scopes, all of them the same identity
(Axiom IV) at larger scale:

1. Safe closed memory for an MPU. The k=3 engine as submitted:
   deterministic allocation inside a bounded pool, a 32-bit wrapped
   pointer because the work was written for efficient closed memory
   allocation, a life and death issue for manufacturers and
   consultants of that era. Sixty-four bits would buy address space
   the design deliberately refuses to have.

2. More efficient limited memory than the buddy system. The same
   engine as a bounded heap in its own right, against the buddy
   baseline, on determinism and flat per-operation cost.

3. Memory as a cartridge for distributed memory. Higher k is a
   separate program, accommodating higher structure: a Beam of
   Cubes, a Map of Beams, a Pool of Maps. Each level is one more
   digit in Equation 5. This opens the door to reliable distributed
   memory: across machines the bijection is a naming system, not
   just an allocator. A coordinate that every node computes
   identically by arithmetic, with no lookup service and no
   translation table, lets any node determine where a block lives
   or should be placed; the counter hierarchy aggregates occupancy
   across levels however they are physically arranged.

Scoping note (desk-check): the identity gives naming, placement and
bookkeeping. It does not give consensus; arbitration under failure
is other machinery, which this naming layer is built to sit under.

Placement: the author sees nowhere for this in the paper except as
further work. His assessment, verbatim in substance: this is the
part that is PhD worthy.
