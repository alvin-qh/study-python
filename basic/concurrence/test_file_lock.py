import time
from itertools import repeat
from multiprocessing.pool import ThreadPool
from typing import List, Optional

from .file_lock import FileLock


def work(id_: str, results: List[str], lock_name: Optional[str]) -> None:
    """_summary_

    Args:
        id_ (str): _description_
        results (List[str]): _description_
        lock (Optional[FileLock]): _description_
    """
    def job() -> None:
        """
        执行具体任务, 输出结果
        """
        for i in range(2):
            results.append(f"{id_}_{i}")
            time.sleep(0.001)

    if lock_name:
        lock = FileLock(lock_name)
        try:
            with lock.lock():
                job()
        finally:
            lock.remove()
    else:
        job()


def test_file_lock() -> None:
    def run(lock_names: Optional[List[str]]) -> List[str]:
        results = []
        with ThreadPool(2) as pool:
            args = zip(["A", "B"], repeat(results), lock_names)
            pool.starmap(work, args)

        return results

    r = run(repeat(None))
    assert r == ["A_0", "B_0", "A_1", "B_1"]

    r = run(repeat("lock"))
    assert r == ["B_0", "B_1", "A_0", "A_1"]

    r = run(["lock1", "lock2"])
    assert r == ["A_0", "B_0", "A_1", "B_1"]
