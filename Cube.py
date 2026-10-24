from array import array

from Geometry import Geometry
from Plane import Plane
from Row import Row



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
