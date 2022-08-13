import re
from typing import Any
from xmlrpc.client import Boolean

from hypothesis import given
from hypothesis import strategies as st


@given(bs=st.binary(min_size=10, max_size=20))
def test_strategies_binary(bs: bytes) -> None:
    """
    假设一组 `byte` 串并依次传递给测试参数, 函数定义如下:

    ```
    hypothesis.strategies.binary(
        *,
        min_size=0,     # 字节串最小允许长度
        max_size=None   # 字节串最大允许长度
    )
    ```
    """
    # 判断生成的结果是一个 byte 串
    assert any(0x0 <= n <= 0x7F for n in bs)
    # 判断生成结果的长度符合预期
    assert 10 <= len(bs) <= 20


@given(b=st.booleans())
def test_strategies_booleans(b: Boolean) -> None:
    """
    假设一组 `Boolean` 值并依次传递给测试参数, 函数定义如下:

    ```
    hypothesis.strategies.booleans()
    ```
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
    将指定函数的返回值依次传递给测试参数

    ```
    hypothesis.strategies.builds(
        target,     # 要调用的函数, 该函数的返回值会作为参数传递给测试函数
        /,
        *args,      # 要传递给 target 函数的参数, 按位置传递
        **kwargs    # 要传递给 target 函数的参数, 按参数名传递
    )
    ```
    """
    # 确认参数为字符串类型
    assert isinstance(r, str)

    # 确认参数是 数字 + 字母 组合
    m = re.match(r"[+-]?\d+(\w+)", r)
    assert m

    # 确认字母组合为所定义的单位字符串
    assert m.group(1) in {"mm", "cm", "m", "km"}


@given(c=st.characters(
    min_codepoint=ord("A"),  # 假设的字符从 A 字符开始
    max_codepoint=ord("Z"),  # 假设的字符到 Z 字符结束
    whitelist_characters="abc",  # 额外传递 a, b, c 三个字符
    blacklist_characters="XY",  # 过滤掉 X, Y 两个字符
    whitelist_categories=("Cs",),  # 允许 Cs 分类中的字符
    blacklist_categories=("Cc", )  # 过滤掉 Cc 分类中的字符
))
def test_strategies_characters(c: str) -> None:
    """
    假设一组字符并依次传递给测试参数

    ```
    hypothesis.strategies.characters(
        *,
        min_codepoint=None,         # 假设字符的最小 unicode 编码
        max_codepoint=None,         # 假设字符的最大 unicode 编码
        whitelist_characters=None,  # 字符白名单, 其内的字符一定会传递给测试参数
        blacklist_characters=None,  # 字符黑名单, 其内的字符会被过滤掉, 不传递给测试参数
        whitelist_categories=None,  # unicode 类别白名单, 在此类别中的字符会传递给测试参数
        blacklist_categories=None   # unicode 类别黑名单, 在此类别中的字符不会传递给测试参数
    )
    ```

    备注: 所谓 Unicode 类别, 即对 Unicode 字符的一个分类, 具体参考 https://unicodeplus.com/category
    """
    assert len(c) == 1

    if ord("A") <= ord(c) <= ord("Z"):
        assert c not in {"X", "Y"}
    else:
        assert c in {"a", "b", "c"}
