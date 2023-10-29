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
from multiprocessing import Manager, Pool
from multiprocessing.managers import BaseManager
from typing import Dict, List, Tuple

from concurrence.multiprocessing import (N_PROCESSES, PrimeResult,
                                         prime_to_dict, prime_to_list,
                                         prime_to_result)


def test_manager_list() -> None:
    """
    演示 `Manager` 类型的 `list` 方法

    `list` 方法返回一个 `List` 类型的代理对象, 可以在进程间共享这个列表对象
    """
    # 实例化 Manager 对象
    with Manager() as manager:
        # 获取一个 List 类型的共享代理对象
        r: List[Tuple[int, bool]] = manager.list()  # type: ignore

        # 实例化进程池
        with Pool(processes=N_PROCESSES) as pool:
            # 启动进程, 将共享 List 代理对象作为参数传入
            pool.starmap(
                prime_to_list,
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


def test_manager_dict() -> None:
    """
    演示 `Manager` 类型的 `dict` 方法

    `dict` 方法返回一个 `Dict` 类型的代理对象, 可以在进程间共享这个字典对象
    """

    # 实例化 Manager 对象
    with Manager() as manager:
        # 获取一个 Dict 类型的共享代理对象
        kv: Dict[int, bool] = manager.dict()  # type: ignore

        # 实例化进程池
        with Pool(processes=N_PROCESSES) as pool:
            # 启动进程, 将共享 Dict 代理对象作为参数传入
            pool.starmap(
                prime_to_dict,
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
        pr = manager.prime_result()  # type: ignore

        # 实例化进程池
        with Pool(processes=N_PROCESSES) as pool:
            # 启动进程, 将共享 PrimeResult 代理对象作为参数传入
            pool.starmap(
                prime_to_result,
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
