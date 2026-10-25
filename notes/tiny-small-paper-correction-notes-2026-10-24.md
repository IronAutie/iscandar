# Tiny/Small paper-correction notes, 2026-10-24

Purpose: derivations made while specifying the Tiny and Small engine probes from the paper, kept in case the paper must be corrected. The paper itself is untouched. Status of everything below: derivation awaiting the author's confirmation or correction, except where marked as his word.

Sources: paper source main.tex: Polytope Formation sections (Tiny: Within Row; Small: Between Rows), Listing 18 (HeuristicTiny.apl), Listing 19 (HeuristicSmall.apl), Listing 37 (PairRowsDriver.apl), Listings 3/4 (OracleLeft/OracleRight.apl). Working principle (author, 2026-10-24): the sections are the source of truth for mode boundaries; the math is primary, figures are illustration only. Notation: A = 32 (row width), r = request size (the paper's L in listings is the request size; the author's L in discussion meant 32, so r/A are used here to avoid collision).

## 1. Tiny Left placement at the run's start (derivation, clarified 2026-10-25)

"Run's start" is ambiguous, and the first draft of this note used it sloppily: it gave a lowest-sector example while citing Nano, but Nano implements the opposite side. Clarified meaning below; sector coordinates throughout (sectors 0..31, sector 31 = MSB side).

Spec (settled by author plus section): Tiny r in 9..32 (mode boundary A/4 < L, minimum (A/4)+1 = 9; 8 belongs to Nano). Left pass: a run of length at least 9 (8-runs not eligible, strict separation of modes), starting anywhere in the 32-word. If the run reaches r, place the requested run. Right pass: tail run ending at sector 31; if it reaches r, place the requested run ending at sector 31 (author's rule, 2026-10-24); leftover becomes an interior gap.

Clarified Left rule (sector package):

- Scan: sectors 0 toward 31; the first (lowest-start) run of length at least 9 wins. Runs shorter than 9 are skipped, including 8-runs.
- Placement: at the run's start, meaning its lowest sectors. Block = [run_low, run_low + r - 1]; sector_out = run_low. The remainder (run length minus r) sits on the high side of the block.
- Example: run at sectors 8..17 (length 10), request 9: Left placement = sectors 8..16, sector_out 8; sector 17 stays free. Mirror: tail run 22..31 (length 10), request 9: Right placement = sectors 23..31; sector 22 stays free. So in sector terms Left takes from the low side, Right takes from the high side.

Why the sector package, and why not Nano's side:

- Nano verified (code plus run, 2026-10-25): its probe scans positions MSB-first with sector_out = 31 - pos - r + 1, taking from the MSB (high-sector) side of the run. Run 8..17, request 4 gives block 14..17; S = 0x80000000, request 4 gives block 27..30 (high side of the 0..30 run). Nano's package is position-first scan plus high-side placement: the mirror image of Tiny-Left's sector package. Citing Nano for Tiny-Left's side was wrong.
- The sector package is forced by the bimodal mechanism itself, in prose, not by the figure: under a position-first scan, Left would reveal a qualifying tail run whenever one exists (it touches sector 31, the first positions scanned), so the second bite could never succeed; Left and Right would return the same run. The stated purpose of the second bite is that it captures what Left missed, which requires Left and Right to be able to return different runs. Sector-first scan gives that: Left reveals the lowest-start qualifying run (interior A before tail B in the example), and Right then reveals the tail run.
- Placement follows the scan side: take from the side scanned from. Mixed packages (scan from one side, take from the other) have no justification.

Status: derivation, not paper text and not yet the author's word. The author asked what "run start" means; this clarified sector-package meaning is the answer awaiting his confirmation or correction.

## 2. Small return b = 32 - P (derivation, paper-correction candidate)

Small probe (Listing 19): per row pair (GR1, GR2 = GR1+1), GR1 at most 1022. P = tail run length of S1 (sectors 32-P..31 of GR1 free). Q = head run length of S2 (sectors 0..Q-1 of GR2 free). Test: if L <= P, done (dead for Small's domain, since L >= 33 > 32 >= P, by the section boundary A < L <= 2A); else M = L - P; fail iff M > Q; else place: start at S1's tail start (sector 32-P in GR1), count L, spanning P sectors of GR1 + M sectors of GR2.

Pair driver formula (Listing 37, ExecuteVector): on conviction at pair i, Result = OK((A x i) + b), where A = 32, i = pair index within the plane, and (status, b) is the checker's return.

Derivation:

- 32i + b must be the within-plane start displacement: row-major linearization, 32 sectors per row, so 32i + b = (row i, sector b) within the plane. The caller (PlanesDriver) adds the plane base for the absolute placement.
- For the result to identify the placement's start, b must be the start sector within row i. The placement starts at the tail start, sector 32 - P. Therefore b = 32 - P.
- Listing 19 writes the checker return as "OK L" (b = L, the request size, 33..64). Counterexample: pair i = 0, tail P = 10, request L = 40. True start displacement = 22 (row 0, sector 22). With b = L, the driver reports 40 = (row 1, sector 8): wrong row, wrong sector, not the block's start. In general, L in 33..64 is out of row i (sectors 0..31) and spills into row i+1 (L = 33..63) or row i+2 (L = 64, sector 0). So "OK L" is incoherent as a start displacement.
- Conclusion for a paper correction: Listing 19's return should be OK (32 - P) (the checker returns the tail start sector), keeping the driver formula. The alternative (driver formula means something else) has no sensible reading.

## Other paper-correction candidates (same fix pass, if ordered)

- Small prose cites "Listing 15 (HeuristicSectorsDriver.apl)": Listing 15 is Decision.apl; Small's code is Listing 19.
- Small L <= P branch: dead by the section boundary (L > 32 >= P); either drop it or mark it defensive.
- PairRowsDriver gate: as written, R <= Counts[i] + Counts[i+1]. The Small section's Summation Predicate counts occupied 1-bits, so Counts is occupied counts, and the gate as written reads backwards (admits full pairs). Engine form: R <= (32 - count[i]) + (32 - count[i+1]) (free sums). Confirm the APL Counts convention when correcting.
- Failure codes: APL FAIL_TINY = 5 and FAIL_SMALL = 6 collide with the engine's Gamma codes (FAIL_GAMMA_ROW = 5, FAIL_GAMMA_PLANE = 6); engine uses TINY_FAIL and SMALL_FAIL by the author's delegation (2026-10-24). Paper codes unchanged unless the paper is revised.

## Settled spec points referenced above (author's word, 2026-10-24)

- Mode boundaries from section headers: Tiny A/4 < L <= A (9..32); Small A < L <= 2A (33..64).
- Tiny run classes: word always 32 sectors; Left sequences start anywhere, length 9..32; Right sequences end at sector 31, length <= 32.
- Tiny-Right placement: requested run ending at sector 31; leftover becomes an interior gap.
- Tiny Left eligibility: runs of at least 9 (8-runs not eligible, strict separation of modes).
- Failure codes by author's delegation: TINY_FAIL, SMALL_FAIL (after NANO_FAIL).
