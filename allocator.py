from Geometry import Geometry
from Cube     import Cube
from Mode     import Mode
from array    import array



"""
Nano: L ≤ A/4 — Center Oracle, single-pass
Tiny: A/4 < L ≤ A — Left Oracle, then Right, dual-pass
Small: A < L ≤ 2A — sector-join across a row boundary
Large: 2A < L ≤ A² — row sequences welded within one plane
Huge: A² < L < A³ — across planes, on the global row manifold
CubeCheck A³ exactly — the gatekeeper tier; anything inadmissible fast-fails here
"""
from Error    import Error
from Nothing  import Nothing
from Nano     import Nano
from Tiny     import Tiny
from Small    import Small
from Large    import Large
from Huge     import Huge
from CubeCheck import CubeCheck



class Modes (dict):

    def __init__   (self):
        """ create decision table here """

        self.error   = Error     ()
        self.nothing = Nothing   ()
        self.nano    = Nano      ()
        self.tiny    = Tiny      ()
        self.small   = Small     ()
        self.large   = Large     ()
        self.huge    = Huge      ()
        self.cube    = CubeCheck ()

        super().__init__({L: self.error   for L in self.range ()})
        super().__init__({L: self.nothing for L in self.range ()})
        super().__init__({L: self.nano    for L in self.range ()})
        super().__init__({L: self.tiny    for L in self.range ()})
        super().__init__({L: self.small   for L in self.range ()})
        super().__init__({L: self.large   for L in self.range ()})
        super().__init__({L: self.huge    for L in self.range ()})  
        super().__init__({L: self.cubecheck for L in self.range ()})
                                                            

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
        
