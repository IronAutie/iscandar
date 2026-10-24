/* These are data structure maintenance routines with no original
 * content. They were written by command of the author while he
 * was ill in bed. */

/* Unmark.c -- the unmark wrapper. Thin export over the shared
 * helper in Commit.c: unmark_sectors calls the helper with the
 * unmark direction. Mirror of Mark.c in every respect.
 *
 * Settled contract: int32_t unmark_sectors(uint32_t *sectors,
 * uint32_t *count_rows, uint32_t *count_planes, uint32_t start,
 * uint32_t count) -> status. Success is GEAR_SUCCESS. The only
 * failure is check-then-set, FAIL_OVERLAY. No overrun guard here:
 * the Python boundary owns that check.
 *
 * Q4 settled (experimental): the single-row case takes the
 * combined-mask branch -- one masked op, no middles. Bodies
 * written per the author's confirmed detailed design; the
 * single-row branch remains experimental. */

#include "Commit.h"
#include "status.h"

int32_t unmark_sectors(uint32_t *sectors, uint32_t *count_rows,
                       uint32_t *count_planes, uint32_t start,
                       uint32_t count)
{
    return commit_sectors(sectors, count_rows, count_planes,
                          start, count, COMMIT_UNMARK);
}
