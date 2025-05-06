from typing import TypeVar


T = TypeVar("T", int, float, str)


def add(a: T, b: T) -> T:
    """定义泛型加法方法

    Args:
        a (T): 第一个参数
        b (T): 第二个参数

    Returns:
        T: 两个参数之和
    """
    return a + b
