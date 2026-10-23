from Mode import Mode
from Cube import Cube



class CubeCheck (Mode):

    "silent mode when bounds exceeded in cube"


    def range    (self):
        "reveal at which this __call__ is invoked"
        
        return self.inclusive (Cube.SECTORS_PER_CUBE - 1,
                               Cube.SECTORS_PER_CUBE - 1)

    def __call__ (self, request):
        return 0
      