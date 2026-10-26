from Geometry import Geometry
from Row      import Row
from Plane    import Plane
from Mode     import Mode
from Status   import Status


def _trailing_run(word):
    """Free run ending at sector 31, counted down from 31.

    This is the Right oracle, in row-word terms: the run that
    ends at the right edge. A word with sector 31 occupied
    gives 0. A wholly clear word gives 32.

    Scan start, pinned down 2026-10-26: sector 31, the MSB
    bit. This is the trailing series in sector order, and
    the same run the OracleRight file reports.
    """
    run = 0
    for sector in range(31, -1, -1):
        if (word >> sector) & 1 == 0:
            run += 1
        else:
            break
    return run


def _leading_run(word):
    """Free run starting at sector 0, counted up from 0.

    This is the Left oracle, in row-word terms: the run that
    starts at the left edge. A word with sector 0 occupied
    gives 0. A wholly clear word gives 32.

    Scan start, pinned down 2026-10-26: sector 0, the LSB
    bit, NOT the MSB. This is the leading series in sector
    order, and the same run the OracleLeft file reports.
    It is not the MSB-starting run; that is the trailing
    run above.
    """
    run = 0
    for sector in range(32):
        if (word >> sector) & 1 == 0:
            run += 1
        else:
            break
    return run


class Large(Mode):
    """Large: 2A < L <= A^2, 65 to 1024 sectors.

    Rederived from requirements, 2026-10-25/26 blackboard,
    not ported from the APL listings. The APL listings were
    set aside as design authority: their Position formulas
    use 64 x plane instead of 1024 x plane, their row
    dispatch call shapes are inconsistent, and the
    VerifyWeld they call is not defined in them.

    Blackboard, in order:
    1. Midsection computed first: core = request div arity.
    2. Option A only. Option A is consecutive full rows
       for the midsection. If consecutive full rows cannot
       be found, Option A is off the table for that
       launching.
    3. Launch gate: a launching cannot proceed unless
       the sum of free sectors of the planes is at least
       the request. Only two planes are ever considered
       for a single launching: the starting plane, and
       the next plane if the span crosses.
    4. A Large span is contiguous, mandatory: one start
       plus one count, consecutive sectors. A span may
       start mid-plane and extend into the next plane;
       that is still Large by size, not Huge.
    5. Row level: at each row in plane A, are the core
       number of rows starting with said row blank?
       Yes, even if they must peek into the second plane.
       If no such sequence is found, return to the plane
       driver for launch of the next plane.
    6. After the core rows are found, three scenarios:
       (a) core start index 0: no head, left oracle on
           the following row for leading sectors
           satisfying the remainder;
       (b) final core row index 1023: no tail, right
           oracle on the previous row for trailing
           sectors satisfying the remainder;
       (c) both rows exist: right oracle first, as
           many trailing sectors as will fit from the
           row before the core; if that covers the
           remaining, done; otherwise subtract what got
           covered, then left oracle to confirm
           sufficient leading sectors to satisfy the
           remainder.
       If none of the three fit, the plane is exhausted
       and return. Else return a coordinate.
    7. The coordinate is at the start of the leading
       run for this entire piecewise span.
    8. No loop traverses the core per candidate. A
       pointer inside the row level handler is reset,
       then advanced and checked as a rolling window:
       the window sum for the next core start is the
       previous window sum, minus the row leaving the
       window, plus the row entering it. In C this is
       multiple statements as an unrolled loop; in
       this Python reference it is the same rolling
       window, advanced one row at a time.
    9. Amendment, 2026-10-26 (second pass, split
       edges). Simulation caught a specification
       error in the case analysis above: a contiguous
       span decomposes as head + f whole rows + tail
       with f either core or core - 1, and items 5
       and 6 cover only f = core. A span with
       f = core - 1 (both edges principal, head +
       tail = remainder + arity) exhausted while an
       exact-fit contiguous hole existed. The
       amendment completes Option A rather than
       adding an Option B: when the first pass finds
       no launching, a second pass runs the same
       drivers with a core - 1 window and a unified
       edge budget (see _probe_split). The second
       pass's launch gate adds the free count of
       the single head row before the launching
       plane, because a split span can lean up to
       arity - 1 sectors into that row, which the
       two-plane sum never counts. The first
       pass is unchanged, so every placement it made
       before the amendment is made identically
       after it; the second pass only rescues spans
       the first pass could not see. With both
       passes, a placement exists if and only if a
       contiguous free run of the request exists.
    """

    def range(self):
        "reveal at which this __call__ is invoked"

        return self.inclusive(Row.SECTORS_TWEEN_ROWS + 1,
                              Plane.SECTORS_PER_PLANE)

    def __call__(self, plane, row, request, ctx, sector_out):
        """Bullet for one core start, shaped like Nano/Tiny/Small.

        plane, row are the core start, in plane/row form.
        ctx is the sectors words array. sector_out is a
        one-element cell taking the start sector on
        conviction. The full start coordinate is also
        stored on self.last_start, because a Large start
        can sit in the head row, in a different plane
        from the core start, and the C bullet contract
        carries only one sector cell. search() reads
        last_start after a conviction; it never trusts
        the core-start plane/row alone.
        """
        start = self._probe(plane * Geometry.ARITY + row,
                            request, ctx)
        if start is None:
            return Status.LARGE_FAIL
        self.last_start = start
        sector_out[0] = start[2]
        return Status.GEAR_SUCCESS

    def _probe(self, core_start, request, words):
        """One core start: return a start coordinate, or None.

        core_start is a global row index. words is the
        1024 row-word array, index plane * 32 + row.
        This checks the core blankness for this start
        only; the rolling window over starts lives in
        _rows_driver, which calls this per start.
        """
        if request not in self.range():
            return None
        core = request // Geometry.ARITY
        remainder = request % Geometry.ARITY
        if core_start < 0 or core_start + core > 1024:
            return None
        for g in range(core_start, core_start + core):
            if words[g] != 0:
                return None
        if remainder == 0:
            return (core_start // Geometry.ARITY,
                    core_start % Geometry.ARITY, 0)
        head_row = core_start - 1
        tail_row = core_start + core
        if core_start == 0:
            if tail_row >= 1024:
                return None
            if _leading_run(words[tail_row]) < remainder:
                return None
            return (core_start // Geometry.ARITY,
                    core_start % Geometry.ARITY, 0)
        if core_start + core - 1 == 1023:
            if head_row < 0:
                return None
            if _trailing_run(words[head_row]) < remainder:
                return None
            return (head_row // Geometry.ARITY,
                    head_row % Geometry.ARITY,
                    32 - remainder)
        head_len = _trailing_run(words[head_row])
        head_take = head_len if head_len < remainder else remainder
        remaining = remainder - head_take
        if remaining == 0:
            return (head_row // Geometry.ARITY,
                    head_row % Geometry.ARITY,
                    32 - head_take)
        if tail_row >= 1024:
            return None
        if _leading_run(words[tail_row]) < remaining:
            return None
        if head_take > 0:
            return (head_row // Geometry.ARITY,
                    head_row % Geometry.ARITY,
                    32 - head_take)
        return (core_start // Geometry.ARITY,
                core_start % Geometry.ARITY, 0)

    def _rows_driver(self, plane, request, count_rows, words):
        """Row level handler for one launching plane.

        Pointer reset at the first row of this plane,
        then advanced one row at a time, checked as a
        rolling window. No loop traverses the core per
        candidate: window_sum is built once for the
        first start in this plane, then rolled.
        Returns a start coordinate, or None.
        """
        core = request // Geometry.ARITY
        first = plane * Geometry.ARITY
        if first + core > 1024:
            return None
        window_sum = 0
        for g in range(first, first + core):
            window_sum += count_rows[g]
        core_start = first
        while core_start < first + Geometry.ARITY:
            if core_start + core > 1024:
                break
            if window_sum == 0:
                start = self._probe(core_start, request, words)
                if start is not None:
                    return start
            if core_start + core < 1024:
                window_sum += (count_rows[core_start + core]
                               - count_rows[core_start])
            core_start += 1
        return None

    def _probe_split(self, core_start, request, words):
        """One core start of the second pass: the
        split-edge case, f = core - 1 blank rows.

        The blank rows are core_start .. core_start +
        core - 2. What they do not cover is the budget:
        request minus the blank rows' sectors, which
        is remainder + arity. The head row's trailing
        run is taken whole toward the budget (it is
        at most arity - 1, always less than the
        budget, so the tail is always needed too);
        the tail row, the row right after the blank
        rows, must cover the rest of the budget with
        its leading run. Returns a start coordinate,
        or None.
        """
        if request not in self.range():
            return None
        core = request // Geometry.ARITY
        width = core - 1
        if core_start < 0 or core_start + width > 1024:
            return None
        for g in range(core_start, core_start + width):
            if words[g] != 0:
                return None
        budget = request - width * Geometry.ARITY
        head_take = 0
        if core_start > 0:
            head_take = _trailing_run(words[core_start - 1])
        owed = budget - head_take
        if owed <= 0:
            return None
        tail_row = core_start + width
        if tail_row >= 1024:
            return None
        if _leading_run(words[tail_row]) < owed:
            return None
        start = core_start * Geometry.ARITY - head_take
        return (start // Plane.SECTORS_PER_PLANE,
                (start % Plane.SECTORS_PER_PLANE)
                // Geometry.ARITY,
                start % Geometry.ARITY)

    def _rows_driver_split(self, plane, request, count_rows,
                           words):
        """Second-pass row handler for one launching
        plane: the first pass's rolling window at
        width core - 1, probed by _probe_split.
        Returns a start coordinate, or None.
        """
        core = request // Geometry.ARITY
        width = core - 1
        first = plane * Geometry.ARITY
        if width < 1 or first + width > 1024:
            return None
        window_sum = 0
        for g in range(first, first + width):
            window_sum += count_rows[g]
        core_start = first
        while core_start < first + Geometry.ARITY:
            if core_start + width > 1024:
                break
            if window_sum == 0:
                start = self._probe_split(core_start,
                                          request, words)
                if start is not None:
                    return start
            if core_start + width < 1024:
                window_sum += (count_rows[core_start + width]
                               - count_rows[core_start])
            core_start += 1
        return None

    def _planes_driver(self, request, count_planes, count_rows,
                       words):
        """Plane driver: two passes over the launchings
        in ascending plane order.

        Pass one is the original driver, unchanged:
        launchings in ascending order under the launch
        gate, verbatim from the blackboard: a launching
        cannot proceed unless the sum of free sectors
        of the planes is at least the request. For
        plane 31 there is no next plane, so its own
        free sectors alone must reach the request.
        Only two planes are considered per launching.
        Pass two, the 2026-10-26 amendment, runs only
        when pass one finds nothing: the same
        launchings, with the split rows driver
        (core - 1 blank rows, both edges principal),
        under the launch gate plus one allowance:
        the free count of the single head row before
        the launching plane, because a split span
        can lean up to arity - 1 sectors into that
        row and the two-plane sum never counts it.
        Returns a start coordinate, or None.
        """
        for plane in range(Geometry.ARITY):
            free_here = (Plane.SECTORS_PER_PLANE
                         - count_planes[plane])
            free_next = 0
            if plane + 1 < Geometry.ARITY:
                free_next = (Plane.SECTORS_PER_PLANE
                             - count_planes[plane + 1])
            if free_here + free_next < request:
                continue
            start = self._rows_driver(plane, request,
                                      count_rows, words)
            if start is not None:
                return start
        for plane in range(Geometry.ARITY):
            free_here = (Plane.SECTORS_PER_PLANE
                         - count_planes[plane])
            free_next = 0
            if plane + 1 < Geometry.ARITY:
                free_next = (Plane.SECTORS_PER_PLANE
                             - count_planes[plane + 1])
            head_allowance = 0
            if plane > 0:
                head_allowance = (Row.SECTORS_PER_ROW
                                  - count_rows[plane
                                               * Geometry.ARITY
                                               - 1])
            if (free_here + free_next + head_allowance
                    < request):
                continue
            start = self._rows_driver_split(plane, request,
                                            count_rows, words)
            if start is not None:
                return start
        return None

    def search(self, request, count_planes, count_rows, words,
               count_overall=None):
        """Large.search calls the large planes driver with
        the large rows driver and Large.__call__.

        In this Python reference, the planes driver and
        rows driver are the methods above, and __call__
        is the per-core-start bullet, called by the
        rows driver through _probe. The return shape is
        the uniform gear tuple (status, plane, row,
        sector), so the engine's translation to
        Coordinate is pattern-independent.
        """
        if request not in self.range():
            return (Status.LARGE_FAIL, 0, 0, 0)
        start = self._planes_driver(request, count_planes,
                                    count_rows, words)
        if start is None:
            return (Status.GEAR_EXHAUST, 0, 0, 0)
        plane, row, sector = start
        return (Status.GEAR_SUCCESS, plane, row, sector)
