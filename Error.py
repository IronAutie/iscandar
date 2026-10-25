from Mode import Mode
from Cube import Cube
from Status import Status



class Error (Mode):
    """ fill decision table with error handler in case'
        there are any table entries missing from fill
        by other handlers """

    def range (self):
        return range (Cube.SECTORS_PER_CUBE)

    def search (self, request, count_planes, count_rows, words,
                count_overall=None):
        """Error search: return FAIL, no sweep, no bullet.

        Error is the table-fill sentinel, for a hole in the
        decision table. A complete table never selects it.
        If it is selected, that is a table fault, so it
        fails explicitly, in the uniform search shape
        (FAIL, 0, 0, 0), and Engine returns that FAIL with
        no mark and no pointer."""

        return Status.FAIL, 0, 0, 0
