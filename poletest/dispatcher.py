from typing import Any, Type

from .equallizer import DefaultEqualizer, Equalizer
from .reporter import Reporter


class Operator:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def __hook__(self, func, args, kwargs):
        results = self.dispatcher(func, *args, **kwargs)
        return results

    def dispatch(self, __funcname, *args, **kwargs):
        return self.__hook__(__funcname, args, kwargs)

    def __len__(self, *args, **kwargs):
        return self.__hook__("__len__", args, kwargs)

    def __iter__(self, *args, **kwargs):
        return self.__hook__("__iter__", args, kwargs)

    def __call__(self, *args, **kwargs):
        return self.__hook__("__call__", args, kwargs)

    def __eq__(self, *args, **kwargs):
        return self.__hook__("__eq__", args, kwargs)


class Dispatcher:
    def __init__(
        self,
        *args: Any,
        equalizer: Equalizer = DefaultEqualizer(),
        reporter: Type = Reporter,
    ):
        self.targes = args
        self.equalizer = equalizer or DefaultEqualizer()
        self.reporter = reporter or Reporter

    def __iter__(self):
        return iter(self.targes)

    def _dispatch(self, __funcname, *args, **kwargs):
        for x in self:
            func = getattr(x, __funcname)
            try:
                result = func(*args, **kwargs)
            except BaseException as e:
                result = self.equalizer.on_error(e)
            yield result

    def dispatch(self, __funcname, *args, **kwargs):
        results = self._dispatch(__funcname, *args, **kwargs)
        on_complete = self.equalizer.on_complete
        results = self.reporter(on_complete(x) for x in results)
        return results

    def __call__(self, __funcname, *args, **kwargs):
        return self.dispatch(__funcname, *args, **kwargs)

    @property
    def op(self):
        return Operator(self)
