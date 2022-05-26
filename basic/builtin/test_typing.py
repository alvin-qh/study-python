from typing import List, TypeVar

# 定义一个泛型类型, 限制在 int, float 和 str 三个类型中
T = TypeVar("T", int, float, str)


def generic_func(val: T) -> List[T]:
    return [val] * 3


def test_generic_method() -> None:
    assert generic_func(True) == [3, 3, 3]
    assert generic_func(0.1) == [0.1, 0.1, 0.1]
    assert generic_func("A") == ["A", "A", "A"]
