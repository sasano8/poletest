from typing import Generator, Iterable, Tuple

from .exceptions import CanNotCompareError


class ReporterBase:
    def __init__(self, values: tuple):
        if isinstance(values, (Generator, list, map, filter)):
            values = tuple(values)
        elif isinstance(values, ReporterBase):
            values = tuple(values)
        elif isinstance(values, tuple):
            ...
        else:
            raise TypeError(f"Can't create Reporter from {type(values)}")

        self._values = values

    @property
    def values(self):
        return self._values

    def __hash__(self):
        return hash(self.values)

    def __iter__(self):
        return iter(self.values)

    def __len__(self):
        return len(self.values)

    @property
    def types(self):
        types, results, errors_types, errors_results = self.from_values(self)
        return types

    @property
    def items(self):
        types, results, errors_types, errors_results = self.from_values(self)
        return [(t, r) for t, r in zip(types, results)]

    def __eq__(self, other):
        if len(self) == 0:
            raise CanNotCompareError("Can't compare if there are no elements.")
        return self.__class__((other, *self))

    def __ne__(self, other):
        raise NotImplementedError()
        if len(self) == 0:
            raise CanNotCompareError("Can't compare if there are no elements.")
        return self.__class__((other, *self))

    @classmethod
    # @lru_cache(maxsize=3)  # 無限ループに陥ることがある
    def from_values(cls, results: Iterable) -> Tuple[list, list, list, list]:
        if len(results) == 0:
            return [], [], [], []
        else:
            types = [x.__class__ for x in results]
            it_types = iter(types)
            it_result = iter(results)

            base_type = next(it_types)
            base_result = next(it_result)

            errors_types = [False] * len(types)
            errors_results = [False] * len(types)

            for i, type in enumerate(it_types, 1):
                if type is not base_type:
                    errors_types[i] = True

            for i, value in enumerate(it_result, 1):
                if value != base_result:
                    errors_results[i] = True

            return types, results, errors_types, errors_results

    @classmethod
    # @lru_cache(maxsize=3)  # 無限ループに陥ることがある
    def report(cls, results: Iterable) -> Tuple[list, list, list, list]:
        types, results, errors_types, errors_results = cls.from_values(results)
        errors_types = ["mismatch_type" if x else "" for x in errors_types]
        errors_results = ["not_same" if x else "" for x in errors_results]

        arr = []
        for i, row in enumerate(zip(types, results, errors_types, errors_results)):
            typ, value, is_mismatch_type, is_not_same = row
            msg = ",".join(x for x in [is_mismatch_type, is_not_same] if x)
            arr.append((i, msg, typ, value))
        return arr

    def __bool__(self):
        if len(self) == 0:
            raise CanNotCompareError("Can't compare if there are no elements.")

        types, results, errors_types, errors_results = self.from_values(self)
        if any(errors_types) or any(errors_results):
            return False
        else:
            return True

    def __str__(self):
        return str(self.values)

    def __repr__(self):
        return repr(self.values)

    def equals(self, *values) -> bool:
        return self.values == values

    def map(self, func):
        return self.__class__(map(func, self.values))


class Reporter(ReporterBase):
    def __str__(self):
        arr = self.report(self)
        return str(arr)

    def __repr__(self):
        arr = self.report(self)
        query = map(
            lambda row: f"[{row[0]}]: [{row[1]}] - {row[2]!r} - {row[3]!r}", arr
        )
        return "\n".join(query)
