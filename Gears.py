# Gears.py -- the Python side of the C gears (RowsCheck.c +
# PlanesCheck.c, PairsRowDriver.c + PlaneSmallDriver.c for Small,
# and Mark.c + Unmark.c for the commit path).
# Build the DLL once, in the engine folder, with all C files together:
#     cl /LD RowsCheck.c PlanesCheck.c PairsRowDriver.c PlaneSmallDriver.c
# which produces RowsCheck.dll holding all gears. Importing this module
# loads the DLL and asserts the ABI version before anything calls it.

import ctypes, os

from Status import Status

_here = os.path.dirname (os.path.abspath (__file__))
lib   = ctypes.CDLL (os.path.join (_here, "RowsCheck.dll"))

# Status values come from Status.py, the canonical home -- never
# hand-written here, so the Python side cannot drift from C.
SUCCESS, FAIL, EXHAUST = (Status.GEAR_SUCCESS, Status.GEAR_FAIL,
                            Status.GEAR_EXHAUST)

BULLET_FN = ctypes.CFUNCTYPE (
    ctypes.c_int32,
    ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32,
    ctypes.c_void_p, ctypes.POINTER (ctypes.c_uint32))

ROW_HANDLER_FN = ctypes.CFUNCTYPE (
    ctypes.c_int32,
    ctypes.POINTER (ctypes.c_uint32), ctypes.c_uint32, ctypes.c_uint32,
    BULLET_FN, ctypes.c_void_p,
    ctypes.POINTER (ctypes.c_uint32), ctypes.POINTER (ctypes.c_uint32))

lib.gear_abi_version.restype  = ctypes.c_int32
lib.rows_gear_bind.argtypes   = [BULLET_FN, ctypes.c_void_p]
lib.rows_gear_bind.restype    = None
lib.rows_gear.argtypes        = [ctypes.POINTER (ctypes.c_uint32), ctypes.c_uint32,
                                 ctypes.c_uint32, ctypes.POINTER (ctypes.c_uint32),
                                 ctypes.POINTER (ctypes.c_uint32)]
lib.rows_gear.restype         = ctypes.c_int32
lib.rows_row_handler.argtypes = [ctypes.POINTER (ctypes.c_uint32), ctypes.c_uint32,
                                 ctypes.c_uint32, BULLET_FN, ctypes.c_void_p,
                                 ctypes.POINTER (ctypes.c_uint32),
                                 ctypes.POINTER (ctypes.c_uint32)]
lib.rows_row_handler.restype  = ctypes.c_int32
lib.planes_gear.argtypes      = [ctypes.POINTER (ctypes.c_uint32),
                                 ctypes.POINTER (ctypes.c_uint32), ctypes.c_uint32,
                                 ROW_HANDLER_FN, BULLET_FN, ctypes.c_void_p,
                                 ctypes.POINTER (ctypes.c_uint32),
                                 ctypes.POINTER (ctypes.c_uint32),
                                 ctypes.POINTER (ctypes.c_uint32)]
lib.planes_gear.restype       = ctypes.c_int32
lib.planes_small_gear_bind.argtypes = [BULLET_FN, ctypes.c_void_p]
lib.planes_small_gear_bind.restype  = None
lib.planes_small_gear.argtypes = [ctypes.POINTER (ctypes.c_uint32),
                                  ctypes.POINTER (ctypes.c_uint32), ctypes.c_uint32,
                                  ctypes.POINTER (ctypes.c_uint32),
                                  ctypes.POINTER (ctypes.c_uint32),
                                  ctypes.POINTER (ctypes.c_uint32)]
lib.planes_small_gear.restype  = ctypes.c_int32
lib.pairs_gear_bind.argtypes = [BULLET_FN, ctypes.c_void_p]
lib.pairs_gear_bind.restype  = None
lib.pairs_gear.argtypes = [ctypes.POINTER (ctypes.c_uint32), ctypes.c_uint32,
                           ctypes.POINTER (ctypes.c_uint32),
                           ctypes.POINTER (ctypes.c_uint32),
                           ctypes.POINTER (ctypes.c_uint32)]
