import time
import timeit
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from typing import Any, Callable, Iterator, Optional

from .lock import FileLock


def run_worker_by_pool(worker: Callable[[Any], None], *args: Iterator[Any]) -> float:
    """通过线程池执行异步函数

    Args:
        - `worker`` (Callable[[Iterator[Any]], None]`): 异步函数对象
        - `args` (`Iterator[Any]`): 异步函数参数, 参数个数为执行异步函数的线程数

    Returns:
        `float`: 整体耗时数
    """
    with ProcessPoolExecutor(cpu_count() * 2) as executor:
        start = timeit.default_timer()
        executor.map(worker, *args)

    return timeit.default_timer() - start


def blocked_filelock_worker(lock_name: Optional[str]) -> None:
    """通过阻塞方式使用文件锁

    Args:
        - `lock_name` (`Optional[str]`): 锁文件名称, `None` 表示不加锁
    """
    if lock_name:
        # 加锁
        with FileLock(lock_name):
            time.sleep(0.1)
    else:
        # 不加锁
        time.sleep(0.1)


def non_blocked_filelock_worker(lock_name: Optional[str]) -> None:
    """通过非阻塞方式使用文件锁

    Args:
        - `lock_name` (`Optional[str]`): 锁文件名称, `None` 表示不加锁
    """
    if lock_name:
        # 加锁
        fl = FileLock(lock_name)
        # 非阻塞方式加锁
        if fl.acquire():
            try:
                time.sleep(0.1)
            finally:
                fl.release()
    else:
        # 不加锁
        time.sleep(0.1)
