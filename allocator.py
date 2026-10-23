

class Geometry:
    """ Shape of the system from paper """
    ARITY      = 32
    DIMENSIONS = 3 



class Row(int):
    """A bitfield of width A."""

    WIDTH = GEOMETRY.ARITY
    MASK = (1 << WIDTH) - 1

    def __new__(cls, value=0):
        return super().__new__(cls, value & cls.MASK)

