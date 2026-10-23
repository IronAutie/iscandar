class Row(int):
    """A bitfield of width A."""

    WIDTH = A
    MASK = (1 << A) - 1

    def __new__(cls, value=0):
        return super().__new__(cls, value & cls.MASK)

        