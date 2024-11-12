from typing import TypeVar

# 加数类型
Additional = TypeVar("Additional", int, float, str)


def add(a: Additional, b: Additional) -> Additional:
    """加法函数

    Args:
        - `a` (`Additional`): 被加数
        - `b` (`Additional`): 加数

    Returns:
        `Additional`: 计算结果
    """
    return a + b
