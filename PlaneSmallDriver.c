/* PlaneSmallDriver.c -- planes sweep for Small requests.
   Drafted by muse from the section "Polytope Formation Between Rows:
   The Small Resolution" of the academic paper titled "An Extension of
   Buddy Systems to Arbitrary Radix for Deterministic Memory Allocation",
   provided by author Andrew Jonathan Fine.
   Wired into Gears.py (scan_small) and build_gears.bat.
   Planes-pair gate, verbatim (user, 2026-10-25): a pair of
   planes passes under Small iff plane n has at least 1 sector
   free and plane n+1 has at least (request - 1) sectors free.
   For plane 31, which has no next plane and whose row 31 cannot
   anchor, a plane is tried only when free in plane 31 alone
   reaches the request. Inside a tried plane, the pair gates in
   pairs_row_handler do the finer work. */

#include <stdint.h>
#include "status.h"

#define PLANES_PER_CUBE  32u
#define SECTORS_PER_PLANE  1024u

/* The bullet: a mode's pair trial. It receives the anchor as
   (plane, row), the request, its context, and sector_of_anchor. It
   returns GEAR_SUCCESS with *sector_of_anchor set to the start
   sector within the anchor row on conviction, or the mode's own
   failure code on acquittal. */
typedef int32_t (*bullet_fn) (uint32_t plane, uint32_t row, uint32_t request,
                              void *ctx, uint32_t *sector_of_anchor);

/* The per-plane pair handler, defined in PairsRowDriver.c. */
extern int32_t pairs_row_handler (const uint32_t *count_rows,
                                  uint32_t plane, uint32_t request,
                                  bullet_fn item_handler, void *ctx,
                                  uint32_t *sector_of_anchor,
                                  uint32_t *row_out);

/* The gearing's surviving state: the seated handler and its context. */
static bullet_fn small_handler_callback = 0;
static void     *small_handler_ctx      = 0;

__declspec(dllexport) void planes_small_gear_bind (bullet_fn bullet, void *ctx)
{
    small_handler_callback = bullet;
    small_handler_ctx      = ctx;
}

__declspec(dllexport) int32_t planes_small_gear (
    const uint32_t *count_planes,
    const uint32_t *count_rows,
    uint32_t request,
    uint32_t *sector_of_anchor, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t plane;
    uint32_t first;
    int32_t  status;
    static uint32_t start = 0;

    /* Rotate, starting at zero: use the current start for this
       call, then advance for the next entry, failures included,
       wrapping 31 -> 0. First call after load starts at plane 0. */
    first = start;
    start = start + 1;
    if (start >= PLANES_PER_CUBE)
        start = 0;

    if (small_handler_callback == 0)
        return GEAR_FAIL;

    plane = first;
    /* Trial 0: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 1: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 2: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 3: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 4: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 5: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 6: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 7: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 8: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 9: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 10: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 11: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 12: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 13: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 14: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 15: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 16: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 17: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 18: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 19: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 20: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 21: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 22: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 23: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 24: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 25: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 26: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 27: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 28: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 29: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 30: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }
    plane = plane + 1;
    if (plane >= PLANES_PER_CUBE)
        plane = 0;

    /* Trial 31: pair-plane gate, then pairs_row_handler. */
    if (((plane == PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= request))
            || ((plane != PLANES_PER_CUBE - 1)
            && (SECTORS_PER_PLANE - count_planes[plane] >= 1)
            && (SECTORS_PER_PLANE - count_planes[plane + 1] >= request - 1)))
    {
        status = pairs_row_handler (count_rows, plane, request,
                                    small_handler_callback,
                                    small_handler_ctx,
                                    sector_of_anchor, row_out);
        if (status == GEAR_SUCCESS) goto convicted;
    }

    return GEAR_EXHAUST;

convicted:
    *plane_out = plane;
    return GEAR_SUCCESS;
}
