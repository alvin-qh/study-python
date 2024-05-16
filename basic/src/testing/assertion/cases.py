def add(a: int, b: int) -> int:
    """用于测试的加法函数

    Args:
        - `a` (`int`): 被加数
        - `b` (`int`): 加数

    Returns:
        `int`: 计算结果
    """
    return a + b


def exception() -> None:
    """测试异常抛出的函数

    Raises:
        `ValueError`: 抛出测试异常
    """
    raise ValueError("Example error")
