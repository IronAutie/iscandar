# Reconcile, 2026-10-23 evening: Muse's Oct 23 classes vs. the CIC factored push

His push (remote tip `69751ef`, "add Gears.py ctypes bridge") is canonical.
Nothing was deleted in the reconcile. Muse's Oct 23 work survives in two
places regardless of what follows: local branch `muse-oct23-classes`
(commit `bd902db`) and `~/workspace/iscandar/backup-20261023-pre-reconcile/`.

## Mapping: my Oct 23 classes -> his factored files

- `Address` -> `Coordinate.py`: same fields, same `displacement`
  (Axiom IV, Eq. 6), same `__eq__`/`__hash__`/`__repr__`. Covered, no loss.
- `Bijection.to_sector` / `to_address` -> `Bijection.to_coordinate` /
  `to_displacement`: same divmod math, renamed. Covered, no loss.
  Verified here: round-trip over all 32,768 coordinates passes, and
  `Coordinate(5,2,1).displacement` is still 1093.
- `Pointer` -> `MPUPointer.py`: superseded AND extended, with two
  deliberate semantic changes that are his design, not losses:
  1. Count is stored shifted (stored = count - 1), so the whole cube
     32,768 is representable. My old `length` was direct (max 32,767).
     Hence my old `wrap(1093, 7, virtual=1) = 0x82228007` is now
     `load_coordinate(Coordinate(5,2,1), 7) = 0x82228006`. Same block,
     new encoding; `unload()` returns the true count 7.
  2. Born-virtual: `load` always raises the V flag; there is no
     virtual=0 creation path, by his consistency rule. My old `wrap`
     allowed virtual=0. Do NOT reintroduce it.
  3. New: Motorola/Intel decode-order switch (`order` argument), a
     code-level bench switch, never a bit in the word.
- Old Oct 22 desk-check findings: resolved by his rewrite. `Modes.__call__`
  now falls back to `self.nothing` (no bare `nothing` NameError), and
  `Engine` composes `Cube` plus a `Modes` instance instead of inheriting
  both dicts into one key space.

## The one piece his tree does NOT cover (preserved here, placement his call)

My old `Pointer.address`: the machine-side byte address the pointer
bridges to, from the deployment parameter `Geometry.BYTES_PER_SECTOR = 4`
(dropped in his `Geometry.py`, which instead has `SECTORS_PER_BYTE = 8`):

    address = start * BYTES_PER_SECTOR | (is_virtual << 31)

with `start` from the word and `is_virtual` its V bit. Nothing else of
mine is uncovered. Where this bridge lives (a property on `MPUPointer`,
a helper, or nowhere) is the author's decision.

## Notes restored

His push carries a tracked `notes/` (independence note, literature
review, oracle manufacture notes). The three untracked Oct 23 background
notes (driver doctrine, further-work draft, nano source map) were
restored alongside them, untracked, as they were.

## Verification on this reconcile (desk-check only)

His tree imports and runs once `bitstruct` is present (new dependency
from `MPUPointer.py`; this VM needed a throwaway venv install, his CIC
evidently already has it). Bijection round-trip 32,768: pass.
`MPUPointer.load(0, 32768)` = `0x80007fff`, count 32,768. Mode classes
are still stubs returning 0 at this tip, so `Engine()(5)` returns 0.

## Status

Everything above is UNCOMMITTED in the local working tree, for the
author's review and commit. Nothing was pushed.
