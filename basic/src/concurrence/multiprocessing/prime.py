from __future__ import annotations

from ctypes import c_bool
from dataclasses import dataclass
from multiprocessing import Queue
from multiprocessing.sharedctypes import SynchronizedArray
from typing import Dict, List, Tuple


def is_prime(n: int, _useless: str = "") -> Tuple[int, bool]:
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


def is_prime_as_list(n: int, result: List[Tuple[int, bool]]) -> None:
    """计算 `n` 以内的所有质数

    本函数用于演示将各个进程的结果统一写入 `Manager` 类型的 `list` 方法产生的列表对象

    Args:
        - `n` (`int`): 整数
        - `result` (`List[Tuple[int, bool]]`): 保存结果的共享列表对象
    """
    if n <= 1:
        # 将结果存入列表
        result.append((n, False))
        return

    for i in range(2, n):
        if n % i == 0:
            # 将结果存入列表
            result.append((n, False))
            return

    # 将结果存入列表
    result.append((n, True))


def is_prime_as_dict(n: int, result: Dict[int, bool]) -> None:
    """进程入口函数

    本函数用于演示将各个进程的结果统一写入 `Manager` 类型的 `dict` 方法产生的列表对象

    Args:
        - `n` (`int`): 整数
        - `result` (`Dict[int, bool]`): 保存结果的共享字典对象
    """
    if n <= 1:
        # 将结果存入字典
        result[n] = False
        return

    for i in range(2, n):
        if n % i == 0:
            # 将结果存入字典
            result[n] = False
            return

    # 将结果存入字典
    result[n] = True


@dataclass
class PrimeResult(List[Tuple[int, bool]]):
    """进程入口函数

    演示在 `BaseManager` 对象中注册自定义类型
    """

    def get_values(self) -> List[Tuple[int, bool]]:
        """获取结果列表

        当通过 `BaseManager` 对象管理对象时, 会产生对应对象的代理对象, 且只代理了原对象的方法, 所以需要
        定义明确的方法用于通过代理对象调用

        Returns:
            `List[Tuple[int, bool]]`: 结果列表
        """
        # 返回结果列表
        return self


def is_prime_as_result_object(n: int, result: PrimeResult) -> None:
    """进程入口函数

    本函数用于演示将各个进程的结果统一写入 `BaseManager` 类型的 `register` 方法注册的类型

    Args:
        - `n` (`int`): 整数
        - `result` (`PrimeResult`): `PrimeResult` 类型的代理对象
    """
    if n <= 1:
        # 保存结果
        result.append((n, False))
        return

    for i in range(2, n):
        if n % i == 0:
            # 保存结果
            result.append((n, False))
            return

    # 保存结果
    result.append((n, True))


def is_prime_as_synchronized_array(n: int, results: SynchronizedArray[c_bool]) -> None:
    """
    进程入口函数

    计算参数 `n` 是否为质数, 并将结果写入 `results` 参数, 该参数为一个进程间共享的 `SynchronizedArray` 类型对象

    Args:
        - `n` (`int`): 带判断的整数
        - `results` (`SynchronizedArray`): 保存结果的共享数组对象
    """
    if n <= 1:
        # 设置第二个 Value 对象, 表示数字是否是质数
        results[n] = c_bool(False)
        return

    for i in range(2, n):
        if n % i == 0:
            # 设置第二个 Value 对象, 表示数字是否是质数
            results[n] = c_bool(False)
            return

    # 设置第二个 Value 对象, 表示数字是否是质数
    results[n] = True


def is_prime_as_synchronized_queue(
    in_que: Queue[int], out_que: Queue[Tuple[int, bool]]
) -> None:
    """
    进程入口函数

    从一个消息队列中获取整数, 判断其是否为质数, 并将结果写入另一个消息队列
    """
    # 从入参队列中获取一个整数
    n = in_que.get(timeout=1)

    if n <= 1:
        # 将结果写入出参队列中
        out_que.put((n, False))
        return

    for i in range(2, n):
        if n % i == 0:
            # 将结果写入出参队列中
            out_que.put((n, False))
            return

    # 将结果写入出参队列中
    out_que.put((n, True))
