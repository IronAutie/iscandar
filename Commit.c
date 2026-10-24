/* These are data structure maintenance routines with no original
 * content. They were written by command of the author while he
 * was ill in bed. */

/* Commit.c -- the shared commit-path helper (proposed name; the
 * author may rename it). One template, with a direction flag:
 * mark one way, unmark the other. Mark.c and Unmark.c are thin
 * wrappers over it. It lives as its own .c file, compiled and
 * linked normally -- no .c file is ever included.
 *
 * Settled shape: start S, count L, end E = S + L - 1; first and
 * last row by division by 32, first and last plane by division by
 * 1024. First edge row and last edge row take one masked word op
 * each (OR to mark, AND with the complement to unmark) plus a
 * partial counter add or subtract. Middle rows go by a single
 * memset over the range (0xFF / 0x00), their counters assigned
 * 32 / 0; middle planes assigned 1024 / 0. Edge planes move by
 * arithmetic: edge partials plus 32 per middle row inside the
 * plane. Check-then-set guards every flip: edge words on their
 * bits, middle ranges on their counters. Any check that fails
 * returns FAIL_OVERLAY and flips nothing.
 *
 * Q4 settled (experimental): the single-row case takes the
 * combined-mask branch -- one masked op, no middles. Bodies
 * written per the author's confirmed detailed design; the
 * single-row branch remains experimental. */

#include "Commit.h"
#include "status.h"

#include <string.h>

int32_t commit_sectors(uint32_t *sectors, uint32_t *count_rows,
                       uint32_t *count_planes, uint32_t start,
                       uint32_t count, int direction)
{
    uint32_t s;
    uint32_t e;
    uint32_t first_row;
    uint32_t last_row;
    uint32_t first_plane;
    uint32_t last_plane;
    uint32_t first_mask;
    uint32_t last_mask;
    uint32_t mask;
    uint32_t first_partial;
    uint32_t last_partial;
    uint32_t middle_in_first;
    uint32_t middle_in_last;
    uint32_t middle_in_plane;
    uint32_t r;
    uint32_t p;
    int is_mark;

    /* Caller error, not an overlay: nothing to mark or unmark. */
    if (count == 0) {
        return FAIL;
    }

    is_mark = (direction == COMMIT_MARK);

    s = start;
    e = s + count - 1;
    first_row = s / 32;
    last_row = e / 32;
    first_plane = first_row / 32;
    last_plane = last_row / 32;

    /* Masks in sector order: sector s is bit s, so a word mask
     * uses 1u << s. Positions are never mirrored into sectors.
     * Shifting by 32 is undefined, so the last-edge mask is built
     * with a guard for the full-row case. */
    first_mask = 0xFFFFFFFFu << (s % 32);
    if ((e % 32) == 31) {
        last_mask = 0xFFFFFFFFu;
    } else {
        last_mask = (1u << ((e % 32) + 1)) - 1;
    }

    /* Single-row case (Q4, experimental): one masked op, no
     * middles. The combined mask is the intersection of the two
     * edge masks in that row. Its contribution to the counters
     * is L. */
    if (first_row == last_row) {
        mask = first_mask & last_mask;
        if (is_mark) {
            if ((sectors[first_row] & mask) != 0) {
                return FAIL_OVERLAY;
            }
        } else {
            if ((sectors[first_row] & mask) != mask) {
                return FAIL_OVERLAY;
            }
        }
        if (is_mark) {
            sectors[first_row] |= mask;
            count_rows[first_row] += count;
            count_planes[first_plane] += count;
        } else {
            sectors[first_row] &= ~mask;
            count_rows[first_row] -= count;
            count_planes[first_plane] -= count;
        }
        return GEAR_SUCCESS;
    }

    first_partial = 32 - (s % 32);
    last_partial = (e % 32) + 1;

    /* Phase 1: validate everything. Nothing flips below unless
     * every check here passes, so a failure changes no word and
     * no counter at all. */
    /* Edge words, on their bits. */
    if (is_mark) {
        if ((sectors[first_row] & first_mask) != 0) {
            return FAIL_OVERLAY;
        }
        if ((sectors[last_row] & last_mask) != 0) {
            return FAIL_OVERLAY;
        }
    } else {
        if ((sectors[first_row] & first_mask) != first_mask) {
            return FAIL_OVERLAY;
        }
        if ((sectors[last_row] & last_mask) != last_mask) {
            return FAIL_OVERLAY;
        }
    }
    /* Middle rows, on their counters: no bit-scan before a bulk
     * fill, per the confirmed design. A middle row about to be
     * filled must be entirely free (mark) or entirely occupied
     * (unmark), and its counter says so. */
    for (r = first_row + 1; r < last_row; r++) {
        if (is_mark) {
            if (count_rows[r] != 0) {
                return FAIL_OVERLAY;
            }
        } else {
            if (count_rows[r] != 32) {
                return FAIL_OVERLAY;
            }
        }
    }
    /* Middle planes, on their counters, likewise. */
    for (p = first_plane + 1; p < last_plane; p++) {
        if (is_mark) {
            if (count_planes[p] != 0) {
                return FAIL_OVERLAY;
            }
        } else {
            if (count_planes[p] != 1024) {
                return FAIL_OVERLAY;
            }
        }
    }

    /* Phase 2: commit. Edge rows first: one masked word op each,
     * plus a partial counter move. */
    if (is_mark) {
        sectors[first_row] |= first_mask;
        count_rows[first_row] += first_partial;
        sectors[last_row] |= last_mask;
        count_rows[last_row] += last_partial;
    } else {
        sectors[first_row] &= ~first_mask;
        count_rows[first_row] -= first_partial;
        sectors[last_row] &= ~last_mask;
        count_rows[last_row] -= last_partial;
    }

    /* Middle rows: one memset over the contiguous range, then
     * assign their counters (memset cannot express 32 in a
     * uint32 array, so the counters go by a bounded loop). */
    if (last_row > first_row + 1) {
        memset(&sectors[first_row + 1],
               is_mark ? 0xFF : 0x00,
               (size_t)(last_row - first_row - 1) * sizeof(uint32_t));
        for (r = first_row + 1; r < last_row; r++) {
            count_rows[r] = is_mark ? 32 : 0;
        }
    }

    /* Planes: middle planes assigned whole; edge planes move by
     * arithmetic (edge partials plus 32 per middle row inside
     * the plane). */
    if (first_plane != last_plane) {
        middle_in_first = 31 - (first_row % 32);
        middle_in_last = last_row % 32;
        for (p = first_plane + 1; p < last_plane; p++) {
            count_planes[p] = is_mark ? 1024 : 0;
        }
        if (is_mark) {
            count_planes[first_plane] += first_partial
                                       + 32 * middle_in_first;
            count_planes[last_plane] += last_partial
                                      + 32 * middle_in_last;
        } else {
            count_planes[first_plane] -= first_partial
                                       + 32 * middle_in_first;
            count_planes[last_plane] -= last_partial
                                      + 32 * middle_in_last;
        }
    } else {
        middle_in_plane = 0;
        if (last_row > first_row + 1) {
            middle_in_plane = last_row - first_row - 1;
        }
        if (is_mark) {
            count_planes[first_plane] += first_partial + last_partial
                                       + 32 * middle_in_plane;
        } else {
            count_planes[first_plane] -= first_partial + last_partial
                                       + 32 * middle_in_plane;
        }
    }

    return GEAR_SUCCESS;
}
