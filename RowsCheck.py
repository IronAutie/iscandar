from Status import SUCCESS, FAIL



class RowsCheck:

    "Examine each row in plane with enough requested sectors"



    def vector2 (self, plane, request, handler, vector1):
        result = [None] * 32
        result [ 0] = handler (plane,  0, request) if vector1 [ 0] is not None else None
        result [ 1] = handler (plane,  1, request) if vector1 [ 1] is not None else None
        result [ 2] = handler (plane,  2, request) if vector1 [ 2] is not None else None
        result [ 3] = handler (plane,  3, request) if vector1 [ 3] is not None else None
        result [ 4] = handler (plane,  4, request) if vector1 [ 4] is not None else None
        result [ 5] = handler (plane,  5, request) if vector1 [ 5] is not None else None
        result [ 6] = handler (plane,  6, request) if vector1 [ 6] is not None else None
        result [ 7] = handler (plane,  7, request) if vector1 [ 7] is not None else None
        result [ 8] = handler (plane,  8, request) if vector1 [ 8] is not None else None
        result [ 9] = handler (plane,  9, request) if vector1 [ 9] is not None else None
        result [10] = handler (plane, 10, request) if vector1 [10] is not None else None
        result [11] = handler (plane, 11, request) if vector1 [11] is not None else None
        result [12] = handler (plane, 12, request) if vector1 [12] is not None else None
        result [13] = handler (plane, 13, request) if vector1 [13] is not None else None
        result [14] = handler (plane, 14, request) if vector1 [14] is not None else None
        result [15] = handler (plane, 15, request) if vector1 [15] is not None else None
        result [16] = handler (plane, 16, request) if vector1 [16] is not None else None
        result [17] = handler (plane, 17, request) if vector1 [17] is not None else None
        result [18] = handler (plane, 18, request) if vector1 [18] is not None else None
        result [19] = handler (plane, 19, request) if vector1 [19] is not None else None
        result [20] = handler (plane, 20, request) if vector1 [20] is not None else None
        result [21] = handler (plane, 21, request) if vector1 [21] is not None else None
        result [22] = handler (plane, 22, request) if vector1 [22] is not None else None
        result [23] = handler (plane, 23, request) if vector1 [23] is not None else None
        result [24] = handler (plane, 24, request) if vector1 [24] is not None else None
        result [25] = handler (plane, 25, request) if vector1 [25] is not None else None
        result [26] = handler (plane, 26, request) if vector1 [26] is not None else None
        result [27] = handler (plane, 27, request) if vector1 [27] is not None else None
        result [28] = handler (plane, 28, request) if vector1 [28] is not None else None
        result [29] = handler (plane, 29, request) if vector1 [29] is not None else None
        result [30] = handler (plane, 30, request) if vector1 [30] is not None else None
        result [31] = handler (plane, 31, request) if vector1 [31] is not None else None
        return result



    def vector0 (self, plane, request, handler):

        vector1 = [None] * 32
        vector1 [ 0] = True if request <= remaining_in_row ( 0) else None
        vector1 [ 1] = True if request <= remaining_in_row ( 1) else None
        vector1 [ 2] = True if request <= remaining_in_row ( 2) else None
        vector1 [ 3] = True if request <= remaining_in_row ( 3) else None
        vector1 [ 4] = True if request <= remaining_in_row ( 4) else None
        vector1 [ 5] = True if request <= remaining_in_row ( 5) else None
        vector1 [ 6] = True if request <= remaining_in_row ( 6) else None
        vector1 [ 7] = True if request <= remaining_in_row ( 7) else None
        vector1 [ 8] = True if request <= remaining_in_row ( 8) else None
        vector1 [ 9] = True if request <= remaining_in_row ( 9) else None
        vector1 [10] = True if request <= remaining_in_row (10) else None
        vector1 [11] = True if request <= remaining_in_row (11) else None
        vector1 [12] = True if request <= remaining_in_row (12) else None
        vector1 [13] = True if request <= remaining_in_row (13) else None
        vector1 [14] = True if request <= remaining_in_row (14) else None
        vector1 [15] = True if request <= remaining_in_row (15) else None
        vector1 [16] = True if request <= remaining_in_row (16) else None
        vector1 [17] = True if request <= remaining_in_row (17) else None
        vector1 [18] = True if request <= remaining_in_row (18) else None
        vector1 [19] = True if request <= remaining_in_row (19) else None
        vector1 [20] = True if request <= remaining_in_row (20) else None
        vector1 [21] = True if request <= remaining_in_row (21) else None
        vector1 [22] = True if request <= remaining_in_row (22) else None
        vector1 [23] = True if request <= remaining_in_row (23) else None
        vector1 [24] = True if request <= remaining_in_row (24) else None
        vector1 [25] = True if request <= remaining_in_row (25) else None
        vector1 [26] = True if request <= remaining_in_row (26) else None
        vector1 [27] = True if request <= remaining_in_row (27) else None
        vector1 [28] = True if request <= remaining_in_row (28) else None
        vector1 [29] = True if request <= remaining_in_row (29) else None
        vector1 [30] = True if request <= remaining_in_row (30) else None
        vector1 [31] = True if request <= remaining_in_row (31) else None
        return vector1

