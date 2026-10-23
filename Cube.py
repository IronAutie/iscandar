from Geometry import Geometry
from Plane import Plane


class Cube(dict):
    """ARITY Planes, keyed by plane index."""

    PLANES_PER_CUBE    = Geometry.ARITY
    ROWS_PER_CUBE      = PLANES_PER_CUBE * Plane.ROWS_PER_PLANE
    SECTORS_PER_CUBE   = PLANES_PER_CUBE * Plane.SECTORS_PER_PLANE

    def __init__(self):
        super().__init__((i, Plane()) for i in range(Geometry.ARITY))

    def __missing__(self, i):
        plane = Plane()
        self[i] = plane
        return plane