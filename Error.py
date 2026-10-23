from Mode import Mode
from Cube import Cube



class Error (Mode):
    """ fill decision table with error handler in case'
        there are any table entries missing from fill
        by other handlers """

    def range (self):
        return self.inclusive (0, Cube.SECTORS_PER_CUBE)
