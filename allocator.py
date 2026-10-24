from Coordinate import Coordinate
from MPUPointer import MPUPointer

from Geometry   import Geometry
from Cube       import Cube
from Modes      import Modes
from Status     import Status

from array      import array



class Engine (Cube):

    def __init__ (self):
        """ initialize a Cube """

        super().__init__()  # allocate the flat sectors store

        self.count_overall = 0
        self.count_planes  = array('I', [0] * Cube.PLANES_PER_CUBE) 
        self.count_rows    = array('I', [0] * Cube.ROWS_PER_CUBE) 

        self.modes         = Modes ()


    def deallocate (self, address):
        """ stubbed """


    def mark (self, pointer):
        """ Mark the block a pointer names, through the C marker.

        The pointer is in start-with-length format: pointer.start
        is the first sector, pointer.count the true length (both
        Motorola order, the pointer's default). The C marker owns
        the sectors array and the row and plane counters; the
        overall counter is a single add, done here on success.
        A block running past the end of the cube never reaches C:
        it returns Status.FAIL at this boundary instead.
        """

        from Gears import mark_sectors  # local: the DLL is only
                                        # needed when marking

        start = pointer.start
        count = pointer.count
        if start + count > Cube.SECTORS_PER_CUBE:
            return Status.FAIL

        status = mark_sectors (self.sectors, self.count_rows,
                               self.count_planes, start, count)
        if status == Status.GEAR_SUCCESS:
            self.count_overall += count
        return status


    def unmark (self, pointer):
        """ Unmark the block a pointer names, through the C unmarker.

        Mirror of mark: same pointer format, same boundary guard,
        same overall-counter bookkeeping in the other direction.
        """

        from Gears import unmark_sectors  # local: DLL only on use

        start = pointer.start
        count = pointer.count
        if start + count > Cube.SECTORS_PER_CUBE:
            return Status.FAIL

        status = unmark_sectors (self.sectors, self.count_rows,
                                 self.count_planes, start, count)
        if status == Status.GEAR_SUCCESS:
            self.count_overall -= count
        return status


    def __call__ (self, request):
        result = self.modes (request)

        if isinstance (result, Coordinate):
            return MPUPointer.load_coordinate (result, request)

        return result
        
