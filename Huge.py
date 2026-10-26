from Geometry import Geometry
from Row      import Row
from Plane    import Plane
from Cube     import Cube
from Mode     import Mode
from Status   import Status

from Large    import _leading_run, _trailing_run


class Huge(Mode):
    """Huge: A^2 < L <= A^3 - 1, 1025 to 32767 sectors.

    Rederived from requirements, 2026-10-26 blackboard
    (huge-blackboard-2026-10-26.md, 53 facts), not ported
    from any APL listing. In outline, in the blackboard's
    own order:

    1. Pieced together similarly to Large, but at scale.
       Based on the request, calculate the core planes
       first, then the leading and trailing plane:
       core = request div arity squared (arity squared
       is one plane of sectors); remaining = request mod
       arity squared.
    2. Plane driver: once the number of core planes is
       known, check each plane in turn to determine if
       it and its followers have zero count. When one
       does, we have a candidate (its first core plane).
       If the candidate is at index 0 there is no head
       plane and the no leading handler fires. If the
       final plane of the candidate sequence is at index
       31 there is no trailer and the no trailing handler
       fires. Else the normal huge row handler fires.
       Each of these could return a coordinate; failing
       that, advance to the next originating plane.
    3. The core formula never makes 32 in Huge, because
       Cube.search() handles the whole cube separately.
    4. Oracle naming, pinned down 2026-10-26: a leading
       series starts at position zero (sector 0) and is
       checked with the Left oracle; a trailing series
       ends at sector 31 and is checked with the Right
       oracle. A leading series can start in mid row and
       a trailing series can end in mid row, in Large
       and in Huge alike.
    5. Named failures are specific, for breakpointing.
       They are returned inside the handlers below, one
       return line per name in this file; the plane
       driver treats any of them as this candidate's
       acquittal and advances, and search reports
       GEAR_EXHAUST when no candidate in the cube fits.
    """

    def range(self):
        "reveal at which this __call__ is invoked"

        return self.inclusive(Plane.SECTORS_PER_PLANE + 1,
                              Cube.SECTORS_PER_CUBE - 1)

    # -- row-level helpers, shared by the three handlers --

    def _lead_check_step(self, pointer, count_rows):
        """One step of the lead analysis unrolled sequence.

        The pointer has already been decremented by the
        caller. Verify the row count at it is zero: the
        blackboard's no trailing failure when it is not,
        success to continue when it is.
        """
        if count_rows[pointer] != 0:
            return Status.HUGE_NO_TRAILER_ROW_FAIL
        return Status.GEAR_SUCCESS

    def _trailing_row_body(self, pointer, count_rows):
        """One call of the normal driver's trailing body.

        Check the row count is zero: the blackboard's
        huge row driver trailing row failure when it is
        not, named for breakpointing.
        """
        if count_rows[pointer] != 0:
            return Status.HUGE_ROW_DRIVER_TRAILING_ROW_FAIL
        return Status.GEAR_SUCCESS

    def _span_free(self, start, request, words):
        """Sector-exact recheck of a proposed span.

        The handlers certify a span by construction; this
        is the same kind of recheck the Large probe does
        of the core, carried to the whole span, so a start
        is never returned on a handler's arithmetic alone.
        Returns True only when every sector is free.
        """
        end = start + request
        if start < 0 or end > Cube.SECTORS_PER_CUBE:
            return False
        first_row = start // Geometry.ARITY
        last_row = (end - 1) // Geometry.ARITY
        for g in range(first_row, last_row + 1):
            word = words[g]
            if word == 0:
                continue
            lo = start - g * Geometry.ARITY if g == first_row else 0
            hi = (end - g * Geometry.ARITY - 1
                  if g == last_row else Geometry.ARITY - 1)
            for sector in range(lo, hi + 1):
                if (word >> sector) & 1:
                    return False
        return True

    # -- the three row handlers --
    #
    # Each takes the candidate's first core plane and
    # returns (status, start) where start is a global
    # sector index on GEAR_SUCCESS, else None.

    def _rows_no_leading(self, candidate, request,
                         count_planes, count_rows, words):
        """Huge row handler no leading (facts 15 to 24).

        What remains is the request minus the sum of
        sectors in the core planes. The remainder lives
        in the plane following: trailing rows first, then
        one oracle row.
        """
        core = request // (Geometry.ARITY * Geometry.ARITY)
        remaining = request - core * Plane.SECTORS_PER_PLANE
        if remaining == 0:
            return (Status.GEAR_SUCCESS,
                    candidate * Plane.SECTORS_PER_PLANE)
        following = candidate + core
        if following >= Cube.PLANES_PER_CUBE:
            return Status.HUGE_FAIL, None
        # Gate: if the plane following cannot satisfy the
        # request (the remaining), this named gate fails.
        if (Plane.SECTORS_PER_PLANE - count_planes[following]
                < remaining):
            return Status.HUGE_GATE_TRAILING_PLANE_GATE_FAIL, None
        # Rows: pointer at the start of the plane
        # following, advanced as an unrolled loop in C;
        # every required full row must have a zero count.
        trailing_rows = remaining // Geometry.ARITY
        base = following * Geometry.ARITY
        for step in range(trailing_rows):
            if count_rows[base + step] != 0:
                return Status.HUGE_TRAILING_ROW_GATE_FAIL, None
        remaining = remaining % Geometry.ARITY
        # Oracle: the following row must consult the Left
        # oracle for a leading series fitting the rest.
        if remaining:
            row = base + trailing_rows
            if (row >= Cube.ROWS_PER_CUBE
                    or _leading_run(words[row]) < remaining):
                return Status.HUGE_NO_LEAD_TRAILER_FAIL, None
        return (Status.GEAR_SUCCESS,
                candidate * Plane.SECTORS_PER_PLANE)

    def _rows_no_trailing(self, candidate, request,
                          count_planes, count_rows, words):
        """Huge no trailer row driver (facts 25 to 36).

        Works backwards: the plane number and the request
        were passed in, and by the time we enter, the core
        planes are known empty, so the remainder lives in
        the single plane before the core, reversed into.
        It reverses by a plane's worth at most: lead
        padding rows, then one candidate row.
        """
        core = request // (Geometry.ARITY * Geometry.ARITY)
        remaining = request % (Geometry.ARITY * Geometry.ARITY)
        if remaining == 0:
            return (Status.GEAR_SUCCESS,
                    candidate * Plane.SECTORS_PER_PLANE)
        lead_rows = remaining // Geometry.ARITY
        lead_sectors = remaining % Geometry.ARITY
        # Core rows base pointer: the row counter for the
        # initial row of the initial core plane, decremented
        # one per step of the unrolled checking sequence.
        pointer = candidate * Geometry.ARITY
        for step in range(lead_rows):
            pointer -= 1
            status = self._lead_check_step(pointer, count_rows)
            if status != Status.GEAR_SUCCESS:
                return (status, None)
        if lead_sectors:
            # One more decrement: we are now pointing at
            # candidate sectors. That row's free run at
            # its end -- the arithmetic mirror of the
            # Left oracle consultation named in the
            # blackboard: arity minus the run's initial
            # sector position is what the row can give --
            # must cover the leading sectors still owed.
            pointer -= 1
            if (pointer < 0
                    or _trailing_run(words[pointer])
                    < lead_sectors):
                return (Status.HUGE_FAIL, None)
        return (Status.GEAR_SUCCESS,
                candidate * Plane.SECTORS_PER_PLANE - remaining)

    def _rows_normal(self, candidate, request,
                     count_planes, count_rows, words):
        """Normal huge rows driver (facts 37 to 53).

        Copied from both special cases. Leader first: the
        remainder is split -- the leading plane gives
        what its free suffix has, and the trailing plane
        fulfils the rest, mandatorily. In rows and
        sectors: padding rows required is the remaining
        div arity, padding sectors required the remaining
        mod arity, and the padding is no more than a
        plane's worth on either side.
        """
        core = request // (Geometry.ARITY * Geometry.ARITY)
        remaining = request - core * Plane.SECTORS_PER_PLANE
        if remaining == 0:
            return (Status.GEAR_SUCCESS,
                    candidate * Plane.SECTORS_PER_PLANE)

        # Leader calculation (facts 38 to 44). Row
        # pointer set to the start of the core plane;
        # each unrolled iteration is a function body:
        # decrement the pointer, verify the row count is
        # zero and count the row toward the padding, or,
        # for the first non-zero row (the leading row),
        # take its end run, via the Right oracle's
        # initial sector position, toward the padding
        # sectors required. The take is tracked as one
        # sector count: full rows and a part row together
        # are exactly the sectors immediately before the
        # core, so their sum is the leader's whole offer.
        pointer = candidate * Geometry.ARITY
        plane_floor = pointer - Geometry.ARITY
        leader_take = 0
        while leader_take < remaining and pointer > plane_floor:
            pointer -= 1
            if count_rows[pointer] == 0:
                leader_take += Geometry.ARITY
            else:
                leader_take += _trailing_run(words[pointer])
                break
        if leader_take > remaining:
            leader_take = remaining
        start = (candidate * Plane.SECTORS_PER_PLANE
                 - leader_take)
        still_owed = remaining - leader_take
        if still_owed == 0:
            return (Status.GEAR_SUCCESS, start)

        # Trailing padding (facts 45 to 53). Set the rows
        # pointer just after the core planes and increment
        # it through calls to a different function body:
        # each required full row must have a zero count,
        # and each one decrements the amount owed by
        # arity sectors. Then, with zero rows left, there
        # should be just padding in sectors: advance the
        # pointer once more and evaluate that row with
        # the Left oracle, from position zero, for the
        # trailing sequence of remaining padding.
        following = candidate + core
        row = following * Geometry.ARITY
        trailing_rows = still_owed // Geometry.ARITY
        for step in range(trailing_rows):
            status = self._trailing_row_body(row + step,
                                             count_rows)
            if status != Status.GEAR_SUCCESS:
                return (status, None)
        still_owed = still_owed % Geometry.ARITY
        if still_owed:
            row += trailing_rows
            if (row >= Cube.ROWS_PER_CUBE
                    or _leading_run(words[row]) < still_owed):
                return Status.HUGE_ROW_DRIVER_TRAILER_PADDING_FAIL, None
        return (Status.GEAR_SUCCESS, start)

    # -- bullet and plane driver --

    def __call__(self, plane, row, request, ctx, sector_out):
        """Bullet for one candidate, shaped like Large's.

        plane is the candidate's first core plane; row is
        unused, because a core candidate is a plane (the
        core start row is plane times arity, by shape).
        ctx is (count_planes, count_rows, words). On
        success the start sector within the start row is
        written to sector_out and the full start kept on
        self.last_start; on failure the handler's named
        status is returned, for breakpointing.
        """
        count_planes, count_rows, words = ctx
        if request not in self.range():
            return Status.HUGE_FAIL
        core = request // (Geometry.ARITY * Geometry.ARITY)
        if plane + core > Cube.PLANES_PER_CUBE:
            return Status.HUGE_FAIL
        for follower in range(plane, plane + core):
            if count_planes[follower] != 0:
                return Status.HUGE_FAIL
        if plane == 0:
            status, start = self._rows_no_leading(
                plane, request, count_planes, count_rows, words)
        elif plane + core - 1 == Cube.PLANES_PER_CUBE - 1:
            status, start = self._rows_no_trailing(
                plane, request, count_planes, count_rows, words)
        else:
            status, start = self._rows_normal(
                plane, request, count_planes, count_rows, words)
        if status != Status.GEAR_SUCCESS or start is None:
            return status
        if not self._span_free(start, request, words):
            return Status.HUGE_FAIL
        self.last_start = (start // Plane.SECTORS_PER_PLANE,
                           (start % Plane.SECTORS_PER_PLANE)
                           // Geometry.ARITY,
                           start % Geometry.ARITY)
        sector_out[0] = start % Geometry.ARITY
        return Status.GEAR_SUCCESS

    def _planes_driver(self, request, count_planes, count_rows,
                       words):
        """Huge plane driver (facts 2 to 13).

        Check each plane in turn as the first of the core
        planes; a plane with zero count whose followers
        also have zero count is a candidate and fires one
        of the three row handlers. Failing a coordinate,
        advance to the next originating plane.
        """
        core = request // (Geometry.ARITY * Geometry.ARITY)
        ctx = (count_planes, count_rows, words)
        candidate = 0
        while candidate + core <= Cube.PLANES_PER_CUBE:
            if count_planes[candidate] == 0:
                sector_out = [0]
                status = self(candidate, 0, request, ctx,
                              sector_out)
                if status == Status.GEAR_SUCCESS:
                    return self.last_start
            candidate += 1
        return None

    def search(self, request, count_planes, count_rows, words,
               count_overall=None):
        """Huge.search calls the huge planes driver with
        the three huge row handlers and Huge.__call__.

        In this Python reference the planes driver and the
        handlers are the methods above. The return shape
        is the uniform gear tuple (status, plane, row,
        sector), as for Large.
        """
        if request not in self.range():
            return (Status.HUGE_FAIL, 0, 0, 0)
        start = self._planes_driver(request, count_planes,
                                    count_rows, words)
        if start is None:
            return (Status.GEAR_EXHAUST, 0, 0, 0)
        plane, row, sector = start
        return (Status.GEAR_SUCCESS, plane, row, sector)
