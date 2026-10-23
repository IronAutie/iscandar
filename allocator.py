from array import array


class Geometry:
    """ Shape of the system from paper """
    ARITY      = 32
    DIMENSIONS = 3 



class Row(int):
    """A bitfield of width A."""

    SECTORS_PER_ROW = Geometry.ARITY

    WIDTH = Geometry.ARITY
    MASK = (1 << WIDTH) - 1

    def __new__(cls, value=0):
        return super().__new__(cls, value & cls.MASK)



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



class Modes (dict):

    def nothing    (self):
        return 0

    def nano       (self):
        return 0

    def tiny       (self):
        return 0

    def small      (self):
        return 0

    def large      (self):
        return 0

    def huge       (self):
        return 0

    def cube       (self):
        return 0

    def __init__   (self):
        """ create decision table here """

        super().__init__({L: self.nothing for L in range(0, 0)})
        super().__init__({L: self.nano    for L in range(1, 4)})


    def __call__   (self, request):
        return self.get (request, nothing) (request)



class Engine (Cube, Modes):

    def __init__ (self):
        """ initialize a Cube """
        self.count_overall = 0
        self.count_planes  = array('I', [0] * Cube.PLANES_PER_CUBE) 
        self.count_rows    = array('I', [0] * Cube.ROWS_PER_CUBE) 


    def deallocate (self, address):
        """ stubbed """


    def __call__ (self, request):
        return Modes.__call__ (self, request)
        
