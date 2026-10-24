/* PlanesCheck.c -- planes gear, rotated sweep (2026-10-24):
   32 lane procedures called via pointers from the driver procedure.
   Each lane encloses one plane's gate and row trial; a lane returns
   GEAR_SUCCESS on conviction, GEAR_EXHAUST when this plane has nothing
   (gate skip or row handler without conviction -- mapping (a), exact
   preservation of the goto version's behavior).
   ROTATED SWEEP: a function-local static start cursor inside planes_gear
   advances by one lane on every entry (wrapping 31 -> 0). The driver
   walks 32 guarded unrolled statements from start, wrapping back to
   lane 0, so every lane is tried exactly once and GEAR_EXHAUST still
   means the whole cube was searched. Single-threaded working assumption
   (embedded origin). Committed 2026-10-24, tagged Rotate. */



#include <stdint.h>
#include "status.h"

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


/* Lane 00: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_00_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [0];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 0, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 0;
    return GEAR_SUCCESS;
}

/* Lane 01: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_01_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [1];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 1, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 1;
    return GEAR_SUCCESS;
}

/* Lane 02: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_02_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [2];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 2, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 2;
    return GEAR_SUCCESS;
}

/* Lane 03: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_03_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [3];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 3, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 3;
    return GEAR_SUCCESS;
}

/* Lane 04: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_04_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [4];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 4, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 4;
    return GEAR_SUCCESS;
}

/* Lane 05: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_05_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [5];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 5, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 5;
    return GEAR_SUCCESS;
}

/* Lane 06: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_06_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [6];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 6, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 6;
    return GEAR_SUCCESS;
}

/* Lane 07: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_07_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [7];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 7, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 7;
    return GEAR_SUCCESS;
}

/* Lane 08: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_08_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [8];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 8, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 8;
    return GEAR_SUCCESS;
}

/* Lane 09: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_09_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [9];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 9, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 9;
    return GEAR_SUCCESS;
}

/* Lane 10: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_10_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [10];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 10, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 10;
    return GEAR_SUCCESS;
}

/* Lane 11: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_11_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [11];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 11, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 11;
    return GEAR_SUCCESS;
}

/* Lane 12: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_12_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [12];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 12, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 12;
    return GEAR_SUCCESS;
}

/* Lane 13: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_13_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [13];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 13, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 13;
    return GEAR_SUCCESS;
}

/* Lane 14: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_14_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [14];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 14, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 14;
    return GEAR_SUCCESS;
}

/* Lane 15: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_15_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [15];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 15, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 15;
    return GEAR_SUCCESS;
}

/* Lane 16: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_16_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [16];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 16, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 16;
    return GEAR_SUCCESS;
}

/* Lane 17: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_17_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [17];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 17, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 17;
    return GEAR_SUCCESS;
}

/* Lane 18: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_18_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [18];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 18, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 18;
    return GEAR_SUCCESS;
}

/* Lane 19: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_19_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [19];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 19, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 19;
    return GEAR_SUCCESS;
}

/* Lane 20: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_20_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [20];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 20, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 20;
    return GEAR_SUCCESS;
}

/* Lane 21: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_21_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [21];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 21, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 21;
    return GEAR_SUCCESS;
}

/* Lane 22: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_22_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [22];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 22, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 22;
    return GEAR_SUCCESS;
}

/* Lane 23: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_23_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [23];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 23, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 23;
    return GEAR_SUCCESS;
}

/* Lane 24: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_24_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [24];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 24, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 24;
    return GEAR_SUCCESS;
}

/* Lane 25: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_25_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [25];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 25, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 25;
    return GEAR_SUCCESS;
}

/* Lane 26: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_26_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [26];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 26, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 26;
    return GEAR_SUCCESS;
}

/* Lane 27: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_27_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [27];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 27, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 27;
    return GEAR_SUCCESS;
}

/* Lane 28: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_28_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [28];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 28, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 28;
    return GEAR_SUCCESS;
}

/* Lane 29: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_29_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [29];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 29, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 29;
    return GEAR_SUCCESS;
}

/* Lane 30: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_30_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [30];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 30, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 30;
    return GEAR_SUCCESS;
}

/* Lane 31: this plane's gate, row trial, and conviction, enclosed. */
static int32_t plane_31_lane (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    uint32_t remaining;
    int32_t  status;

    remaining = SECTORS_PER_PLANE - count_planes [31];
    if (request > remaining) return GEAR_EXHAUST;
    status = row_handler (count_rows, 31, request,
                          item_handler, ctx, sector_out, row_out);
    if (status != GEAR_SUCCESS) return GEAR_EXHAUST;
    *plane_out = 31;
    return GEAR_SUCCESS;
}

/* The sweep order, as data: lane N sits at index N. */
typedef int32_t (*plane_lane_fn) (const uint32_t *count_planes,
    const uint32_t *count_rows, uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out);

static const plane_lane_fn planes_lanes [PLANES_PER_CUBE] = {
    plane_00_lane,
    plane_01_lane,
    plane_02_lane,
    plane_03_lane,
    plane_04_lane,
    plane_05_lane,
    plane_06_lane,
    plane_07_lane,
    plane_08_lane,
    plane_09_lane,
    plane_10_lane,
    plane_11_lane,
    plane_12_lane,
    plane_13_lane,
    plane_14_lane,
    plane_15_lane,
    plane_16_lane,
    plane_17_lane,
    plane_18_lane,
    plane_19_lane,
    plane_20_lane,
    plane_21_lane,
    plane_22_lane,
    plane_23_lane,
    plane_24_lane,
    plane_25_lane,
    plane_26_lane,
    plane_27_lane,
    plane_28_lane,
    plane_29_lane,
    plane_30_lane,
    plane_31_lane,
};

__declspec(dllexport) int32_t planes_gear (    const uint32_t *count_planes, const uint32_t *count_rows,
    uint32_t request,
    row_handler_fn row_handler, bullet_fn item_handler, void *ctx,
    uint32_t *sector_out, uint32_t *row_out, uint32_t *plane_out)
{
    static const plane_lane_fn *start = planes_lanes;
    const plane_lane_fn *end = planes_lanes + PLANES_PER_CUBE;
    const plane_lane_fn *lane;
    int32_t  status;

    start++;
    if (start >= end) start = planes_lanes;
    lane = start;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    if (lane >= end) lane = planes_lanes;
    status = (*lane++)(count_planes, count_rows, request,
                       row_handler, item_handler, ctx,
                       sector_out, row_out, plane_out);
    if (status == GEAR_SUCCESS) return GEAR_SUCCESS;
    return GEAR_EXHAUST;
}
