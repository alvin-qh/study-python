import threading
import time
from typing import Dict, Optional, Tuple

import atomics


def test_start_thread() -> None:
    """
    启动线程
    """
    total = 0

    def func(times: int) -> None:
        """
        线程入口函数

        Args:
            times (int): 循环次数
        """
        # 访问外层定义的变量
        nonlocal total

        # 将变量增加若干次
        for _ in range(times):
            total += 1

    # 产生一个线程对象
    # target 线程入口函数
    # kwargs 线程入口函数参数
    t = threading.Thread(target=func, kwargs={"times": 10})
    # 启动线程
    t.start()

    # 等待线程结束
    t.join()

    assert total == 10


def test_thread_class() -> None:
    """
    另一种使用线程的方式是: 从线程类继承, 并重写其 `run` 方法
    """
    class MyThread(threading.Thread):
        """
        继承线程类
        """

        def __init__(self, id_: int, times: int) -> None:
            """
            初始化线程对象

            Args:
                times (int): 循环次数
            """
            super().__init__()

            # 记录线程 ID
            self._id = id_
            # 记录计算结果
            self._value = 0
            # 保存循环次数
            self._times = times

        @property
        def value(self) -> Tuple[int, int]:
            """
            获取计算结果

            Returns:
                int: 计算结果
            """
            return (self._id, self._value)

        def run(self):
            """_summary_
            """
            for _ in range(self._times):
                self._value += 1

    # 启动 id=1 的线程
    t1 = MyThread(id_=1, times=10)
    t1.start()

    # 启动 id=2 的线程
    t2 = MyThread(id_=2, times=20)
    t2.start()

    # 等待两个线程执行完毕
    t1.join()
    t2.join()

    # 验证线程确实执行
    assert t1.value == (1, 10)
    assert t2.value == (2, 20)


def test_active_count_function() -> None:
    """
    获取当前启动的线程数

    `threading` 包的 `active_count` 函数用于获取当前总共运行的线程数
    """
    # 定义一个条件锁对象
    cond = threading.Condition()

    def func() -> None:
        """
        线程入口函数
        """
        # 等待锁通知
        with cond:
            cond.wait()

    # 此时只有一个线程启动 (主线程)
    assert threading.active_count() == 1

    # 启动线程
    t = threading.Thread(target=func)
    t.start()

    # 此时只有两个线程启动
    assert threading.active_count() == 2

    # 通知锁
    with cond:
        cond.notify()


def test_lock() -> None:
    """
    测试线程加锁 Lock 类型

    - `acquire` 函数进入锁
    - `release` 函数释放锁

    即

    ```python
    try:
        lock.acquire()
        ...
    finally:
        lock.release()
    ```

    可以通过 `with` 语句简化处理

    ```python
    with lock:
        ...
    ```

    `acquire` 函数的 `blocking` 参数表示当锁被占用时, 是否阻塞
        - `True` 表示阻塞, 此时线程会被挂起, 直到占用的锁被释放, 当前线程占用该锁
        - `False` 表示非阻塞, 此时函数返回是否成功的占用了锁
    """
    # 定义一给锁对象
    lock = threading.Lock()

    # 定义一个公共资源变量
    name: Optional[str] = None

    def func() -> None:
        """
        线程入口函数
        """
        nonlocal name

        # 加锁后修改公共资源
        with lock:
            name = f"Hello, {name}"

    # 进入锁
    with lock:
        # 启动线程, 此时由于锁的缘故, 线程函数无法访问公共资源
        t = threading.Thread(target=func)
        t.start()

        # 为公共资源赋值
        name = "Alvin"

    # 等待线程处理公共资源
    # 此时主线程离开锁, 子线程可以访问公共资源, 主线程等待一段时间保证子线程完成访问
    time.sleep(0.1)

    # 确认公共资源被子线程修改完毕
    assert name == "Hello, Alvin"


def test_rlock() -> None:
    """
    测试 `RLock` 类型

    `RLock` 的用法和 `Lock` 类似, 但 `RLock` 会和线程绑定, 即 `RLock` 不会阻塞同一个线程中的占用
    """
    lock = threading.Lock()
    try:
        # 对于 Lock, 在同一线程使用多次, 第二次会被阻塞
        assert lock.acquire(blocking=False) is True
        assert lock.acquire(blocking=False) is False  # 第二次占用锁失败
    finally:
        lock.release()

    lock = threading.RLock()
    try:
        # 对于 RLock, 在同一线程使用多次不会发生阻塞
        assert lock.acquire(blocking=False) is True
        assert lock.acquire(blocking=False) is True  # 每次占用锁都可以成功
    finally:
        lock.release()


def test_condition() -> None:
    """
    `Condition` 对象是一个带条件判断的锁

    当线程进入锁后, 需要等待另一个线程对锁进行通知操作
    - `notify` 通知所有等待方的其中一个
    - `notify_all` 同时通知所有等待方
    """
    # 定义条件锁
    cond = threading.Condition()

    def func(id_: str, result: Dict[str, bool]) -> None:
        """
        线程入口函数

        Args:
            id_ (str): 线程 ID
            result (Dict[str, bool]): 保存结果的字典对象
        """
        # 进入锁
        with cond:
            # 等待锁通知并记录通知结果
            result[id_] = cond.wait(1)

    # 保存线程执行结果的字典
    r: Dict[str, bool] = {}

    # 定义两个线程
    threads = [
        threading.Thread(target=func, args=("A", r)),
        threading.Thread(target=func, args=("B", r)),
    ]

    # 启动两个线程
    for t in threads:
        t.start()

    # 通知其中的一个线程
    # 此时另一个线程等待通知会超时
    with cond:
        cond.notify()

    # 等待线程结束
    for t in threads:
        t.join()

    # 验证结果, A 线程等待通知成功, B 线程等待失败
    assert r == {"A": True, "B": False}

    r = {}

    # 重新定义两个线程
    threads = [
        threading.Thread(target=func, args=("A", r)),
        threading.Thread(target=func, args=("B", r)),
    ]

    # 启动两个线程
    for t in threads:
        t.start()

    # 通知所有线程
    with cond:
        cond.notify_all()

    # 等待线程执行完毕
    for t in threads:
        t.join()

    # 验证结果, AB 线程均等待通知成功
    assert r == {"A": True, "B": True}


def test_semaphore() -> None:
    """
    信号量
    """

    class Resource:
        """
        定义资源类
        """

        def __init__(self, count: int) -> None:
            """
            初始化资源

            Args:
                count (int): 资源数量
            """
            self._count = atomics.atomic(width=4, atype=atomics.INT)
            self._count.store(count)

        def get(self) -> int:
            self._count.dec()
            return self._count.load()

        def back(self) -> int:
            self._count.inc()
            return self._count.load()

    res_count = 10

    semp = threading.Semaphore(res_count)

    def func(id_: str) -> None:
        with semp:
            
