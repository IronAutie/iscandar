/* RowsCheck.c -- rows gear: counter gate, bullet trial, first conviction up.
   The gear is mode-neutral: it knows counters and lanes, never tables.
   Mode knowledge lives in the bullet, bound once through rows_gear_bind. */

#include <stdint.h>

#define GEAR_SUCCESS 0
#define GEAR_FAIL    1
#define GEAR_EXHAUST 2

#define ROWS_PER_PLANE   32u
#define SECTORS_PER_ROW  32u

/* The bullet: a mode's trial. Returns GEAR_SUCCESS with *sector_out set
   on conviction, or the mode's own failure code on acquittal. */
typedef int32_t (*bullet_fn) (uint32_t plane, uint32_t row, uint32_t request,
                              void *ctx, uint32_t *sector_out);

/* The gearing's surviving state: the seated handler and its context. */
static bullet_fn handler_callback = 0;
static void     *handler_ctx      = 0;

__declspec(dllexport) int32_t gear_abi_version (void)
{
    return 1;
}

__declspec(dllexport) void rows_gear_bind (bullet_fn bullet, void *ctx)
{
    handler_callback = bullet;
    handler_ctx      = ctx;
}

__declspec(dllexport) int32_t rows_gear (
    const uint32_t *count_rows,
    uint32_t plane, uint32_t request,
    uint32_t *sector_out, uint32_t *row_out)
{
    uint32_t row;
    uint32_t base;
    uint32_t at;

    uint32_t remaining;
    int32_t  status;

    if (handler_callback == 0)
        return GEAR_FAIL;

    base      = plane * ROWS_PER_PLANE;

row_00:
    row       = 0;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_01;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_01;
    *row_out = row;
    return GEAR_SUCCESS;

row_01:
    row       = 1;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_02;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_02;
    *row_out = row;
    return GEAR_SUCCESS;

row_02:
    row       = 2;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_03;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_03;
    *row_out = row;
    return GEAR_SUCCESS;

row_03:
    row       = 3;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_04;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_04;
    *row_out = row;
    return GEAR_SUCCESS;

row_04:
    row       = 4;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_05;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_05;
    *row_out = row;
    return GEAR_SUCCESS;

row_05:
    row       = 5;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_06;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_06;
    *row_out = row;
    return GEAR_SUCCESS;

row_06:
    row       = 6;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_07;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_07;
    *row_out = row;
    return GEAR_SUCCESS;

row_07:
    row       = 7;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_08;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_08;
    *row_out = row;
    return GEAR_SUCCESS;

row_08:
    row       = 8;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_09;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_09;
    *row_out = row;
    return GEAR_SUCCESS;

row_09:
    row       = 9;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_10;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_10;
    *row_out = row;
    return GEAR_SUCCESS;

row_10:
    row       = 10;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_11;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_11;
    *row_out = row;
    return GEAR_SUCCESS;

row_11:
    row       = 11;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_12;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_12;
    *row_out = row;
    return GEAR_SUCCESS;

row_12:
    row       = 12;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_13;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_13;
    *row_out = row;
    return GEAR_SUCCESS;

row_13:
    row       = 13;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_14;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_14;
    *row_out = row;
    return GEAR_SUCCESS;

row_14:
    row       = 14;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_15;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_15;
    *row_out = row;
    return GEAR_SUCCESS;

row_15:
    row       = 15;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_16;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_16;
    *row_out = row;
    return GEAR_SUCCESS;

row_16:
    row       = 16;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_17;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_17;
    *row_out = row;
    return GEAR_SUCCESS;

row_17:
    row       = 17;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_18;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_18;
    *row_out = row;
    return GEAR_SUCCESS;

row_18:
    row       = 18;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_19;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_19;
    *row_out = row;
    return GEAR_SUCCESS;

row_19:
    row       = 19;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_20;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_20;
    *row_out = row;
    return GEAR_SUCCESS;

row_20:
    row       = 20;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_21;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_21;
    *row_out = row;
    return GEAR_SUCCESS;

row_21:
    row       = 21;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_22;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_22;
    *row_out = row;
    return GEAR_SUCCESS;

row_22:
    row       = 22;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_23;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_23;
    *row_out = row;
    return GEAR_SUCCESS;

row_23:
    row       = 23;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_24;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_24;
    *row_out = row;
    return GEAR_SUCCESS;

row_24:
    row       = 24;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_25;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_25;
    *row_out = row;
    return GEAR_SUCCESS;

row_25:
    row       = 25;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_26;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_26;
    *row_out = row;
    return GEAR_SUCCESS;

row_26:
    row       = 26;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_27;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_27;
    *row_out = row;
    return GEAR_SUCCESS;

row_27:
    row       = 27;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_28;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_28;
    *row_out = row;
    return GEAR_SUCCESS;

row_28:
    row       = 28;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_29;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_29;
    *row_out = row;
    return GEAR_SUCCESS;

row_29:
    row       = 29;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_30;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_30;
    *row_out = row;
    return GEAR_SUCCESS;

row_30:
    row       = 30;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto row_31;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto row_31;
    *row_out = row;
    return GEAR_SUCCESS;

row_31:
    row       = 31;
    at        = base + row;
    remaining = SECTORS_PER_ROW - count_rows [at];
    if (request > remaining) goto exhaust;
    status = handler_callback (plane, row, request, handler_ctx, sector_out);
    if (status != GEAR_SUCCESS) goto exhaust;
    *row_out = row;
    return GEAR_SUCCESS;

exhaust:
    return GEAR_EXHAUST;
}