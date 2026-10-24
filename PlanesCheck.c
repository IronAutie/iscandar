/* PlanesCheck.c -- planes gear: counter gate, row trial, first conviction up.
   The planes gear is mode-neutral, like the rows gear beneath it: it knows
   counters and lanes, never tables. Two handlers travel down the chain:
   the row handler is fired once per qualifying plane, and the item handler
   (the bullet) is passed through the row handler to the rows gear. */

#include <stdint.h>

#define GEAR_SUCCESS 0
#define GEAR_FAIL    1
#define GEAR_EXHAUST 2

#define PLANES_PER_CUBE    32u
#define SECTORS_PER_PLANE  1024u

/* The bullet: a mode's trial. Returns GEAR_SUCCESS with *sector_out set
   on conviction, or the mode's own failure code on acquittal. */
typedef int32_t (*bullet_fn) (uint32_t plane, uint32_t row, uint32_t request,
                              void *ctx, uint32_t *sector_out);

/* The row handler: fired at one plane; it receives the item handler to
   pass down to the rows gear, exactly as in the Python composition. */
typedef int32_t (*row_handler_fn) (const uint32_t *count_rows,
                                   uint32_t plane, uint32_t request,
                                   bullet_fn item_handler, void *ctx,
                                   uint32_t *sector_out, uint32_t *row_out);

/* The rows gear, living in RowsCheck.c: its bullet arrives by bind. */
extern void    rows_gear_bind (bullet_fn bullet, void *ctx);
extern int32_t rows_gear (const uint32_t *count_rows,
                          uint32_t plane, uint32_t request,
                          uint32_t *sector_out, uint32_t *row_out);

/* The adapter: seats the item handler it was handed in the rows gear,
   then fires the rows gear at this plane. Exported so the Python side
   can name it wherever a row_handler_fn is wanted. */
__declspec(dllexport) int32_t rows_row_handler (
    const uint32_t *count_rows,
    uint32_t plane, uint32_t request,
    bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out)
{
    rows_gear_bind (item_handler, ctx);
    return rows_gear (count_rows, plane, request, sector_out, row_out);
}

__declspec(dllexport) int32_t planes_gear (
    const uint32_t *count_planes, const uint32_t *count_rows,
    uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t plane;
    uint32_t remaining;
    int32_t  status;

plane_00:
    plane     = 0;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_01;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_01;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_01:
    plane     = 1;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_02;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_02;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_02:
    plane     = 2;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_03;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_03;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_03:
    plane     = 3;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_04;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_04;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_04:
    plane     = 4;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_05;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_05;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_05:
    plane     = 5;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_06;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_06;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_06:
    plane     = 6;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_07;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_07;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_07:
    plane     = 7;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_08;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_08;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_08:
    plane     = 8;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_09;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_09;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_09:
    plane     = 9;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_10;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_10;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_10:
    plane     = 10;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_11;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_11;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_11:
    plane     = 11;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_12;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_12;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_12:
    plane     = 12;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_13;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_13;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_13:
    plane     = 13;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_14;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_14;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_14:
    plane     = 14;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_15;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_15;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_15:
    plane     = 15;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_16;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_16;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_16:
    plane     = 16;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_17;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_17;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_17:
    plane     = 17;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_18;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_18;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_18:
    plane     = 18;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_19;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_19;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_19:
    plane     = 19;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_20;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_20;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_20:
    plane     = 20;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_21;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_21;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_21:
    plane     = 21;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_22;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_22;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_22:
    plane     = 22;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_23;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_23;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_23:
    plane     = 23;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_24;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_24;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_24:
    plane     = 24;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_25;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_25;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_25:
    plane     = 25;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_26;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_26;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_26:
    plane     = 26;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_27;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_27;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_27:
    plane     = 27;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_28;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_28;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_28:
    plane     = 28;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_29;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_29;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_29:
    plane     = 29;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_30;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_30;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_30:
    plane     = 30;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto plane_31;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto plane_31;
    *plane_out = plane;
    return GEAR_SUCCESS;

plane_31:
    plane     = 31;
    remaining = SECTORS_PER_PLANE - count_planes [plane];
    if (request > remaining) goto exhaust;
    status = row_handler (count_rows, plane, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) goto exhaust;
    *plane_out = plane;
    return GEAR_SUCCESS;

exhaust:
    return GEAR_EXHAUST;
}
