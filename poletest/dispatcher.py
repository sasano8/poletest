from typing import Any, Type

from .equallizer import DefaultEqualizer
from .interfaces import IDispatcher, IEqualizer
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


class Dispatcher(IDispatcher):
    def __init__(
        self,
        *args: Any,
        equalizer: IEqualizer = DefaultEqualizer(),
        reporter: Type = Reporter,
    ):
        self.targes = args
        self.equalizer = equalizer or DefaultEqualizer()
        self.reporter = reporter or Reporter

    def __iter__(self):
        return iter(self.targes)

    def dispatch(self, __funcname, *args, **kwargs):
        funcs = self._dispatch(__funcname, *args, **kwargs)
        results = self.equalizer.handle(funcs)
        results = self.reporter(results)
        return results

    def __call__(self, __funcname, *args, **kwargs):
        return self.dispatch(__funcname, *args, **kwargs)

    @property
    def op(self):
        return Operator(self)
