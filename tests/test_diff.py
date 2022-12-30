import pytest

from poletest.difftool import (
    FsspecDiffTool,
    DiffTool,
    Raised,
    OpTool,
    Reporter,
    ReporterBase,
    CanNotCompareError,
)


class ReturnValue:
    def do(self, x):
        return x


class ReturnStr:
    def do(self, x):
        return str(x)


class RaiseException:
    def do(self, x):
        if x > 0:
            return x
        else:
            raise Exception(x)


class Op:
    def __init__(self):
        self.x = -1

    def __eq__(self, other) -> bool:
        self.x += 1
        return self.x == other


def test_not_infinity_loop():
    """Make sure you don't get stuck in an infinite loop with lru_cache."""

    assert Reporter([1]) == 1
    assert Reporter([1]) == 1  # not infinity loop


def test_reporter():
    assert hash(Reporter([]))

    r = Reporter([])
    assert list(r) == []
    with pytest.raises(CanNotCompareError):
        bool(r)
    assert str(r) == "[]"
    assert repr(r) == ""

    r = Reporter([1])
    assert list(r) == [1]
    assert str(r) == "[(0, '', <class 'int'>, 1)]"
    assert repr(r) == "[0]: [] - <class 'int'> - 1"
    assert bool(r) == True

    r = r == 1
    assert list(r) == [1, 1]
    assert str(r) == "[(0, '', <class 'int'>, 1), (1, '', <class 'int'>, 1)]"
    assert repr(r) == "[0]: [] - <class 'int'> - 1\n[1]: [] - <class 'int'> - 1"
    assert bool(r) == True

    r = Reporter([1, 2])
    assert list(r) == [1, 2]
    assert bool(r) == False

    r = Reporter([1])
    r = r == 2
    assert list(r) == [2, 1]
    assert bool(r) == False

    assert Reporter([1]) == 1

    # FIXME: __ne__を実装する
    # r = Reporter([1]) != 1
    # assert bool(r) == False


def test_base_0():
    obj_1 = RaiseException()

    t = DiffTool(obj_1)
    r = t.dispatch("do", 1)
    assert isinstance(r, Reporter)
    assert list(r) == [1]
    assert r == 1
    assert t.dispatch("do", 1) == 1
    assert t.dispatch("do", -1) == Raised(Exception, "-1")

    # FIXME: Annotated[Raised[Exception], Msg("-1")]
    # FIXME: Raised("-1")
    # FIXME: Raised[Exception]("-1")
    # FIXME: Raised[Exception](msg="-1")


def test_operator():
    obj = Op()
    assert obj == 0
    assert obj == 1

    op = DiffTool(obj).op
    assert list(op.dispatch("__eq__", 2)) == [True]
    assert list(op.dispatch("__eq__", 2)) == [False]
    assert list(op == 4) == [True]
    assert list(op == 4) == [False]
    assert (op == 6) == True
    assert (op == 6) == False

    op = DiffTool([1,2], [3]).op
    assert list(op.dispatch("__iter__").map(list)) == [[1,2],[3]]


def test_base():
    obj_1 = ReturnValue()
    obj_2 = RaiseException()

    t = DiffTool(obj_1, obj_2)
    assert t.dispatch("do", 1) == 1
    assert t.dispatch("do", -1).equals(-1, Raised(cls=Exception, msg="-1"))

    assert t.dispatch("do", 1)
    assert list(t.dispatch("do", -1)) == [-1, Raised(Exception, "-1")]

    assert not t.dispatch("do", -1)

    obj_1 = ReturnValue()
    obj_2 = ReturnStr()
    t = DiffTool(obj_1, obj_2)
    assert list(t.dispatch("do", "1")) == ["1", "1"]
    assert list(t.dispatch("do", 1)) == [1, "1"]
    assert not t.dispatch("do", 1)


