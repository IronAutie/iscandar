"""DRAFT for the author's red pen -- NOT installed in the engine.

View-backed Row / Plane / Cube: the same class names, the same
constants, the same get-modify-set call shape as the current dict
versions, but the state is one flat array('I', 1024) of row words.
That array is what C gets a pointer to; the dict classes become
views over it, not a second copy.

Installed into Cube.py/Plane.py/Row.py at the author's word
(2026-10-24); this file remains as the design record and
self-test. Row.py needed no change: it already matched the draft.

The ONE deliberate behavior change, flagged for the author:
the old dicts silently accepted out-of-range keys (a read of a
missing key returned an empty Row; a write stored a new entry and
grew the dict). The flat store is fixed at 1024 words, so
out-of-range keys raise IndexError at the view layer -- and the
engine boundary catches it and returns Status.KEYRANGE to the
caller, never a traceback (author's call, 2026-10-24). KEYRANGE
is the IndexError's own unique status, per the per-site rule.

Why the split, and why not return the failure from __getitem__
itself: a failure code handed back as a row word would read as
occupancy data (Row(1) looks like a set bit). Detection stays sharp
at the view; reporting becomes a status at the boundary, matching
the gears' existing (status, plane, row, sector) vocabulary.

Doctrine (author, 2026-10-24): soft assertions. A failure at any
level returns a status, never crashes, and is never tolerated or
papered over -- it is debugger time, terminal for that operation.
Nothing in the engine uses out-of-range keys today (checked
2026-10-24); every valid key 0..31 behaves as before.
"""

import os
import sys
from array import array

# Engine folder = parent of this file's folder (notes/ lives inside
# it), so this draft runs from any checkout, not just one machine.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Geometry import Geometry
from Status import Status


class Row(int):
    """A bitfield of width A. Unchanged from the current Row.py."""

    SECTORS_PER_ROW = Geometry.ARITY
    SECTORS_TWEEN_ROWS = 2 * SECTORS_PER_ROW

    WIDTH = Geometry.ARITY
    MASK = (1 << WIDTH) - 1

    def __new__(cls, value=0):
        return super().__new__(cls, value & cls.MASK)


class Plane:
    """A view over 32 consecutive row words of the flat cube store."""

    ROWS_PER_PLANE = Geometry.ARITY
    SECTORS_PER_PLANE = ROWS_PER_PLANE * Row.SECTORS_PER_ROW

    def __init__(self, words, plane=0):
        self._words = words
        self._base = plane * Geometry.ARITY

    def _check(self, i):
        if not 0 <= i < Geometry.ARITY:
            raise IndexError(f"row index out of range: {i!r}")

    def __getitem__(self, i):
        self._check(i)
        return Row(self._words[self._base + i])

    def __setitem__(self, i, value):
        self._check(i)
        self._words[self._base + i] = Row(value)

    def __len__(self):
        return Geometry.ARITY

    def __iter__(self):
        return iter(range(Geometry.ARITY))

    def __contains__(self, i):
        return isinstance(i, int) and 0 <= i < Geometry.ARITY

    def get(self, i, default=None):
        return self[i] if i in self else default

    def keys(self):
        return list(range(Geometry.ARITY))

    def values(self):
        return [self[i] for i in range(Geometry.ARITY)]

    def items(self):
        return [(i, self[i]) for i in range(Geometry.ARITY)]


class Cube:
    """A view over the whole flat store: 32 planes x 32 rows."""

    PLANES_PER_CUBE = Geometry.ARITY
    ROWS_PER_CUBE = PLANES_PER_CUBE * Plane.ROWS_PER_PLANE
    SECTORS_PER_CUBE = PLANES_PER_CUBE * Plane.SECTORS_PER_PLANE

    def __init__(self, words=None):
        # The backing store. Hand this array's buffer to C; the views
        # above read and write exactly these words, nothing else.
        self.words = words if words is not None else array("I", [0]) * 1024

    @property
    def sectors(self):
        """The author's name for the store: the sectors array.

        Same object as .words, not a copy: 1024 unsigned 32-bit
        row words, index plane * 32 + row, each word holding one
        row's 32 sector bits. Hand its buffer to C.
        """
        return self.words

    def _check(self, p):
        if not 0 <= p < Geometry.ARITY:
            raise IndexError(f"plane index out of range: {p!r}")

    def __getitem__(self, p):
        self._check(p)
        return Plane(self.words, p)

    def __setitem__(self, p, plane):
        # Whole-plane assignment: copy 32 row values in, masked.
        self._check(p)
        rows = list(plane) if isinstance(plane, Plane) else list(plane)
        if len(rows) != Geometry.ARITY:
            raise ValueError("a plane assignment needs 32 row values")
        base = p * Geometry.ARITY
        for i, value in enumerate(rows):
            self.words[base + i] = Row(value)

    def __len__(self):
        return Geometry.ARITY

    def __iter__(self):
        return iter(range(Geometry.ARITY))

    def __contains__(self, p):
        return isinstance(p, int) and 0 <= p < Geometry.ARITY

    def get(self, p, default=None):
        return self[p] if p in self else default

    def keys(self):
        return list(range(Geometry.ARITY))

    def values(self):
        return [self[p] for p in range(Geometry.ARITY)]

    def items(self):
        return [(p, self[p]) for p in range(Geometry.ARITY)]


