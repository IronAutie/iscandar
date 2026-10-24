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

    """Gear statuses (used across the C boundary by Gears.py and
    the gears themselves; same numbering shape, separate names, so
    a gear outcome can never be mistaken for a mode outcome):
    """

    GEAR_SUCCESS = 0
    GEAR_FAIL    = 1
    GEAR_EXHAUST = 2
