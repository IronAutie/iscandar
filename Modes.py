
from Error    import Error
from Nothing  import Nothing
from Nano     import Nano
from Tiny     import Tiny
from Small    import Small
from Large    import Large
from Huge     import Huge
from CubeCheck import CubeCheck



class Modes (dict):
    """
    Nano: L ≤ A/4 — Center Oracle, single-pass
    Tiny: A/4 < L ≤ A — Left Oracle, then Right, dual-pass
    Small: A < L ≤ 2A — sector-join across a row boundary
    Large: 2A < L ≤ A² — row sequences welded within one plane
    Huge: A² < L < A³ — across planes, on the global row manifold
    CubeCheck A³ exactly — the gatekeeper tier; anything inadmissible fast-fails here
    """

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

        super().__init__({L: self.error   for L in self.error.range ()})
        super().__init__({L: self.nothing for L in self.nothing.range ()})
        super().__init__({L: self.nano    for L in self.nano.range ()})
        super().__init__({L: self.tiny    for L in self.tiny.range ()})
        super().__init__({L: self.small   for L in self.small.range ()})
        super().__init__({L: self.large   for L in self.large.range ()})
        super().__init__({L: self.huge    for L in self.huge.range ()})  
        super().__init__({L: self.cube    for L in self.cube.range ()})
                                                            

    def __call__   (self, request):
        return self.get (request, nothing) (request)

