# Oracle manufacture — prep notes

Source: Iscandar_24b.pdf (the latest version the user has access to, uploaded 2026-10-22),
Appendix D "Oracle Manufacture", Listings 2-7, plus the oracle definition in the glossary
("a precomputed body of polytope seed (Center Oracle) or join (Left or Right Oracle) solutions").

Prepared by Muse as a desk-check brief. The manufacture code is the author's to write;
these notes only extract what the paper specifies.

Update (user, 2026-10-22): the APL files are to be replaced with Python.
The .apl namespaces in Listings 2-4 (Init mapping the .bin file, Resolve doing
the lookup) get Python equivalents — in Python terms, an mmap-backed table
with the same shapes: Center (2^32, 9) uint8, Left/Right (2^32, 2) uint8,
same byte order in each row, same Resolve return values. The .bin formats
below do not change; only the language of the access layer (and, if he
chooses, of the manufacture scripts in Listings 5-7) changes.

## The three bitwise files

All three are indexed by a full 32-bit occupancy state S (2^32 rows).
Bit numbering is Motorola: Bit 0 = MSB / leftmost, Bit 31 = LSB / rightmost.
A set bit = occupied, a clear bit = free.

### OracleCenter.bin — 2^32 rows x 9 bytes = 38,654,705,664 bytes (36 GiB)

- Row S, columns k = 0..8 (requested allocation length).
- k = 0 column is redundant, always byte 0.
- For k >= 1: the leftmost position pos in 0..(32-k) such that k consecutive
  bits starting at pos are all clear in S; byte = pos, or 255 (0xFF) if none.
- Mask as written in Listing 5: (2^k - 1) << (32 - k - pos); hit iff (S & mask) == 0.
- First hit wins ("closest to left" packing). APL side memory-maps it as
  (4294967296 9) Type 80 and resolves with Pos <- Data[State; Length],
  returning a bit position 0-31 or 255 for fail.

### OracleLeft.bin — 2^32 rows x 2 bytes = 8,589,934,592 bytes (8 GiB)

- Logic as written in Listing 6: the trailing run (the free run that ends at the LSB).
- If S & 1 != 0 (LSB occupied): Byte A = 255 (blocked), Byte B = 0.
- Else: Byte A = r, the length of the trailing run of clear bits counted from
  the LSB upward; Byte B = 32 - r (the run's start position, relative to MSB).
- APL side maps (4294967296 2) Type 80, Resolve returns (Length StartPos).

### OracleRight.bin — 2^32 rows x 2 bytes = 8,589,934,592 bytes (8 GiB)

- Logic as written in Listing 7: the leading run (the free run that starts at the MSB).
- If S & 0x80000000 != 0 (MSB occupied): Byte A = 255 (blocked), Byte B = 0.
- Else: Byte A = r, the length of the leading run of clear bits counted from
  the MSB downward; Byte B = 0 always.
- APL side maps (4294967296 2) Type 80, Resolve returns (Length StartPos).

Total for the set: 52 GiB on disk, memory-mapped, not loaded into RAM
(the Center listing itself notes the map is "a virtual link without consuming 38GB of RAM").

## Spot-check rows (from the formulas, for verifying a generated file)

- S = 0x00000000: Center gives pos 0 for every k = 1..8; Left gives (32, 0); Right gives (32, 0).
- S = 0xFFFFFFFF: Center gives 255 for every k = 1..8; Left gives (255, 0); Right gives (255, 0).
- S = 0x00000001: Left is blocked (255, 0); Right gives (31, 0).
- S = 0x80000000: Right is blocked (255, 0); Left gives (31, 1).

## Open desk-check items (author's call, not corrections)

1. Naming cross: Listing 6 ("Left") computes the run that ends at the right
   edge (LSB), and Listing 7 ("Right") computes the run that starts at the
   left edge (MSB). Consistent within Appendix D, but worth confirming this
   matches how the welding sections use Left/Right (LHL/RHL) before generating 52 GiB.
2. Center covers only k = 0..8. That bounds the single-pass intersection
   requests (Nano/Tiny tier); larger requests are assembled from joins.
   Worth confirming 8 is the intended ceiling before manufacture.
3. Manufacture cost: as written the PowerShell loops visit all 2^32 states
   (Center additionally scans up to 32 positions for each of 8 lengths).
   A generated-file approach wants a blockwise/vectorised pass or a
   recurrence over S, plus a heartbeat/checkpoint so a long run can resume.
4. Byte order inside a row is file order (k ascending for Center; A then B
   for Left/Right). The APL maps assume exactly that layout.
