from typing import Tuple


def is_prime_with_extra_arg(n: int, _useless: str = "") -> Tuple[int, bool]:
    """线程入口函数

    本函数作为线程池每个线程的入口函数

    Args:
        - `n` (`int`): 待判断的数字
        - `_useless` (`str`): 用于演示多个参数传参, 无实际意义

    Returns:
        `Tuple[int, bool]`: 返回数字是否质数
    """
    if n <= 1:
        return n, False

    for i in range(2, n):
        if n % i == 0:
            return n, False

    return n, True
