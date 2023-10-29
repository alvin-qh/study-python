import time
import timeit
from itertools import repeat
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from typing import Any, Callable, Iterator, Optional

from concurrence import FileLock


def run_worker_by_pool(
    worker: Callable[[Any], None],
    args: Iterator[Any]
) -> float:
    """
    通过线程池执行异步函数

    Args:
        worker (Callable[[Iterator[Any]], None]): 异步函数对象
        args (Iterator[Any]): 异步函数参数, 参数个数为执行异步函数的线程数

    Returns:
        float: 整体耗时数
    """
    start = timeit.default_timer()
    with ThreadPool(cpu_count() * 2) as pool:
        pool.map(worker, args)

    return round(timeit.default_timer() - start, 1)


def test_file_lock_blocked() -> None:
    """
    测试阻塞方式的文件锁
    """

    def worker(lock_name: Optional[str]) -> None:
        """
        线程入口函数, 执行一次耗时 0.1 秒

        Args:
            lock_name (Optional[str]): 锁文件名称, None 表示不加锁
        """
        if lock_name:
            # 加锁
            with FileLock(lock_name):
                time.sleep(0.1)
        else:
            # 不加锁
            time.sleep(0.1)

    # 通过 5 个线程执行, 不加锁
    r = run_worker_by_pool(worker, repeat(None, 5))
    assert 0.1 <= r < 0.2  # 整体执行耗时约 0.1 秒, 表示 5 个线程并发同时执行

    # 通过 5 个线程执行, 加锁
    r = run_worker_by_pool(worker, repeat("lock", 5))
    assert 0.5 <= r < 0.6  # 整体执行耗时约 0.5 秒, 表示 5 个线程依次顺序执行


def test_file_lock_non_blocked() -> None:
    """
    测试非阻塞方式加锁
    """

    def worker(lock_name: Optional[str]) -> None:
        """
        线程入口函数, 执行一次耗时 0.1 秒

        Args:
            lock_name (Optional[str]): 锁文件名称, None 表示不加锁
        """
        if lock_name:
            # 加锁
            fl = FileLock(lock_name)
            # 非阻塞方式加锁
            if fl.acquire(blocking=False):
                try:
                    time.sleep(0.1)
                finally:
                    fl.release()
        else:
            # 不加锁
            time.sleep(0.1)

    # 通过 5 个线程执行, 不加锁
    r = run_worker_by_pool(worker, repeat(None, 5))
    assert 0.1 <= r < 0.2  # 整体执行耗时约 0.1 秒, 表示 5 个线程并发同时执行

    # 通过 5 个线程执行, 加锁
    r = run_worker_by_pool(worker, repeat("lock", 5))
    assert 0.1 <= r < 0.2  # 整体执行耗时约 0.1 秒, 表示 5 个线程并发同时执行, 加锁不阻塞执行
