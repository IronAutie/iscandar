from Geometry import Geometry

class Row(int):
    """A bitfield of width A."""

    SECTORS_PER_ROW    = Geometry.ARITY
    SECTORS_TWEEN_ROWS = 2 * SECTORS_PER_ROW

    WIDTH = Geometry.ARITY
    MASK = (1 << WIDTH) - 1

    def __new__(cls, value=0):
        return super().__new__(cls, value & cls.MASK)