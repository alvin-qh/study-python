from typing import Tuple


def is_prime_with_extra_arg(n: int, _useless: str = "") -> Tuple[int, bool]:
    """
    测试进程池的进程入口函数

    判断一个数是否质数, 当使用进程池的时候, 由于进程池不共享上下文内存, 所以无法使用闭包函数
    作为进程入口函数

    必须是全局函数或者类方法

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