def guarded(fn):
    """Engine-boundary wrapper: run fn; an out-of-range index
    becomes Status.KEYRANGE for the caller, never a traceback.

    This is where Engine.__call__ and Engine.deallocate would wrap
    their marking/unmarking work: the views raise (detection), the
    boundary converts (reporting).
    """
    try:
        return fn()
    except IndexError:
        return Status.KEYRANGE


# Engine integration sketch (not code, author's call):
#   class Engine(Cube):
#       def __init__(self):
#           super().__init__(array("I", [0]) * 1024)  # words store
#           self.count_planes = array("I", [0]) * Cube.PLANES_PER_CUBE
#           self.count_rows = array("I", [0]) * Cube.ROWS_PER_CUBE
#           ... counters unchanged, modes unchanged ...
#       def __call__(self, request):
#           ... guarded(lambda: <marking work>) ...
#       def deallocate(self, pointer):
#           ... guarded(lambda: <unmarking work>) ...
# Gears then takes self.words' buffer pointer the same way it
# already takes the counter buffers.


if __name__ == "__main__":
    # Self-test: view/flat equivalence, masking, dict-like surface.
    c = Cube()
    assert Cube.PLANES_PER_CUBE == 32
    assert Cube.ROWS_PER_CUBE == 1024
    assert Cube.SECTORS_PER_CUBE == 32768
    assert Plane.SECTORS_PER_PLANE == 1024
    assert Row.SECTORS_PER_ROW == 32

    # Mark through the view, read the flat array.
    c[3][7] = 0b101
    assert c.words[3 * 32 + 7] == 0b101

    # Mark through the flat array, read through the view.
    c.words[5 * 32 + 0] = 0x80000000
    assert c[5][0] == 0x80000000

    # Get-modify-set, the shape existing code already uses.
    c[3][7] = c[3][7] | 0b1000
    assert c[3][7] == 0b1101 and c.words[3 * 32 + 7] == 0b1101

    # Masking on write, as the old Plane.__setitem__ did via Row().
    c[1][2] = 0x1FFFFFFFF
    assert c[1][2] == 0xFFFFFFFF

    # Two views of one plane see each other's writes (aliasing is
    # the point: there is only one store).
    assert c[3][7] == c[3][7]
    c[3][7] = 0
    assert c.words[3 * 32 + 7] == 0

    # Dict-like surface.
    assert len(c) == 32 and len(c[0]) == 32
    assert list(c) == list(range(32)) and list(c[0]) == list(range(32))
    assert 31 in c and 32 not in c and 0 in c[0]
    assert c.get(31) is not None and c.get(32) is None
    assert c[0].get(5) == 0
    assert len(c.keys()) == 32 and len(c[0].items()) == 32

    # Whole-plane assignment.
    c[9] = [1] * 32
    assert all(c.words[9 * 32 + i] == 1 for i in range(32))

    # Out-of-range keys raise at the view layer (detection)...
    for bad in (lambda: c[32], lambda: c[0][32], lambda: c.__setitem__(32, [0] * 32)):
        try:
            bad()
        except IndexError:
            pass
        else:
            raise AssertionError("out-of-range key did not raise")

    # ...and become Status.KEYRANGE at the guarded boundary
    # (reporting), never a traceback escaping to the caller.
    assert guarded(lambda: c[32]) == Status.KEYRANGE
    assert guarded(lambda: c[0][32]) == Status.KEYRANGE
    assert guarded(lambda: c.__setitem__(32, [0] * 32)) == Status.KEYRANGE
    assert guarded(lambda: c[3][7]) == c[3][7]  # valid access unaffected
    assert Status.FAIL == 1 and Status.KEYRANGE == 3

    # The store is one flat C-sized buffer: 1024 x 4 bytes.
    assert len(c.words) == 1024 and c.words.itemsize == 4

    # The sectors array, under the author's name, exposed to C.
    # Same object, not a copy; the pointer below is exactly the
    # mechanism Gears._u32 already uses for the counters.
    import ctypes
    assert c.sectors is c.words
    assert len(c.sectors) == 1024 and c.sectors.itemsize == 4
    ptr = ctypes.cast(c.sectors.buffer_info()[0],
                      ctypes.POINTER(ctypes.c_uint32))
    ptr[3 * 32 + 7] = 0xDEADBEEF  # write from the "C side"
    assert c[3][7] == 0xDEADBEEF   # visible through the Python view
    c[3][7] = 0x12345678           # write from the Python side
    assert ptr[3 * 32 + 7] == 0x12345678  # visible through the pointer

    print("draft-flat-views self-test: ALL OK")
