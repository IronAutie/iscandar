from Geometry import Geometry
from Cube     import Cube
from Mode     import Mode
from array    import array

from Error    import Error
from Nothing  import Nothing



"""
Nano: L ≤ A/4 — Center Oracle, single-pass
Tiny: A/4 < L ≤ A — Left Oracle, then Right, dual-pass
Small: A < L ≤ 2A — sector-join across a row boundary
Large: 2A < L ≤ A² — row sequences welded within one plane
Huge: A² < L < A³ — across planes, on the global row manifold
Cube: L = A³ exactly — the gatekeeper tier; anything inadmissible fast-fails here
"""


class Modes (dict):

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

        self.error   = Error ()
        self.nothing = Nothing ()

        super().__init__({L: self.error   for L in self.range ()})
        super().__init__({L: self.nothing for L in self.range ()})

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
        
