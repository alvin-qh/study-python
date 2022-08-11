import re
from typing import Any
from xmlrpc.client import Boolean

from hypothesis import given
from hypothesis import strategies as st


@given(bs=st.binary(min_size=10, max_size=20))
def test_strategies_binary(bs: bytes) -> None:
    """
    假设一组 `byte` 串
    """
    # 判断生成的结果是一个 byte 串
    assert any(0x0 <= n <= 0x7F for n in bs)
    # 判断生成结果的长度符合预期
    assert 10 <= len(bs) <= 20


@given(b=st.booleans())
def test_strategies_bools(b: Boolean) -> None:
    """
    假设一个 `Boolean` 类型值

    Args:
        b (Boolean): _description_
    """
    assert isinstance(b, bool)


def format_num(num: int, unit: str) -> str:
    """
    格式化字符串, 合并数字和单位

    Args:
        num (int): 数字参数
        unit (str): 单位字符串

    Returns:
        str: 格式化后的字符串
    """
    return f"{num}{unit}"


@given(r=st.builds(
    format_num,  # 要调用的参数
    num=st.integers(),  # 为 format_num 函数假设的第一个参数
    unit=st.sampled_from(["mm", "cm", "m", "km"]),  # 为 format_num 函数假设的第二个参数
))
def test_strategies_builds(r: Any) -> None:
    """
    设置一个函数调用, 并为函数调用假设所需的参数, 将函数返回值作为参数传入
    """
    # 确认参数为字符串类型
    assert isinstance(r, str)

    # 确认参数是 数字 + 字母 组合
    m = re.match(r"[+-]?\d+(\w+)", r)
    assert m

    # 确认字母组合为所定义的单位字符串
    assert m.group(1) in {"mm", "cm", "m", "km"}
