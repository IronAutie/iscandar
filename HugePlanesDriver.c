/* HugePlanesDriver.c -- plane driver for Huge requests
   Blackboard 2026-10-26 (huge-blackboard, 53 facts).
   Check each plane in turn: a plane whose own count is
   zero and whose follower core planes also have zero
   count is a candidate and fires a row handler. Failing
   a coordinate, advance to the next originating plane.
   Core is request div arity squared and never makes 32
   in Huge, since Cube handles the whole cube separately.
   Plane dispatch is unrolled, one block per plane.
   Amendment 2026-10-26: a second sweep (split seams)
   runs after the first sweep, core - 1 empty planes
   flanked by both edge planes; see Huge.py item 6.
   Portable: EXPORT is empty on non-Windows.
*/
#include <stdint.h>
#include "status.h"
#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif
#define ARITY 32u
#define PLANES 32u
#define SECTORS_PER_PLANE 1024u

extern int32_t rows_huge_gear(const uint32_t *count_planes,
                              const uint32_t *count_rows,
                              const uint32_t *words,
                              uint32_t candidate,
                              uint32_t request,
                              uint32_t *plane_out,
                              uint32_t *row_out,
                              uint32_t *sector_out);
extern int32_t rows_huge_split_gear(const uint32_t *count_planes,
                                    const uint32_t *count_rows,
                                    const uint32_t *words,
                                    uint32_t seam,
                                    uint32_t request,
                                    uint32_t *plane_out,
                                    uint32_t *row_out,
                                    uint32_t *sector_out);

static int32_t split_fires(const uint32_t *count_planes,
                           const uint32_t *count_rows,
                           const uint32_t *words,
                           uint32_t seam,
                           uint32_t request,
                           uint32_t *plane_out,
                           uint32_t *row_out,
                           uint32_t *sector_out) {
    uint32_t core = request / SECTORS_PER_PLANE;
    if (seam < 1 || seam + core - 1 > PLANES - 1) return GEAR_FAIL;
    return rows_huge_split_gear(count_planes, count_rows, words,
                                seam, request,
                                plane_out, row_out, sector_out);
}

static int32_t candidate_fires(const uint32_t *count_planes,
                               const uint32_t *count_rows,
                               const uint32_t *words,
                               uint32_t candidate,
                               uint32_t request,
                               uint32_t *plane_out,
                               uint32_t *row_out,
                               uint32_t *sector_out) {
    uint32_t core = request / SECTORS_PER_PLANE;
    uint32_t k;
    if (candidate + core > PLANES) return GEAR_FAIL;
    for (k = 0; k < core; k++) {
        if (count_planes[candidate + k] != 0) return GEAR_FAIL;
    }
    return rows_huge_gear(count_planes, count_rows, words,
                          candidate, request,
                          plane_out, row_out, sector_out);
}

