

class Geometry:
    """ Shape of the system from paper """
    ARITY      = 32
    DIMENSIONS = 3 



class Row(int):
    """A bitfield of width A."""

    WIDTH = Geometry.ARITY
    MASK = (1 << WIDTH) - 1

    def __new__(cls, value=0):
        return super().__new__(cls, value & cls.MASK)


class Plane(dict):
    """ARITY Rows, keyed by row index."""

    def __init__(self):
        super().__init__((i, Row()) for i in range(Geometry.ARITY))

    def __missing__(self, i):
        return Row()

