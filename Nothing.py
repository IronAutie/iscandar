from Mode import Mode



class Nothing (Mode):
    "silent mode when bounds exceeded in cube"

    def range    (self):
        "reveal at which this __call__ is invoked"
        return self.inclusive (0, 0)

    def search (self, request, count_planes, count_rows, words,
                count_overall=None):
        """Nothing search: return None, silent, no sweep.

        Nothing is request 0, and the Engine fallback for
        an out-of-table request. It places nothing, marks
        nothing, and fails nothing. Engine returns this
        result, None, directly, without unpacking it as a
        gear tuple. This method is the breakpoint place
        for the silent path."""

        return None

    def __call__ (self, request):
        return 0