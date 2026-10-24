from Geometry import Geometry    
from Mode     import Mode
from Status   import Status


class Nano (Mode):
    "handles request inside bytes"

    def range    (self):
        "reveal at which this __call__ is invoked"
        return self.inclusive (1, Geometry.SECTORS_PER_BYTE)

    def __call__ (self, plane, row, request, ctx, sector_out):
        "SectorChecker as a bullet, shaped by the handler call."

        # The handler call defines this shape: probe one row.
        # ctx is the sectors words array; sector_out is a
        # one-element mutable cell taking the run's start sector
        # on conviction. (The C adapter in Gears.py bridges the
        # cell to the pointer.) Acquittal returns the mode's own
        # failure code, per the C bullet contract; the gear treats
        # any non-success as "try the next row".

        # Boundary check, as in Listing 17: GlobalRow past 1023
        # fails. Out-of-domain length fails the same way: no row
        # fits it, so the gear exhausts and the mode fails.
        global_row = plane * Geometry.ARITY + row
        if not 0 <= global_row <= 1023:
            return Status.NANO_FAIL
        if request not in self.range ():
            return Status.NANO_FAIL

        s = ctx [global_row]

        # Center function, position order (MSB first): the smallest
        # pos whose mask of L clear bits finds nothing set. The
        # mask formula is the paper's: ((1 << L) - 1) << (32 - L - pos).
        for pos in range (0, 32 - request + 1):
            mask = ((1 << request) - 1) << (32 - request - pos)
            if s & mask == 0:
                sector_out [0] = 31 - pos - request + 1
                return Status.GEAR_SUCCESS

        return Status.NANO_FAIL
