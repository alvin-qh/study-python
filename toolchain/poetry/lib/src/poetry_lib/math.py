def add[T: (int, float, str)](a: T, b: T) -> T:
    """加法函数

    Args:
        - `a` (`Additional`): 被加数
        - `b` (`Additional`): 加数

    Returns:
        `Additional`: 计算结果
    """
    return a + b
