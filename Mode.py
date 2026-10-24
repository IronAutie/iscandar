class Mode:
    "associate range of request, with a function to service it"

    def __call__ (self, request):
        "must override, should never be called bare!"

        self.x = 0  # for breakpoints
        return 0


    def search (self, request, count_planes, count_rows, words):
        "Run this mode's search/test pattern against the C gears."

        # The pattern lives on the mode. The base runs the standard
        # single-row pattern: the planes gear over the rows gear,
        # with this mode's probe as the bullet. Modes whose pattern
        # differs (Large, Huge) override search with their own.
        # The outcome shape is uniform across patterns: the raw
        # gear result (status, plane, row, sector), so the engine's
        # translation to Coordinate or mode failure is
        # pattern-independent. That failure mapping is the
        # engine's job, not search's.

        # Local import, as in Engine.mark: the engine still imports
        # without the DLL; only a search call needs it.
        import Gears

        # Adapter: the C path hands the bullet a void* ctx (None
        # from scan). The probe's contract wants the words array
        # as ctx, so the closure supplies it and ignores the C
        # ctx. The sector cell needs no adapter: a C pointer and
        # a Python list cell both take sector_out [0] = value.
        def bullet (plane, row, request, _ctx, sector_out):
            return self (plane, row, request, words, sector_out)

        bullet_fn = Gears.BULLET_FN (bullet)
        return Gears.scan (count_planes, count_rows, request, bullet_fn)


    def inclusive  (self, a, b):
        """The integers a through b, both ends included."""

        return range (a, b + 1)


    @property
    def range (self):
        return range (0, 0)
