"""
演示 `multiprocessing` 包的 `Manager` 类型

如果使用 `Pool` 通过进程池使用进程, 则因为无法共享内存上下文, 所以`Value`, `Queue`
等内存共享方式无法直接使用 (需要通过 `initializer` 方法对共享变量进行初始化)

而 `Manager` 类型则可以通过 Socket 方式完成底层的通信, 实现数据共享, 包括:
- `list` 方法, 得到一个可在进程间共享的列表对象
- `dict` 方法, 得到一个可在进程间共享的字典对象
- `Value` 类型, 一个可在进程间共享的简单值对象
- `Queue` 类型, 一个可在进程间共享的消息队列

可以通过 `Manager` 类型的 `register` 函数将任意类型挂载到 `Manager` 类型
"""
from itertools import repeat
from multiprocessing import Manager, Pool, cpu_count
from multiprocessing.managers import BaseManager
from typing import Dict, List, Tuple

from .prime_result import PrimeResult

# 可以启动的进程总数
_n_processes = cpu_count()


def _is_prime_to_list(
    n: int, result: List[Tuple[int, bool]]
) -> None:
    """
    进程入口函数, 用于演示 `Manager` 类型的 `list` 方法产生的列表对象

    Args:
        n (int): 整数
        result (List[Tuple[int, bool]]): 保存结果的共享列表对象
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


def test_manager_list() -> None:
    """
    演示 `Manager` 类型的 `list` 方法

    `list` 方法返回一个 `List` 类型的代理对象, 可以在进程间共享这个列表对象
    """
    # 实例化 Manager 对象
    with Manager() as manager:
        # 获取一个 List 类型的共享代理对象
        r = manager.list()

        # 实例化进程池
        with Pool(processes=_n_processes) as pool:
            # 启动进程, 将共享 List 代理对象作为参数传入
            pool.starmap(
                _is_prime_to_list,
                zip(range(10), repeat(r)),
            )

        # 将结果存放到本地的列表对象中
        # 共享的列表对象只能在 manager 的上下文中使用, 这里将共享列表的元素复制到本地列表对象中
        r = [*r]
        r.sort(key=lambda x: x[0])

    # 确认进程执行结果
    assert r == [
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (5, True),
        (6, False),
        (7, True),
        (8, False),
        (9, False),
    ]


def _is_prime_to_dict(n: int, result: Dict[int, bool]) -> None:
    """
    进程入口函数, 用于演示 `Manager` 类型的 `dict` 方法产生的字典对象

    Args:
        n (int): 整数
        result (Dict[int, bool]): 保存结果的共享字典对象
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


def test_manager_dict() -> None:
    """
    演示 `Manager` 类型的 `dict` 方法

    `dict` 方法返回一个 `Dict` 类型的代理对象, 可以在进程间共享这个字典对象
    """

    # 实例化 Manager 对象
    with Manager() as manager:
        # 获取一个 Dict 类型的共享代理对象
        kv = manager.dict()

        # 实例化进程池
        with Pool(processes=_n_processes) as pool:
            # 启动进程, 将共享 Dict 代理对象作为参数传入
            pool.starmap(
                _is_prime_to_dict,
                zip(range(10), repeat(kv)),
            )

        # 将结果存放到本地的列表对象中
        # 共享的列表对象只能在 manager 的上下文中使用, 这里将共享字典的元素复制到本地列表对象中
        r = [(n, r) for n, r in kv.items()]

    r.sort(key=lambda x: x[0])

    # 确认进程执行结果
    assert r == [
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (5, True),
        (6, False),
        (7, True),
        (8, False),
        (9, False),
    ]


def _is_prime_to_prime_result(n: int, result: PrimeResult) -> None:
    """
    进程入口函数, 用于演示通过 `BaseManager` 类型的 `register` 方法注册的类型

    Args:
        n (int): 整数
        result (PrimeResult): PrimeResult 类型的代理对象
    """
    if n <= 1:
        # 保存结果
        result.put(n, False)
        return

    for i in range(2, n):
        if n % i == 0:
            # 保存结果
            result.put(n, False)
            return

    # 保存结果
    result.put(n, True)


def test_manager_register() -> None:
    """
    演示 `BaseManager` 类型的 `register` 方法

    `register` 方法用于注册任意类型, 并可通过注册类型的名称获取其代理对象
    获取的代理对象可以在多进程间共享

    注意: 注册类型的代理对象仅针对类型的方法进行代理, 属性和魔法方法无法使用
    """

    # 产生一个 BaseManager 类型的对象
    # Manager 类型即是从 BaseManager 类型继承的, 内置注册了一系列常用类型
    manager = BaseManager()
    # 通过 prime_result 为名称, 注册 PrimeResult 类型
    manager.register("prime_result", PrimeResult)

    with manager:
        # 通过 prime_result 名称返回 PrimeResult 的代理对象
        pr = manager.prime_result()

        # 实例化进程池
        with Pool(processes=_n_processes) as pool:
            # 启动进程, 将共享 PrimeResult 代理对象作为参数传入
            pool.starmap(
                _is_prime_to_prime_result,
                zip(range(10), repeat(pr)),
            )

        # 将共享对象结果复制到本地列表中
        r = [*pr.iterator()]

    r.sort(key=lambda x: x[0])

    # 确认进程执行结果
    assert r == [
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (5, True),
        (6, False),
        (7, True),
        (8, False),
        (9, False),
    ]