lib.pairs_gear.restype  = ctypes.c_int32

assert lib.gear_abi_version () == 1, "gear ABI mismatch"

# The exported adapter in PlanesCheck.c, dressed as a row_handler_fn so it
# can be passed wherever a row handler is wanted: it binds the item handler
# it is handed, then fires the rows gear at its plane.
rows_row_handler = ROW_HANDLER_FN (
    ctypes.cast (lib.rows_row_handler, ctypes.c_void_p).value)

def _u32 (counters):
    assert counters.itemsize == 4
    return ctypes.cast (counters.buffer_info () [0],
                        ctypes.POINTER (ctypes.c_uint32))

def scan (count_planes, count_rows, request, bullet_cb):
    sector = ctypes.c_uint32 ()
    row    = ctypes.c_uint32 ()
    plane  = ctypes.c_uint32 ()
    status = lib.planes_gear (_u32 (count_planes), _u32 (count_rows), request,
                              rows_row_handler, bullet_cb, None,
                              ctypes.byref (sector), ctypes.byref (row),
                              ctypes.byref (plane))
    return status, plane.value, row.value, sector.value

def scan_small (count_planes, count_rows, request, bullet_cb):
    """ Small search through the separate planes-small gear.

    The gear binds the bullet once, then sweeps planes with
    pairs_row_handler, first conviction up. Planes-pair gate,
    verbatim (user, 2026-10-25): a pair of planes passes iff
    plane n has at least 1 sector free and plane n+1 has at
    least (request - 1) sectors free; plane 31, which has no
    next plane, is tried only when its own free reaches the
    request.
    Return shape is the same raw tuple as scan, so the engine's
    translation to Coordinate or mode failure is unchanged.
    """
    sector = ctypes.c_uint32 ()
    row    = ctypes.c_uint32 ()
    plane  = ctypes.c_uint32 ()
    lib.planes_small_gear_bind (bullet_cb, None)
    status = lib.planes_small_gear (_u32 (count_planes), _u32 (count_rows), request,
                                    ctypes.byref (sector), ctypes.byref (row),
                                    ctypes.byref (plane))
    return status, plane.value, row.value, sector.value

def scan_pairs (count_rows, request, bullet_cb):
    """ Small search through the standalone global pairs gear.

    Pinned pivot sweep 0..1022, first conviction up. Kept for
    completeness alongside scan_small; Small.search uses
    scan_small, the separate gear, as decided.
    """
    sector = ctypes.c_uint32 ()
    row    = ctypes.c_uint32 ()
    plane  = ctypes.c_uint32 ()
    lib.pairs_gear_bind (bullet_cb, None)
    status = lib.pairs_gear (_u32 (count_rows), request,
                             ctypes.byref (sector), ctypes.byref (row),
                             ctypes.byref (plane))
    return status, plane.value, row.value, sector.value

lib.mark_sectors.argtypes = [ctypes.POINTER (ctypes.c_uint32),
                             ctypes.POINTER (ctypes.c_uint32),
                             ctypes.POINTER (ctypes.c_uint32),
                             ctypes.c_uint32, ctypes.c_uint32]
lib.mark_sectors.restype = ctypes.c_int32
lib.unmark_sectors.argtypes = [ctypes.POINTER (ctypes.c_uint32),
                               ctypes.POINTER (ctypes.c_uint32),
                               ctypes.POINTER (ctypes.c_uint32),
                               ctypes.c_uint32, ctypes.c_uint32]
lib.unmark_sectors.restype = ctypes.c_int32


def mark_sectors (sectors, count_rows, count_planes, start, count):
    """ Mark a block through the C marker (Mark.c). Returns the
    C status; the caller owns the overall counter. """
    return lib.mark_sectors (_u32 (sectors), _u32 (count_rows),
                             _u32 (count_planes), start, count)


def unmark_sectors (sectors, count_rows, count_planes, start, count):
    """ Unmark a block through the C unmarker (Unmark.c). """
    return lib.unmark_sectors (_u32 (sectors), _u32 (count_rows),
                               _u32 (count_planes), start, count)
