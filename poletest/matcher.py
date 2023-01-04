from typing import Generator, Type


class Raised:
    def __init__(self, cls: Type, msg: str):
        self.cls = cls
        self.msg = msg

    def __hash__(self):
        return hash((self.cls, self.msg))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Raised):
            return False
        else:
            if not issubclass(other.cls, self.cls):
                return False
            else:
                return self.msg == other.msg

    def __repr__(self) -> str:
        return f"Raised({self.cls.__name__}, {self.msg!r})"


class Generated:
    """Generator型に一致し、かつ、遅延評価後の値を検証するための特殊な型"""

    def __init__(self, iterable):
        if isinstance(iterable, Generator):
            iterable = list(iterable)
        elif isinstance(iterable, (list, set, tuple)):
            ...
        else:
            raise TypeError(
                f"iterable must be Generator or list, set, tuple, but {type(iterable)}"
            )

        self.iterable = iterable

    def __len__(self):
        return len(self.iterable)

    def __iter__(self):
        return iter(self.iterable)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Generated):
            return False
        else:
            return self.iterable == other.iterable

    def __repr__(self) -> str:
        return f"Generated({self.iterable!r})"
