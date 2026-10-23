class Mode:
    "associate range of request, with a function to service it"

    def __call__ (self, request):
        "must override, should never be called bare!"

        self.x = 0  # for breakpoints
        return 0


    def inclusive  (self, a, b):
        """The integers a through b, both ends included."""

        return range (a, b + 1)


    @property
    def range (self):
        return range (0, 0)

