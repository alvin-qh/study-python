import time
import timeit

from .group import ProcessGroup


def test_multiple_processes() -> None:
    """
    `multiprocessing` 包的 `Process` 类表示一个进程, 通过一个进程入口函数和入口函数的参数列表
    即可产生一个进程对象
        - 通过 `start` 方法启动一个进程
        - 通过 `join` 方法可以等待一个进程执行完毕
    """
    # 10 以内的质数结果
    # 该集合对象会被拷贝到所有子进程内存空间中, 但相互独立
    results = [
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

    def is_prime(n: int) -> None:
        """
        进程入口函数

        计算参数 n 是否为质数

        Args:
            n (int): 带判断的整数
            result (Tuple[Value, Value]): 输出一个 (n, 是否质数) 的元组
        """
        # 休眠, 表示当前函数至少需执行 1 秒
        time.sleep(1)

        # 是否为质数的结果
        expected = results[n]
        # 在子进程中清空列表, 但不会影响其它进程
        results.clear()

        r = True
        if n > 1:
            for i in range(2, n):
                if n % i == 0:
                    # 设置结果为真, 表示是质数
                    r = False
                    break
        else:
            r = False

        # 判断结果值是否符合预期
        assert r == expected

    # 实例化一组进程对象, 数量和 results 集合相同
    group = ProcessGroup(target=is_prime, arglist=zip(range(len(results)),))

    # 记录起始时间
    start = timeit.default_timer()

    # 启动所有进程并等待执行完毕
    group.start_and_join()

    # 所有进程执行时间少于 1.1 秒, 表示都是并发执行
    assert 1.0 < timeit.default_timer() - start < 1.1
