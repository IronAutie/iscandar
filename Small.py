from Geometry import Geometry
from Row      import Row
from Mode     import Mode
from Status   import Status


class Small (Mode):
    "handles between rows requests"

    def range    (self):
        "reveal at which this __call__ is invoked"

        return self.inclusive (Row.SECTORS_PER_ROW + 1,
                               Row.SECTORS_TWEEN_ROWS)

    def search (self, request, count_planes, count_rows, words,
                count_overall=None):
        "Run this mode's search/test pattern against the C gears."

        # Separate gear, called from Small mode like pairs_gear:
        # planes_small_gear, not the standard planes-over-rows
        # pattern. count_planes IS passed, for the pair-plane gate (user
        # verbatim, 2026-10-25): a pair of planes passes iff
        # plane n has at least 1 sector free and plane n+1 has
        # at least (request - 1) sectors free; plane 31 alone,
        # since it has no next plane. The pair gates inside
        # pairs_row_handler do the finer work. Return shape is the same raw gear tuple
        # (status, plane, row, sector) as the base pattern, so
        # the engine's translation is pattern-independent.
        import Gears

        def bullet (plane, row, request, _ctx, sector_of_anchor):
            return self (plane, row, request, words, sector_of_anchor)

        bullet_fn = Gears.BULLET_FN (bullet)
        return Gears.scan_small (count_planes, count_rows, request, bullet_fn)

    def __call__ (self, plane, row, request, ctx, sector_of_anchor):
        "SectorChecker as a bullet, shaped by the handler call."

        # The handler call defines this shape: probe a pair of
        # rows. ctx is the sectors words array; sector_of_anchor
        # is a one-element mutable cell taking the placement's
        # start sector within the anchor row on conviction. The
        # probe never marks; it only reports a sector or a
        # failure. Acquittal returns the mode's own failure code,
        # per the C bullet contract; the gear treats any
        # non-success as "try the next pair".

        # Anchor is the earlier row of the pair, ancillary the
        # later row, which is simply the next word in ctx, even
        # across a plane boundary (anchor row 31 of a plane
        # pairs with row 0 of the next plane). Global row 1023
        # has no later row, so it cannot be an anchor.
        # Out-of-domain length fails the same way: no pair
        # fits it, so the gear exhausts and the mode fails.
        global_row = plane * Geometry.ARITY + row
        if not 0 <= global_row <= 1022:
            return Status.SMALL_FAIL
        if request not in self.range ():
            return Status.SMALL_FAIL

        anchor = ctx [global_row]
        ancillary = ctx [global_row + 1]

        # P: anchor tail run ending at sector 31. Count clear
        # bits down from sector 31; stop at the first occupied
        # sector, or at 32 if the whole row is clear. P = 0
        # means the anchor does not reach the row edge, so this
        # pair cannot join, however much free space the pair
        # holds elsewhere. Edge-join only is the semantic
        # intent, not a bug.
        tail_len = 0
        for sector in range (31, -1, -1):
            if (anchor >> sector) & 1 == 0:
                tail_len += 1
            else:
                break

        # Q: ancillary head run starting at sector 0. Count
        # clear bits up from sector 0; stop at the first
        # occupied sector, or at 32 if the whole row is clear.
        # Q = 0 means the ancillary does not start at the row
        # edge, so this pair cannot join. Center cannot certify
        # this: a run 1..31 in the ancillary, length 31, is
        # detected by Center, but its head is 0, and the pair
        # must acquit.
        head_len = 0
        for sector in range (32):
            if (ancillary >> sector) & 1 == 0:
                head_len += 1
            else:
                break

        # Logical pair certification, not a free-sum gate: both
        # edges must be present, and together they must reach
        # the request. A free-sum gate alone does not prove
        # edge anchoring.
        if tail_len < 1 or head_len < 1:
            return Status.SMALL_FAIL
        if tail_len + head_len < request:
            return Status.SMALL_FAIL

        # Conviction: start at the anchor tail's start, so the
        # block runs forward from there into the ancillary head,
        # which always starts at sector 0. Oversize tails still
        # start at the tail start: Engine.mark marks a flat
        # linear interval of request sectors from this start,
        # so it takes the whole tail and only the head portion
        # it needs, leaving any extra head free.
        sector_of_anchor [0] = 32 - tail_len
        return Status.GEAR_SUCCESS
