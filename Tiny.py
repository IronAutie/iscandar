from Geometry import Geometry
from Row      import Row
from Mode     import Mode
from Status   import Status


class Tiny (Mode):
    "handles request inside row"

    def range    (self):
        "reveal at which this __call__ is invoked"

        return self.inclusive (Geometry.SECTORS_PER_BYTE + 1,
                               Row.SECTORS_PER_ROW)

    def __call__ (self, plane, row, request, ctx, sector_out):
        "SectorChecker as a bullet, shaped by the handler call."

        # The handler call defines this shape: probe one row.
        # ctx is the sectors words array; sector_out is a
        # one-element mutable cell taking the placement's start
        # sector on conviction. The probe never marks; it only
        # reports a sector or a failure. Acquittal returns the
        # mode's own failure code, per the C bullet contract;
        # the gear treats any non-success as "try the next row".

        # Boundary check, as in Listing 18: GlobalRow past 1023
        # fails. Out-of-domain length fails the same way: no row
        # fits it, so the gear exhausts and the mode fails.
        global_row = plane * Geometry.ARITY + row
        if not 0 <= global_row <= 1023:
            return Status.TINY_FAIL
        if request not in self.range ():
            return Status.TINY_FAIL

        s = ctx [global_row]

        # Left pass (sector package): scan sectors 0 toward 31;
        # the first (lowest-start) clear run of at least 9
        # sectors wins. Runs under 9 are skipped: 8-runs are not
        # eligible, strict separation of modes (Nano owns 1..8).
        # The sentinel at 32 flushes a run ending at sector 31.
        run_start = -1
        run_len = 0
        left_run = None
        for sector in range (33):
            if sector < 32 and (s >> sector) & 1 == 0:
                if run_len == 0:
                    run_start = sector
                run_len += 1
            else:
                if run_len >= 9:
                    left_run = (run_start, run_len)
                    break
                run_len = 0
        if left_run is not None:
            start, length = left_run
            if length >= request:
                # Place at the run's start: its lowest sectors.
                # This holds even when the revealed run happens
                # to be a tail run (pass scoping: Left always
                # places low-side; only the Right pass places
                # ending at sector 31).
                sector_out [0] = start
                return Status.GEAR_SUCCESS
            # Eligible but short: second bite.

        # Right pass (second bite): tail run ending at sector 31.
        tail_len = 0
        for sector in range (31, -1, -1):
            if (s >> sector) & 1 == 0:
                tail_len += 1
            else:
                break
        if tail_len >= request:
            # Place the requested run ending at sector 31. The
            # leftover, if the tail run was longer, becomes an
            # interior gap.
            sector_out [0] = 32 - request
            return Status.GEAR_SUCCESS

        return Status.TINY_FAIL
