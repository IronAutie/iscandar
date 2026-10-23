from Geometry import Geometry    
from Mode     import Mode


class Nano (Mode):
    "handles request inside row"

    def range    (self):
        "reveal at which this __call__ is invoked"

        return self.inclusive (Geometry.SECTORS_PER_BYTE,
                               Row.SECTORS_PER_ROW)})

    def __call__ (self, request):
        return 0