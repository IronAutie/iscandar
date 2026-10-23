from Mode import Mode



class Nothing (Mode):
    "silent mode when bounds exceeded in cube"

    def range    (self)
        "reveal at which this __call__ is invoked"
        return self.inclusive (0, 0)

    def __call__ (self, request):
        return 0