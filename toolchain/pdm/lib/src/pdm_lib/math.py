def add[T: (int, float, str)](a: T, b: T) -> T:
    """加法函数

    Args:
        - `a` (`T`): 被加数
        - `b` (`T`): 加数

    Returns:
        `T`: 计算结果
    """
    return a + b
