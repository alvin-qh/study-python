from __future__ import annotations

import timeit
from ctypes import c_bool
from itertools import repeat
from multiprocessing import Array
from typing import List

from concurrence.multiprocessing.group import ProcessGroup
from concurrence.multiprocessing.prime import is_prime


def test_multiple_processes() -> None:
    """测试进程入口函数

    `multiprocessing` 包的 `Process` 类表示一个进程, 通过一个进程入口函数和入口函数的参数列表即可产生一个进程对象:

    - 通过 `start` 方法启动一个进程
    - 通过 `join` 方法可以等待一个进程执行完毕
    """

    results = Array(c_bool, [False] * 10)

    # 实例化一组进程对象, 数量和 results 集合相同
    group = ProcessGroup(
        target=is_prime,
        arglist=zip(
            range(len(results)),
            repeat(results),
        ),
    )

    # 记录起始时间
    start = timeit.default_timer()

    # 启动所有进程并等待执行完毕
    group.start_and_join()

    # 所有进程执行时间少于 1 秒, 表示都是并发执行
    assert 0 < timeit.default_timer() - start < 1
    assert [bool(r) for r in results.get_obj()] == [
        False,
        False,
        True,
        True,
        False,
        True,
        False,
        True,
        False,
        False,
    ]
