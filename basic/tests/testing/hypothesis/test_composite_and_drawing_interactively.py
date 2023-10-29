from typing import List, Tuple

from hypothesis import Verbosity, given, note, settings
from hypothesis import strategies as st
from hypothesis.strategies._internal.core import DataObject
from testing.hypothesis import list_and_index


@given(t=list_and_index(
    # elements=st.integers()  # 该参数在 list_and_index 函数中已默认定义
))
def test_composite(t: Tuple[List[int], int]) -> None:
    """
    利用假设函数产生用例并传递给测试参数

    调用 `list_and_index` 函数, 需传递除 `draw` 参数外的所有其它参数
    """
    # 确认参数类型为 Tuple 类型
    assert isinstance(t, tuple)
    # 确认 Tuple 的长度为 2
    assert len(t) == 2

    # 确认 Tuple 的元素 1 为 List 对象
    assert isinstance(t[0], list)
    assert len(t[0]) >= 1

    # 确认 Tuple 的元素 2 为 int 类型
    assert isinstance(t[1], int)
    assert t[1] <= len(t[0]) - 1


@settings(verbosity=Verbosity.verbose)  # 设置在日志中输出更多信息
@given(data=st.data())
def test_drawing_interactively(data: DataObject) -> None:
    """
    `data()` 策略是一种交互的策略方法, 无需在 `@given` 装饰器中直接定义假设规则, 而是在
    测试函数代码中设置策略

    类似于 `@composite` 装饰器, 但功能更为强大. 缺点是 `@example` 装饰器不在起作用, 而
    且当测试出现问题时, 比较难以回放错误, 调试错误
    """
    # 获取一个整数用例并设置 label
    x = data.draw(st.integers(), label="first number")

    # 获取一个整数用例, 且要求不得小于 x 的值, 并设置 label
    y = data.draw(st.integers(min_value=x), label="second number")

    # 确认获取的用例值
    note(f"x <= y is {x <= y}")
    assert x <= y
