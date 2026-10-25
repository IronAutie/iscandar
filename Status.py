class Status:
    """System status codes -- the ONE canonical home for them.

    Rule: a new status is added here, one line, and nowhere else.
    gen_status.py turns exactly these lines into status.h for the
    C gears, so the two languages can never drift apart. Never
    hand-edit status.h, and never hand-write a status value in
    Gears.py or in a C file: import or include it instead.

    Engine / mode statuses (used by Python callers):
    """

    SUCCESS   = 0
    FAIL      = 1
    NANO_FAIL = 2
    KEYRANGE  = 3  # index/key out of range (views raise IndexError;
                   # the engine boundary converts it to this status)
    FAIL_OVERLAY = 4  # check-then-set failure on the commit path: a
                      # mark landing on occupied bits (or an unmark
                      # clearing clear ones) -- a misdesign, never
                      # tolerated silently
    FAIL_GAMMA_ROW = 5  # Gamma ladder: a row counter disagrees with
                        # the popcount of its row word
    FAIL_GAMMA_PLANE = 6  # Gamma ladder: a plane counter disagrees
                          # with the sum of its row counters
    FAIL_GAMMA_OVERALL = 7  # Gamma ladder: the overall counter
                            # disagrees with the sum of plane counters
    TINY_FAIL = 9  # Tiny probe acquittal: no Left run of at least 9
                   # reaching the request, and no sufficient tail run
    SMALL_FAIL = 10  # Small probe acquittal: no tail + head pair
                     # reaching the request (either edge missing,
                     # or P + Q < request). Not the paper's APL
                     # FAIL_SMALL 6, which collides with
                     # FAIL_GAMMA_PLANE.

    """Gear statuses (used across the C boundary by Gears.py and
    the gears themselves; separate names, and a nonzero success,
    so a gear outcome can never be mistaken for a mode outcome,
    not even numerically):
    """

    GEAR_SUCCESS = 8
    GEAR_FAIL    = 1
    GEAR_EXHAUST = 2
