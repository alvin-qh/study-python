from typing import List, Tuple, TypeVar

from hypothesis import Verbosity, given, note, settings
from hypothesis import strategies as st
from hypothesis.strategies._internal.core import DataObject

E = TypeVar("E")


@st.composite
def list_and_index(
    draw: st.DrawFn,
    elements: st.SearchStrategy[E] = st.integers(),  # type: ignore
) -> Tuple[List[E], int]:
    """
    定义一个组合的假设函数, 可以根据所给参数组合多个假设对象生成用例数据

    Args:
        draw (st.DrawFn): 根据假设对象产生用例的函数
        elements (SearchStrategy[E], optional): 产生类型为 `E` 用例的假设对象.
            Defaults to `st.integers()`.

    Returns:
        Tuple[List[int], int]: 产生的假设值
    """
    # 产生一个集合类型的用例
    xs = draw(st.lists(elements, min_size=1))

    # 产生集合下标范围内的任意整数
    i = draw(st.integers(min_value=0, max_value=len(xs) - 1))

    # 返回用例值
    return (xs, i)


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
