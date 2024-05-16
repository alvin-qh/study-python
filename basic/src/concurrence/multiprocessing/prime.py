from __future__ import annotations

import time
from ctypes import c_bool
from multiprocessing import Queue
from multiprocessing.connection import Connection
from multiprocessing.sharedctypes import Synchronized, SynchronizedArray
from typing import Dict, List, Optional, Tuple


def is_prime(n: int, results: List[bool]) -> None:
    """进程入口函数

    判断一个数是否质数, 当使用进程池的时候, 由于进程池不共享上下文内存, 所以无法使用闭包函数作为进程入口函数

    必须是全局函数或者类方法

    Args:
        - `n` (`int`): 带判断的整数
    """
    # 休眠, 表示当前函数至少需执行 1 秒
    time.sleep(0.1)

    r = True
    if n > 1:
        for i in range(2, n):
            if n % i == 0:
                # 设置结果为真, 表示是质数
                r = False
                break
    else:
        r = False

    results[n] = r


def is_prime_with_extra_arg(n: int, _useless: str = "") -> Tuple[int, bool]:
    """进程入口函数

    本函数具备多个参数, 用于测试多参数情况下进程的启动

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


# 全局变量, 每个进程的内存空间都会具备
global_values: Optional[List[Tuple[Synchronized[int], Synchronized[bool]]]] = None


def initializer(values: List[Tuple[Synchronized[int], Synchronized[bool]]]) -> None:
    """进程池初始化函数

    当实例化 `multiprocessing.Pool` 对象时, 可以传入一个函数作为线程池的初始化函数, 这个函数会在每个进程中执行一次,
    并且在进程池中每个进程之间共享内存空间, 且在进程池中每个进程之间共享内存空间的操作都是原子操作,
    且在进程池中每个进程之间共享内存空间的操作都是原子操作

    Args:
        - `values` (`List[Tuple[Synchronized[int], Synchronized[bool]]]`): 进程池初始化参数, `Value` 对象列表
    """
    global global_values

    # 这个赋值操作相当于为每个进程的 values 全局变量进行复制
    # 此时每个子进程的内存空间中都会存在一个 Value 列表对象的副本
    global_values = values


def is_prime_by_global_variable(n: int) -> None:
    """进程池入口函数

    该函数将计算结果存入 `global_values` 全局变量中, 该变量通过 `initializer` 函数在实例化进程池时为每个进程进行初始化

    Args:
        - `n` (`int`): 要判断是否为质数的数
    """

    if not global_values:
        raise ValueError("No values")

    num, val = global_values[n]
    # 由于每个进程只会进行一次初始化操作
    # 且因为进程池会复用进程, 所以这里对某个进程的公共变量操作, 可能会在复用该进程时影响到
    # 对公共变量的访问
    # values.clear()

    num.value = n

    if n <= 1:
        # 设置结果值
        val.value = False
        return

    for i in range(2, n):
        if n % i == 0:
            # 设置结果值
            val.value = False
            return

    # 设置结果值
    val.value = True


def is_prime_into_list(n: int, result: List[Tuple[int, bool]]) -> None:
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


def is_prime_into_dict(n: int, result: Dict[int, bool]) -> None:
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


def is_prime_into_result_object(n: int, result: PrimeResult) -> None:
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


def is_prime_into_synchronized_array(
    n: int, results: SynchronizedArray[c_bool]
) -> None:
    """进程入口函数

    本函数会将将结果写入 `results` 参数, 该参数为一个进程间共享的 `SynchronizedArray` 类型对象

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
    results[n] = c_bool(True)


def is_prime_into_synchronized_queue(
    in_que: Queue[int], out_que: Queue[Tuple[int, bool]]
) -> None:
    """进程入口函数

    本函数通过 `multiprocessing.Queue` 对象进行数据传递, 并将结果写入 `multiprocessing.Queue` 对象中

    Args:
        - `in_que` (`Queue[int]`): 输入队列, 用于输入参数
        - `out_que` (`Queue[Tuple[int, bool]]`): 结果队列, 用于输出结果
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


def is_prime_by_event_queue(
    in_que: Queue[int], out_que: Queue[Tuple[int, Optional[bool]]]
) -> None:
    """进程入口函数

    本函数通过消息队列, 从一个消息队列中获取整数, 判断其是否为质数, 并将结果写入另一个消息队列
    """
    n: int = 0

    # 持续循环, 直到传递 0 或超时
    while True:
        # 从入参消息队列获取一个整数
        n = in_que.get(timeout=1)
        if n <= 0:
            break

        r = True
        if n > 1:
            for i in range(2, n):
                if n % i == 0:
                    r = False
        else:
            r = False

        # 将结果写入结果消息队列中
        out_que.put((n, r))

    # 在消息队列中写入表示结束的消息
    out_que.put((n, None))


def is_prime_by_pipe(conn: Connection) -> None:
    """进程入口函数

    本函数从子进程管道中获取整数, 判断其是否为质数, 并将结果写入管道中
    """
    # 持续循环, 直到传递 0 或超时
    n: int = 0
    while True:
        # 从管道中读取一个数, 判断其是否为质数
        n = conn.recv()
        if n <= 0:
            break

        r = True
        if n > 1:
            for i in range(2, n):
                if n % i == 0:
                    r = False
        else:
            r = False

        # 将结果写入管道
        conn.send((n, r))

    # 将结束消息写入管道
    conn.send((n, None))
