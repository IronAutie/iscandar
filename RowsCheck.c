/* gear.c -- rows gear: counter gate, bullet trial, first conviction up.
   The gear is mode-neutral: it knows counters and lanes, never tables.
   Mode knowledge lives in the bullet, bound once through rows_gear_bind. */

#include <stdint.h>

#define GEAR_SUCCESS 0
#define GEAR_FAIL    1

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
    uint32_t remaining;
    int32_t  status;

    if (handler_callback == 0)
        return GEAR_FAIL;

    base = plane * ROWS_PER_PLANE;

    for (row = 0; row < ROWS_PER_PLANE; row++)
    {
        remaining = SECTORS_PER_ROW - count_rows [base + row];
        if (request <= remaining)
        {
            status = handler_callback (plane, row, request,
                                       handler_ctx, sector_out);
            if (status == GEAR_SUCCESS)
            {
                *row_out = row;
                return GEAR_SUCCESS;
            }
            /* acquittal: the gearing survives, the procession resumes */
        }
    }

    return GEAR_FAIL;
}
