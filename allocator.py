from Coordinate import Coordinate
from MPUPointer import MPUPointer

from Geometry   import Geometry
from Cube       import Cube
from Modes      import Modes
from Plane      import Plane
from Row        import Row
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
        """ Allocate a block: gate, select, search, mark, return. """

        # Step 1: overall admissibility gate. The overall counter
        # is the apex register; a request larger than what remains
        # rejects here, with no mode dispatch and no sweep.
        remaining = Cube.SECTORS_PER_CUBE - self.count_overall
        if request > remaining:
            return Status.FAIL

        # Step 2: select the mode by request size. The decision
        # table is the diagnostic choke point: a hole in the ranges
        # surfaces as Error selected, an out-of-table request as
        # Nothing.
        mode = self.modes.get (request, self.modes.nothing)

        # Step 3: the mode's search, through the C gears. A success
        # carries plane, row, and the start sector relative to the
        # row found; any other status is the search's failure.
        status, plane, row, sector = mode.search (
            request, self.count_planes, self.count_rows, self.sectors)

        # Step 4: if failure, return it. The gear's exhaust is
        # unique -- GEAR_EXHAUST means the whole cube, no placement
        # -- so the search's own status is the failure returned.
        if status != Status.GEAR_SUCCESS:
            return status

        # Gates 2 and 1, explicit, as post-search verification:
        # the gears gate again internally, but Engine checks the
        # found placement against the counters itself. A probe
        # success implies room in the found row and plane when
        # the counters are exact, so a failure here is a
        # counter/probe inconsistency -- a fault, not a placement
        # to trust. (Pre-search steering gates were set aside:
        # they would cost a full counter scan per allocation,
        # while the doomed search they skip is itself bounded;
        # this O(1) check catches the same inconsistencies. A
        # per-site gate code can replace generic FAIL here when
        # one is named.)
        if (Plane.SECTORS_PER_PLANE - self.count_planes [plane]
                < request
                or Row.SECTORS_PER_ROW
                - self.count_rows [plane * Row.SECTORS_PER_ROW + row]
                < request):
            return Status.FAIL

        # The search succeeded: the Coordinate, fields kept
        # separate -- the sector is relative to the row found,
        # never folded with the row offset, never the position.
        coordinate = Coordinate (sector, row, plane)

        # Step 5: construct the pointer from the Coordinate, born
        # so it can first be passed to mark.
        pointer = MPUPointer.load_coordinate (coordinate, request)

        # Step 6: mark first. A failed mark cannot return the
        # pointer, so the mark status propagates the same way.
        # (mark returns the C status: GEAR_SUCCESS on success.)
        status = self.mark (pointer)
        if status != Status.GEAR_SUCCESS:
            return status

        # Step 7: return the pointer. The return contract: an
        # MPUPointer or a failure, nothing else.
        return pointer
