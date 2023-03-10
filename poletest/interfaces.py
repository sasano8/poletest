from functools import partial


class IDispatcher:
    def __init__(self, *targets) -> None:
        self.targets = targets

    def __iter__(self):
        return iter(self.targets)

    def dispatch(self, __funcname, *args, **kwargs):
        for x in self:
            func = getattr(x, __funcname)
            result = partial(func, *args, **kwargs)
            yield result

    def __call__(self, __funcname, *args, **kwargs):
        raise NotImplementedError()


class IEqualizer:
    def handle(self, funcs):
        for func in funcs:
            try:
                result = func()
            except BaseException as e:
                result = self.on_error(e)

            result = self.on_complete(result)
            yield result

    def on_error(self, exc: BaseException):
        raise NotImplementedError()

    def on_complete(self, result):
        raise NotImplementedError()


class IReporter:
    def __init__(self, dispatcher, equalizer):
        ...
