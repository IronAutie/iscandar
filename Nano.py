from Geometry import Geometry    
from Mode     import Mode


class Nano (Mode):
    "handles request inside bytes"

    def range    (self):
        "reveal at which this __call__ is invoked"
        return self.inclusive (1, Geometry.SECTORS_PER_BYTE)})

    def __call__ (self, request):
        return 0