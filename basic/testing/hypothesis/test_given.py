import re
from turtle import exitonclick
from typing import Union

from hypothesis import example, given
from hypothesis import strategies as st

# 基于属性的自动化测试 (Property-based testing)
#
# 是指编写对你的代码来说为真的逻辑语句 (即"属性"), 然后使用自动化工具来生成测试输入 (一般来说，
# 是指某种特定类型的随机生成输入数据)，并观察程序接受该输入时属性是否保持不变。如果某个输入违反
# 了某一条属性，则用户证明程序存在一处错误，并找到一个能够演示该错误的便捷示例


def add(x: int, y: int) -> int:
    """
    加法函数

    Args:
        x (int): 数字 1
        y (int): 数字 2

    Returns:
        int: 两个数字的和
    """
    return x + y


@given(x=st.integers(), y=st.integers())
def test_given(x: int, y: int) -> None:
    """
    `given` 装饰器用于提供一组 "假设", 该组假设中包含了指定类型的随机数据 (包括边界数据), 
    以这组数据为驱动, 驱动测试执行

    `@given(x=st.integers(), y=st.integers())` 表示会给测试函数 `x`, `y` 两个参数, 
    整数类型

    Args:
        x (int): _description_
        y (int): _description_
    """
    print(f"given x={x}, y={y}")
    # 确认加法函数正常
    assert add(x, y) == x + y


def ascii_filter(s: str) -> Union[str, bool]:
    """
    过滤包含非 ASCII 编码字符的字符串

    Args:
        s (str): 输入的字符串

    Returns:
        Union[str, bool]: 如果字符串包含非 ASCII 编码字符, 则返回 False; 否则返回字符串本身
    """
    if re.match("^[\x01-\x7F]{1,}$", s):
        return s

    return False


expected_str = set()


@given(s=st.text())
@example(s="alvin")
@example(s="emma")
def test_example(s: str) -> None:
    """
    `@example` 装饰器用于指定必须产生的测试属性值

    Args:
        s (str): 产生的字符串
    """
    print(f"given s={s}")

    # 过滤字符串
    r = ascii_filter(s)

    if r != False:
        print(f"filtered s={s}")

        # 确认字符串的所有字符都有 ASCII 字符组成
        for c in r:
            assert 0 < ord(c) < 128

    if s in {"alvin", "emma"}:
        # 将指定测试用例值加到确认列表中
        expected_str.add(s)


def teardown_function() -> None:
    """
    测试结束后验证整体结果
    """
    # 确认 test_example 中指定的测试用例被执行
    assert expected_str == {"alvin", "emma"}
