from Row  import Row 
from Mode import Mode



class Small (Mode):
    "handles between rows requests"

    def range    (self):
        "reveal at which this __call__ is invoked"

        return self.inclusive (Row.SECTORS_PER_ROW,
                               Row.SECTORS_TWEEN_ROWS)

    def __call__ (self, request):
        return 0