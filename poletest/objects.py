from typing import Type


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

            if self.msg != other.msg:
                return False

            return True

    def __repr__(self) -> str:
        return f"Raised({self.cls.__name__}, {self.msg!r})"
