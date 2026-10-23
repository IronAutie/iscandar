from Geometry import Geometry
from Cube     import Cube
from Modes    import Modes
from array    import array



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
        
