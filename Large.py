from Row   import Row 
from Plane import Plane
from Mode  import Mode



class Large (Mode):
    "handles within plane"

    def range    (self):
        "reveal at which this __call__ is invoked"

        return self.inclusive (Row.SECTORS_TWEEN_ROWS + 1
                               Plane.SECTORS_PER_PLANE)

    def __call__ (self, request):
        return 0