EXPORT int32_t planes_huge_gear(const uint32_t *count_planes,
                                const uint32_t *count_rows,
                                const uint32_t *words,
                                uint32_t request,
                                uint32_t *plane_out,
                                uint32_t *row_out,
                                uint32_t *sector_out) {
    /* P0 */
    if (candidate_fires(count_planes, count_rows, words, 0u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P1 */
    if (candidate_fires(count_planes, count_rows, words, 1u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P2 */
    if (candidate_fires(count_planes, count_rows, words, 2u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P3 */
    if (candidate_fires(count_planes, count_rows, words, 3u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P4 */
    if (candidate_fires(count_planes, count_rows, words, 4u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P5 */
    if (candidate_fires(count_planes, count_rows, words, 5u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P6 */
    if (candidate_fires(count_planes, count_rows, words, 6u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P7 */
    if (candidate_fires(count_planes, count_rows, words, 7u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P8 */
    if (candidate_fires(count_planes, count_rows, words, 8u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P9 */
    if (candidate_fires(count_planes, count_rows, words, 9u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P10 */
    if (candidate_fires(count_planes, count_rows, words, 10u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P11 */
    if (candidate_fires(count_planes, count_rows, words, 11u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P12 */
    if (candidate_fires(count_planes, count_rows, words, 12u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P13 */
    if (candidate_fires(count_planes, count_rows, words, 13u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P14 */
    if (candidate_fires(count_planes, count_rows, words, 14u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P15 */
    if (candidate_fires(count_planes, count_rows, words, 15u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P16 */
    if (candidate_fires(count_planes, count_rows, words, 16u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P17 */
    if (candidate_fires(count_planes, count_rows, words, 17u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P18 */
    if (candidate_fires(count_planes, count_rows, words, 18u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P19 */
    if (candidate_fires(count_planes, count_rows, words, 19u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P20 */
    if (candidate_fires(count_planes, count_rows, words, 20u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P21 */
    if (candidate_fires(count_planes, count_rows, words, 21u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P22 */
    if (candidate_fires(count_planes, count_rows, words, 22u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P23 */
    if (candidate_fires(count_planes, count_rows, words, 23u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P24 */
    if (candidate_fires(count_planes, count_rows, words, 24u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P25 */
    if (candidate_fires(count_planes, count_rows, words, 25u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P26 */
    if (candidate_fires(count_planes, count_rows, words, 26u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P27 */
    if (candidate_fires(count_planes, count_rows, words, 27u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P28 */
    if (candidate_fires(count_planes, count_rows, words, 28u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P29 */
    if (candidate_fires(count_planes, count_rows, words, 29u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P30 */
    if (candidate_fires(count_planes, count_rows, words, 30u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* P31 */
    if (candidate_fires(count_planes, count_rows, words, 31u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S1 */
    if (split_fires(count_planes, count_rows, words, 1u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S2 */
    if (split_fires(count_planes, count_rows, words, 2u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S3 */
    if (split_fires(count_planes, count_rows, words, 3u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S4 */
    if (split_fires(count_planes, count_rows, words, 4u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S5 */
    if (split_fires(count_planes, count_rows, words, 5u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S6 */
    if (split_fires(count_planes, count_rows, words, 6u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S7 */
    if (split_fires(count_planes, count_rows, words, 7u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S8 */
    if (split_fires(count_planes, count_rows, words, 8u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S9 */
    if (split_fires(count_planes, count_rows, words, 9u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S10 */
    if (split_fires(count_planes, count_rows, words, 10u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S11 */
    if (split_fires(count_planes, count_rows, words, 11u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S12 */
    if (split_fires(count_planes, count_rows, words, 12u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S13 */
    if (split_fires(count_planes, count_rows, words, 13u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S14 */
    if (split_fires(count_planes, count_rows, words, 14u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S15 */
    if (split_fires(count_planes, count_rows, words, 15u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S16 */
    if (split_fires(count_planes, count_rows, words, 16u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S17 */
    if (split_fires(count_planes, count_rows, words, 17u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S18 */
    if (split_fires(count_planes, count_rows, words, 18u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S19 */
    if (split_fires(count_planes, count_rows, words, 19u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S20 */
    if (split_fires(count_planes, count_rows, words, 20u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S21 */
    if (split_fires(count_planes, count_rows, words, 21u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S22 */
    if (split_fires(count_planes, count_rows, words, 22u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S23 */
    if (split_fires(count_planes, count_rows, words, 23u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S24 */
    if (split_fires(count_planes, count_rows, words, 24u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S25 */
    if (split_fires(count_planes, count_rows, words, 25u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S26 */
    if (split_fires(count_planes, count_rows, words, 26u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S27 */
    if (split_fires(count_planes, count_rows, words, 27u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S28 */
    if (split_fires(count_planes, count_rows, words, 28u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S29 */
    if (split_fires(count_planes, count_rows, words, 29u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S30 */
    if (split_fires(count_planes, count_rows, words, 30u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    /* Second sweep, S31 */
    if (split_fires(count_planes, count_rows, words, 31u, request, plane_out, row_out, sector_out) == GEAR_SUCCESS) return GEAR_SUCCESS;

    return GEAR_EXHAUST;
}
