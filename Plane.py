from Geometry import Geometry
from Row import Row


class Plane(dict):
    """ARITY Rows, keyed by row index."""

    ROWS_PER_PLANE    = Geometry.ARITY
    SECTORS_PER_PLANE = ROWS_PER_PLANE * Row.SECTORS_PER_ROW


    def __init__(self):
        super().__init__((i, Row()) for i in range(Geometry.ARITY))

    def __missing__(self, i):
        return Row()

    def __setitem__(self, i, value):
        super().__setitem__(i, Row(value))