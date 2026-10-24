from Status     import Status
from Coordinate import Coordinate



class PlanesCheck:

    """
    Examine each plane in cube with enough requested sectors.
    This is done as a handcoded procession for determinism.
    """

    def vector3 (self, vector2):

        'return first qualifying result'

        if isinstance (vector2 [ 0], Coordinate): return vector2 [ 0]
        if isinstance (vector2 [ 1], Coordinate): return vector2 [ 1]
        if isinstance (vector2 [ 2], Coordinate): return vector2 [ 2]
        if isinstance (vector2 [ 3], Coordinate): return vector2 [ 3]
        if isinstance (vector2 [ 4], Coordinate): return vector2 [ 4]
        if isinstance (vector2 [ 5], Coordinate): return vector2 [ 5]
        if isinstance (vector2 [ 6], Coordinate): return vector2 [ 6]
        if isinstance (vector2 [ 7], Coordinate): return vector2 [ 7]
        if isinstance (vector2 [ 8], Coordinate): return vector2 [ 8]
        if isinstance (vector2 [ 9], Coordinate): return vector2 [ 9]
        if isinstance (vector2 [10], Coordinate): return vector2 [10]
        if isinstance (vector2 [11], Coordinate): return vector2 [11]
        if isinstance (vector2 [12], Coordinate): return vector2 [12]
        if isinstance (vector2 [13], Coordinate): return vector2 [13]
        if isinstance (vector2 [14], Coordinate): return vector2 [14]
        if isinstance (vector2 [15], Coordinate): return vector2 [15]
        if isinstance (vector2 [16], Coordinate): return vector2 [16]
        if isinstance (vector2 [17], Coordinate): return vector2 [17]
        if isinstance (vector2 [18], Coordinate): return vector2 [18]
        if isinstance (vector2 [19], Coordinate): return vector2 [19]
        if isinstance (vector2 [20], Coordinate): return vector2 [20]
        if isinstance (vector2 [21], Coordinate): return vector2 [21]
        if isinstance (vector2 [22], Coordinate): return vector2 [22]
        if isinstance (vector2 [23], Coordinate): return vector2 [23]
        if isinstance (vector2 [24], Coordinate): return vector2 [24]
        if isinstance (vector2 [25], Coordinate): return vector2 [25]
        if isinstance (vector2 [26], Coordinate): return vector2 [26]
        if isinstance (vector2 [27], Coordinate): return vector2 [27]
        if isinstance (vector2 [28], Coordinate): return vector2 [28]
        if isinstance (vector2 [29], Coordinate): return vector2 [29]
        if isinstance (vector2 [30], Coordinate): return vector2 [30]
        if isinstance (vector2 [31], Coordinate): return vector2 [31]
        return Status.FAIL


    def vector2 (self, plane, request, row_handler, item_handler, vector1):

        'apply row_handler to any qualifying plane'

        result = [None] * 32
        result [ 0] = row_handler (0, request, item_handler) if vector1 [ 0] is not None else None
        result [ 1] = row_handler (1, request, item_handler) if vector1 [ 1] is not None else None
        result [ 2] = row_handler (2, request, item_handler) if vector1 [ 2] is not None else None
        result [ 3] = row_handler (3, request, item_handler) if vector1 [ 3] is not None else None
        result [ 4] = row_handler (4, request, item_handler) if vector1 [ 4] is not None else None
        result [ 5] = row_handler (5, request, item_handler) if vector1 [ 5] is not None else None
        result [ 6] = row_handler (6, request, item_handler) if vector1 [ 6] is not None else None
        result [ 7] = row_handler (7, request, item_handler) if vector1 [ 7] is not None else None
        result [ 8] = row_handler (8, request, item_handler) if vector1 [ 8] is not None else None
        result [ 9] = row_handler (9, request, item_handler) if vector1 [ 9] is not None else None
        result [10] = row_handler (10, request, item_handler) if vector1 [10] is not None else None
        result [11] = row_handler (11, request, item_handler) if vector1 [11] is not None else None
        result [12] = row_handler (12, request, item_handler) if vector1 [12] is not None else None
        result [13] = row_handler (13, request, item_handler) if vector1 [13] is not None else None
        result [14] = row_handler (14, request, item_handler) if vector1 [14] is not None else None
        result [15] = row_handler (15, request, item_handler) if vector1 [15] is not None else None
        result [16] = row_handler (16, request, item_handler) if vector1 [16] is not None else None
        result [17] = row_handler (17, request, item_handler) if vector1 [17] is not None else None
        result [18] = row_handler (18, request, item_handler) if vector1 [18] is not None else None
        result [19] = row_handler (19, request, item_handler) if vector1 [19] is not None else None
        result [20] = row_handler (20, request, item_handler) if vector1 [20] is not None else None
        result [21] = row_handler (21, request, item_handler) if vector1 [21] is not None else None
        result [22] = row_handler (22, request, item_handler) if vector1 [22] is not None else None
        result [23] = row_handler (23, request, item_handler) if vector1 [23] is not None else None
        result [24] = row_handler (24, request, item_handler) if vector1 [24] is not None else None
        result [25] = row_handler (25, request, item_handler) if vector1 [25] is not None else None
        result [26] = row_handler (26, request, item_handler) if vector1 [26] is not None else None
        result [27] = row_handler (27, request, item_handler) if vector1 [27] is not None else None
        result [28] = row_handler (28, request, item_handler) if vector1 [28] is not None else None
        result [29] = row_handler (29, request, item_handler) if vector1 [29] is not None else None
        result [30] = row_handler (30, request, item_handler) if vector1 [30] is not None else None
        result [31] = row_handler (31, request, item_handler) if vector1 [31] is not None else None
        return result


    def vector1 (self, plane, request, row_handler, item_handler):

        'check lanes for sufficient room to fulfil request'

        result = [None] * 32
        result [ 0] = True if request <= remaining_in_plane (0) else None
        result [ 1] = True if request <= remaining_in_plane (1) else None
        result [ 2] = True if request <= remaining_in_plane (2) else None
        result [ 3] = True if request <= remaining_in_plane (3) else None
        result [ 4] = True if request <= remaining_in_plane (4) else None
        result [ 5] = True if request <= remaining_in_plane (5) else None
        result [ 6] = True if request <= remaining_in_plane (6) else None
        result [ 7] = True if request <= remaining_in_plane (7) else None
        result [ 8] = True if request <= remaining_in_plane (8) else None
        result [ 9] = True if request <= remaining_in_plane (9) else None
        result [10] = True if request <= remaining_in_plane (10) else None
        result [11] = True if request <= remaining_in_plane (11) else None
        result [12] = True if request <= remaining_in_plane (12) else None
        result [13] = True if request <= remaining_in_plane (13) else None
        result [14] = True if request <= remaining_in_plane (14) else None
        result [15] = True if request <= remaining_in_plane (15) else None
        result [16] = True if request <= remaining_in_plane (16) else None
        result [17] = True if request <= remaining_in_plane (17) else None
        result [18] = True if request <= remaining_in_plane (18) else None
        result [19] = True if request <= remaining_in_plane (19) else None
        result [20] = True if request <= remaining_in_plane (20) else None
        result [21] = True if request <= remaining_in_plane (21) else None
        result [22] = True if request <= remaining_in_plane (22) else None
        result [23] = True if request <= remaining_in_plane (23) else None
        result [24] = True if request <= remaining_in_plane (24) else None
        result [25] = True if request <= remaining_in_plane (25) else None
        result [26] = True if request <= remaining_in_plane (26) else None
        result [27] = True if request <= remaining_in_plane (27) else None
        result [28] = True if request <= remaining_in_plane (28) else None
        result [29] = True if request <= remaining_in_plane (29) else None
        result [30] = True if request <= remaining_in_plane (30) else None
        result [31] = True if request <= remaining_in_plane (31) else None
        return result


    def __call__ (self, plane, request, row_handler, item_handler):

        result = self.vector1 (plane, request, row_handler, item_handler) 
        result = self.vector2 (plane, request, row_handler, item_handler, result)
        return   self.vector3 (result)