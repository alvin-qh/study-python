from itertools import repeat

from basic.concurrence.filelock import blocked_filelock_worker, run_worker_by_pool


def test_file_locked() -> None:
    """测试阻塞方式的文件锁"""

    # 通过 5 个线程执行, 不加锁
    r1 = run_worker_by_pool(blocked_filelock_worker, repeat(None, 5))

    # 通过 5 个线程执行, 加锁
    r2 = run_worker_by_pool(blocked_filelock_worker, repeat("lock", 5))
    assert r1 < r2  # 整体执行耗时大于 0.5 秒, 表示 5 个线程依次顺序执行
