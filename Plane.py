from Geometry import Geometry
from Row import Row



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
