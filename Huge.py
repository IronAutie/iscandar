from Row   import Row 
from Plane import Plane
from Cube  import Cube
from Mode  import Mode



class Huge (Mode):
    "handles between planes within cube"

    def range    (self):
        "reveal at which this __call__ is invoked"

        return self.inclusive (Plane.SECTORS_PER_PLANE + 1,
                               Cube.SECTORS_PER_CUBE - 1)

    def __call__ (self, request):
        return 0