from itertools import repeat

from concurrence.filelock import (
    blocked_filelock_worker,
    non_blocked_filelock_worker,
    run_worker_by_pool,
)


def test_file_lock_blocked() -> None:
    """测试阻塞方式的文件锁"""

    # 通过 5 个线程执行, 不加锁
    r = run_worker_by_pool(blocked_filelock_worker, repeat(None, 5))
    assert r < 0.5  # 整体执行耗时小于 0.5 秒, 表示 5 个线程并发同时执行

    # 通过 5 个线程执行, 加锁
    r = run_worker_by_pool(blocked_filelock_worker, repeat("lock", 5))
    assert r >= 0.5  # 整体执行耗时大于 0.5 秒, 表示 5 个线程依次顺序执行


def test_file_lock_non_blocked() -> None:
    """测试非阻塞方式加锁"""

    # 通过 5 个线程执行, 不加锁
    r = run_worker_by_pool(non_blocked_filelock_worker, repeat(None, 5))
    assert r < 0.5  # 整体执行耗时小于 0.5 秒, 表示 5 个线程并发同时执行

    # 通过 5 个线程执行, 加锁
    r = run_worker_by_pool(non_blocked_filelock_worker, repeat("lock", 5))
    assert r < 0.5  # 整体执行耗时小于 0.5 秒, 表示 5 个线程并发同时执行, 加锁不阻塞执行
