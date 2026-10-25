from Mode import Mode
from Cube import Cube
from Status import Status



class CubeCheck (Mode):

    "silent mode when bounds exceeded in cube"


    def range    (self):
        "reveal at which this __call__ is invoked"
        
        return self.inclusive (Cube.SECTORS_PER_CUBE,
                               Cube.SECTORS_PER_CUBE)

    def search (self, request, count_planes, count_rows, words,
                count_overall=None):
        """Whole-cube search, all in Python: no gear, no bullet.

        The only question is the overall cube count. It must
        be zero to succeed: a whole-cube block fits only in
        an empty cube. Nonzero -> GEAR_EXHAUST, with 0, 0, 0
        as placeholders, the same exhaust shape as the gears.
        Zero -> GEAR_SUCCESS, plane 0, row 0, sector 0, the
        only possible start for a 32768-sector block. The
        Engine passes its apex counter as count_overall;
        a direct call without it falls back to the sum of
        the plane counters, which is the overall count by
        the Gamma ladder. A request other than the whole
        cube is not a Cube placement, so it exhausts too."""

        if request != Cube.SECTORS_PER_CUBE:
            return Status.GEAR_EXHAUST, 0, 0, 0
        if count_overall is None:
            count_overall = sum (count_planes)
        if count_overall != 0:
            return Status.GEAR_EXHAUST, 0, 0, 0
        return Status.GEAR_SUCCESS, 0, 0, 0

    def __call__ (self, request):
        return 0
      