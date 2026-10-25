/* PairsRowDriver.c -- pair-row gear for Small requests: counter gate,
   bullet trial, first conviction up.
   Drafted by muse from the section "Polytope Formation Between Rows:
   The Small Resolution" of the academic paper titled "An Extension of
   Buddy Systems to Arbitrary Radix for Deterministic Memory Allocation",
   provided by author Andrew Jonathan Fine.
   DRAFT, uncommitted, not yet wired into Gears.py or build_gears.bat.
   The gear is mode-neutral: it knows counters and pairs, never tables.
   Arrangement lives in the bullet, bound once through pairs_gear_bind.
   The bullet determines the start sector; this driver forwards the
   bullet's sector_of_anchor unchanged, so no listing return formula is baked
   in here. Return contract (blackboard, 2026-10-25): the anchor is the
   earlier row of the pair; the bullet returns sector_of_anchor, the start
   sector within the anchor row, passed as an output parameter, equal to
   32 minus P where P is the anchor row's tail run length; the ancillary
   head always starts at sector 0. This file sweeps pairs only.
   Sweep order: ascending global pivot, pinned start (first-fit-low
   shape), no rotation yet. Pivot GR1 runs 0..1022, so the second row
   GR1+1 always exists; cross-plane pairs are included, and the pair
   starting at the last row of plane 31 has no second row and is not
   a pivot. When the last pivot acquits or gate-skips, GEAR_EXHAUST
   means the whole cube was searched for a pair, cube-true.
   The pair gate uses free sums: count_rows holds occupied counts, so
   a pair's free room is (32 - count[i]) + (32 - count[i+1]). A pair
   whose free sum is below the request is skipped without a trial.
   This driver does not redefine gear_abi_version: the ABI version 1
   already exported by RowsCheck.c covers this file when built
   together, and a second definition would collide. */

#include <stdint.h>
#include "status.h"

#define ROWS_TOTAL       1024u
#define SECTORS_PER_ROW  32u
#define LAST_PIVOT       1022u

/* The bullet: a mode's pair trial. It receives the pivot as
   (plane, row), the request, its context, and sector_of_anchor. It returns
   GEAR_SUCCESS with *sector_of_anchor set to the start sector within the
   pivot row on conviction, or the mode's own failure code on
   acquittal. The bullet reads both rows of the pair (pivot row and
   pivot row + 1, which may sit in the next plane) from its context. */
typedef int32_t (*bullet_fn) (uint32_t plane, uint32_t row, uint32_t request,
                              void *ctx, uint32_t *sector_of_anchor);

/* The gearing's surviving state: the seated handler and its context. */
static bullet_fn pair_handler_callback = 0;
static void     *pair_handler_ctx      = 0;

__declspec(dllexport) void pairs_gear_bind (bullet_fn bullet, void *ctx)
{
    pair_handler_callback = bullet;
    pair_handler_ctx      = ctx;
}

__declspec(dllexport) int32_t pairs_gear (
    const uint32_t *count_rows,
    uint32_t request,
    uint32_t *sector_of_anchor, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t pivot;
    uint32_t plane;
    uint32_t row;
    uint32_t free_pair;
    int32_t  status;

    if (pair_handler_callback == 0)
        return GEAR_FAIL;

    for (pivot = 0; pivot <= LAST_PIVOT; pivot++)
    {
        free_pair = (SECTORS_PER_ROW - count_rows[pivot])
                  + (SECTORS_PER_ROW - count_rows[pivot + 1]);
        if (request > free_pair)
            continue;
        plane = pivot / SECTORS_PER_ROW;
        row = pivot % SECTORS_PER_ROW;
        status = pair_handler_callback (plane, row, request,
                                        pair_handler_ctx, sector_of_anchor);
        if (status != GEAR_SUCCESS)
            continue;
        *row_out = row;
        *plane_out = plane;
        return GEAR_SUCCESS;
    }

    return GEAR_EXHAUST;
}

/* Per-plane pair handler, for calling the pair sweep plane at a time
   through planes_gear, in the row_handler_fn shape of PlanesCheck.c.
   The first row of the pair is the anchor: it lives in the plane this
   handler is called for. The second row is ancillary by reference:
   it is read directly as count_rows[pivot + 1] (and, by the bullet,
   as the next word in its context), with no second search and no
   copy. For anchor row 31 in planes 0..30, that ancillary is the
   next plane's row 0, with no special case. In plane 31, anchor row
   31 is skipped, since it has no second row. Each pair has exactly
   one anchor, its first row, so no pair is tried twice.
   No plane-total gate lives in this handler, by design. The existing
   planes_gear lane gate (plane free >= request) must be bypassed or
   relaxed for Small cross-plane pairs, because a pair can succeed
   even when its anchor plane total free is below the request (for
   example anchor tail 20 plus next plane head 20 for a request of
   40, while the anchor plane total free is only 20). The pair gates
   below do the real work. A plane whose anchors all gate-skip or
   acquit returns GEAR_EXHAUST for that plane only; planes_gear turns
   the last plane's exhaust into the whole-cube outcome. */
__declspec(dllexport) int32_t pairs_row_handler (
    const uint32_t *count_rows,
    uint32_t plane, uint32_t request,
    bullet_fn item_handler, void *ctx,
    uint32_t *sector_of_anchor, uint32_t *row_out)
{
    uint32_t row;
    uint32_t pivot;
    uint32_t free_pair;
    uint32_t last_row;
    int32_t  status;

    if (item_handler == 0)
        return GEAR_FAIL;
    if (plane >= 32)
        return GEAR_EXHAUST;

    last_row = SECTORS_PER_ROW - 1;
    if (plane == 31)
        last_row = SECTORS_PER_ROW - 2;

    for (row = 0; row <= last_row; row++)
    {
        pivot = plane * SECTORS_PER_ROW + row;
        free_pair = (SECTORS_PER_ROW - count_rows[pivot])
                  + (SECTORS_PER_ROW - count_rows[pivot + 1]);
        if (request > free_pair)
            continue;
        status = item_handler (plane, row, request, ctx, sector_of_anchor);
        if (status != GEAR_SUCCESS)
            continue;
        *row_out = row;
        return GEAR_SUCCESS;
    }

    return GEAR_EXHAUST;
}
