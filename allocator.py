from array import array


class Geometry:
    """ Shape of the system from paper """
    ARITY      = 32
    DIMENSIONS = 3 

    SECTORS_PER_BYTE = ARITY // 4    


class Row(int):
    """A bitfield of width A."""

    SECTORS_PER_ROW    = Geometry.ARITY
    SECTORS_TWEEN_ROWS = 

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


"""
Nano: L ≤ A/4 — Center Oracle, single-pass
Tiny: A/4 < L ≤ A — Left Oracle, then Right, dual-pass
Small: A < L ≤ 2A — sector-join across a row boundary
Large: 2A < L ≤ A² — row sequences welded within one plane
Huge: A² < L < A³ — across planes, on the global row manifold
Cube: L = A³ exactly — the gatekeeper tier; anything inadmissible fast-fails here
"""

class Modes (dict):

    def inclusive  (self, a, b):
        """The integers a through b, both ends included."""

        return range (a, b + 1)


    def error      (self, request):
        "should never be called!"

        self.x = 0  # for breakpoints
        return 0


    def nothing    (self, request):
        return 0


    def nano       (self, request):
        return 0


    def tiny       (self, request):
        return 0


    def small      (self, request):
        return 0


    def large      (self):
        return 0


    def huge       (self, request):
        return 0


    def cube       (self, request):
        return 0


    def __init__   (self):
        """ create decision table here """

        super().__init__({L: self.error  
          for L in self.inclusive (0, Cube.SECTORS_PER_CUBE)})
        
        self [0] = self.nothing 

        super().__init__({L: self.nano    
          for L in self.inclusive (1, Geometry.SECTORS_PER_BYTE)})

        super().__init__({L: self.tiny    
          for L in self.inclusive (Geometry.SECTORS_PER_BYTE,
                                   Row.SECTORS_PER_ROW)})

        super().__init__({L: self.small    
          for L in self.inclusive (Row.SECTORS_PER_ROW,
                                   Row.SECTORS_TWEEN_ROWS)})

        super().__init__({L: self.large    
          for L in self.inclusive (Row.SECTORS_TWEEN_ROWS,
                                   Plane.SECTORS_PER_PLANE)})

        super().__init__({L: self.huge    
          for L in self.range     (Plane.SECTORS_PER_PLANE,
                                   Cube.SECTORS_PER_CUBE)})

        self [Cube.SECTORS_PER_CUBE] = self.cube


    def __call__   (self, request):
        return self.get (request, nothing) (request)



class Engine (Cube):

    def __init__ (self):
        """ initialize a Cube """

        self.count_overall = 0
        self.count_planes  = array('I', [0] * Cube.PLANES_PER_CUBE) 
        self.count_rows    = array('I', [0] * Cube.ROWS_PER_CUBE) 

        self.modes         = Modes ()


    def deallocate (self, address):
        """ stubbed """


    def __call__ (self, request):
        return self.modes (request)
        
