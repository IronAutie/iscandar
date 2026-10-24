/* These are data structure maintenance routines with no original
 * content. They were written by command of the author while he
 * was ill in bed. */

/* Mark.c -- the mark wrapper. Thin export over the shared helper
 * in Commit.c: mark_sectors calls the helper with the mark
 * direction. The helper owns the sectors array and the row and
 * plane counters; the overall counter is kept in Python.
 *
 * Settled contract: int32_t mark_sectors(uint32_t *sectors,
 * uint32_t *count_rows, uint32_t *count_planes, uint32_t start,
 * uint32_t count) -> status. Success is GEAR_SUCCESS. The only
 * failure is check-then-set, FAIL_OVERLAY. No overrun guard here:
 * the Python boundary owns that check.
 *
 * Implementation pending the author's word: blackboard Q4 (the
 * single-row collapse) and confirmation of the detailed design. */
