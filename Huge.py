from Row   import Row 
from Plane import Plan
from Cube  import Cube
from Mode  import Mode



class Huge (Mode):
    "handles between planes within cube"

    def range    (self):
        "reveal at which this __call__ is invoked"

        return range (Plane.SECTORS_PER_PLANE,
                      Cube.SECTORS_PER_CUBE)

    def __call__ (self, request):
        return 0