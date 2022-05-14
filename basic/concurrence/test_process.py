from ctypes import c_bool, c_int
from multiprocessing import Process, Value
from typing import Tuple


def test_new_process() -> None:
    """
    测试启动新进程

    `multiprocessing` 包的 `Process` 类表示一个进程, 通过一个进程入口函数和入口函数的参数列表
    即可产生一个进程对象
        - 通过 `start` 方法启动一个进程
        - 通过 `join` 方法可以等待一个进程执行完毕

    由于进程在不同的内存空间, 所以进程无法直接共享内存, 需要通过专门的内存共享对象来完成

    `multiprocessing` 包的 `Value` 类型表示一个共享内存的值, 可以在多进程之间共享值的存储.
    `Value` 对象中存储了一个 C 类型的值, 必须指定具体类型 (参考 `ctypes` 包)
        - `value` 字段即存储的值, 可以对其进行读写
    """
    def is_prime(n: int, result: Tuple[Value, Value]) -> None:
        """
        进程入口函数

        计算参数 n 是否为质数

        Args:
            n (int): 带判断的整数
            result (Tuple[Value, Value]): 输出一个 (n, 是否质数) 的元组
        """
        # 元组第一项为 n 值
        result[0].value = n

        if n <= 1:
            # 设置结果值
            result[1].value = False
            return

        for i in range(2, n):
            if n % i == 0:
                # 设置结果值
                result[1].value = False
                return

        # 设置结果值
        result[1].value = True

    # 定义一组保存进程函数输出结果元组的 List 集合
    results = [(Value(c_int, 0), Value(c_bool, False)) for _ in range(10)]

    # 实例化一组进程对象, 数量和 results 集合相同
    ps = [
        Process(target=is_prime, args=(n, results[n]))
        for n in range(len(results))
    ]

    # 启动所有进程
    for p in ps:
        p.start()

    # 等待所有进程执行成功
    for p in ps:
        p.join()

    # 结果转换为普通值
    results = [(r[0].value, r[1].value) for r in results]
    results.sort(key=lambda x: x[0])

    # 确保结果符合预期
    assert results == [
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
