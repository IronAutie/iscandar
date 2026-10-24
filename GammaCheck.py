from Geometry import Geometry
from Status import Status


# Harness instrumentation, NOT part of the commit path: the trace
# harness calls these after operations. They guard the assumption
# the C helper leans on -- that the Gamma counters are exact, which
# is what lets middle ranges be checked by their counters instead of
# scanned bit by bit. A drift between bits and books is caught here,
# in the open, instead of being trusted silently.
#
# Failures return a status code, never a description string. All
# code is debug code: the code identifies the failing site, and the
# debugger finds the instance from there. Explanations live in
# comments like these, not in return values.


def _popcount(word):
    # bin().count(): no version dependency (int.bit_count needs 3.10+).
    return bin(word).count("1")


def _row_range(start, count):
    first = start // Geometry.ARITY
    last = (start + count - 1) // Geometry.ARITY
    return first, last


def _plane_range(start, count):
    first = start // (Geometry.ARITY * Geometry.ARITY)
    last = (start + count - 1) // (Geometry.ARITY * Geometry.ARITY)
    return first, last


def verify_block(engine, start, count):
    # Check the Gamma ladder over exactly the rows and planes a
    # block touches, plus the overall counter. First failure wins:
    # fix it, rerun, and the next surfaces. Checked in ladder
    # order -- rows, then planes, then overall -- so a lower
    # failure can explain a higher one.
    if count < 1:
        # Not a ladder failure at all: an empty block is a caller
        # error, so it takes the generic code.
        return Status.FAIL

    words = engine.words
    count_rows = engine.count_rows
    count_planes = engine.count_planes

    first_row, last_row = _row_range(start, count)
    for row in range(first_row, last_row + 1):
        if count_rows[row] != _popcount(words[row]):
            return Status.FAIL_GAMMA_ROW

    first_plane, last_plane = _plane_range(start, count)
    for plane in range(first_plane, last_plane + 1):
        base = plane * Geometry.ARITY
        if count_planes[plane] != sum(
                count_rows[base + i] for i in range(Geometry.ARITY)):
            return Status.FAIL_GAMMA_PLANE

    if engine.count_overall != sum(count_planes):
        return Status.FAIL_GAMMA_OVERALL
    return Status.SUCCESS


def verify(engine):
    # Full-ladder check: every row, every plane, the overall.
    return verify_block(engine, 0, Geometry.ARITY ** 3)
