import math
import threading
import time
import timeit
from concurrent.futures import ThreadPoolExecutor, wait
from functools import partial
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
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

    使用方法

    ```python
    # 消费者方
    try:
        cond.acquire()  # 先进入 Condition 对象的锁
        cond.wait() # 等待 Condition 对象被通知
        ...
    finally:
        cond.release() # 释放 Condition 对象的锁

    # 生成者方
    try:
        cond.acquire()  # 先进入 Condition 对象的锁
        cond.notify() # 发送信号
    finally:
        cond.release() # 释放 Condition 对象的锁
    ```

    或者通过 `with` 语句简化

    ```python
    # 消费者方
    with cond:
        cond.wait()
        ...

    # 生产者方
    with cond:
        cond.notify()
    ```
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

    信号量是一个带计数器的条件锁, 即可设置信号量的总数, 每个进入信号量的线程会占用一个数字,
    离开信号量时归还
    当信号量总数为 0 时, 新的线程将无法进入信号量, 直到有一个线程释放一个信号量

    使用方法

    ```python
    try:
        semp.acquire()  # 占用一个信号量
        ...
    finally:
        semp.release() # 释放占用的信号量
    ```

    或者通过 `with` 语句简化

    ```python
    with semp:
        ...
    ```
    """

    class Resource:
        """
        定义资源类

        资源类的作用是在资源总量的基础上, 记录使用和释放的数量
        """

        def __init__(self, count: int) -> None:
            """
            初始化资源

            Args:
                count (int): 资源数量
            """
            self._count = count
            self._in_use = atomics.atomic(width=4, atype=atomics.INT)

        @property
        def total(self) -> int:
            """
            获取资源总数

            Returns:
                int: 资源总数
            """
            return self._count

        @property
        def left(self) -> int:
            """
            获取剩余资源数量

            Returns:
                int: 剩余资源数量
            """
            return self._count - self._in_use.load()

        def use(self) -> None:
            """
            占用一个资源
            """
            self._in_use.inc()
            # 确保资源不会被超用
            assert self.left >= 0

        def release(self) -> None:
            """
            释放一个资源
            """
            self._in_use.dec()

    # 定义一个具备 10 个资源的对象
    res = Resource(10)

    # 按资源总量定义信号量的数量
    semp = threading.Semaphore(res.total)

    # 记录开始执行时间
    start = timeit.default_timer()

    # 线程执行记录字典
    records: Dict[str, int] = {}

    def func(id_: str) -> None:
        """
        线程入口函数

        Args:
            id_ (str): 线程 ID
        """
        # 进入信号量
        with semp:
            # 记录当前线程获取信号量的时间
            records[id_] = int(timeit.default_timer() - start)

            # 使用一个资源
            res.use()

            # 模拟资源使用 1 秒
            time.sleep(1)

        # 释放被使用的资源
        res.release()

    # 产生若干个线程, 线程数量为 资源总数 + 5
    # 前 资源总数个 线程可以直接获取到信号量
    # 后 5 个线程无法直接获取到信号量, 必须等前面的某个线程释放了信号量后
    # 所以后 5 个线程只能在 1 秒后获取到信号量
    threads = [
        threading.Thread(
            target=func, args=(chr(ord("A") + n),),
        )
        for n in range(res.total + 5)
    ]
    # 启动所有线程
    for t in threads:
        t.start()

    # 等待处理完毕
    for t in threads:
        t.join()

    # 确保资源总数个线程未因获取信号量被阻塞 (时长为 0 的总数)
    assert list(records.values()).count(0) == res.total
    # 确保 5 个线程必须等待 1 秒才能获取到信号量 (时长为 1 的总数)
    assert list(records.values()).count(1) == len(threads) - res.total

    # 确保所有的资源都被使用并归还
    assert res.left == res.total


class TestThreadPool:
    """
    测试线程池, 即一组挂起的线程
    可以将一组任务及其参数放入任务队列中, 线程池可以根据池的大小, 批量的并发执行若干任务
    直到将任务队列中的任务消耗完

    建立一个线程池的方法如下:

    ```python
    with ThreadPool(processes=n_threads) as pool:
    ```
    - `processes` 表示线程池中初始化的线程数
    """

    # 线程池线程总数, 即 CPU 内核总数的 2 倍
    n_threads = cpu_count() * 2

    @staticmethod
    def is_prime(n: int, name: str) -> Tuple[int, bool]:
        """
        判断一个数是否质数

        Args:
            n (int): 待判断的数字
            name (str): 仅用于测试传多个参的无用参数

        Returns:
            Tuple[int, bool]: 返回数字是否质数
        """
        if n <= 1:
            # 1 以下的数不是质数
            return n, False

        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                # 如果能被之前的某个数整除则不是质数
                return n, False

        return n, True

    def test_apply(self) -> None:
        """
        通过线程池管理线程

        `apply` 方法从线程池获取一个线程, 并对传递的线程入口函数和参数执行一次

        `pool.apply(func, (a1, b1, c1))` 表示将 `Tuple` 参数作为入参绑定到 `func` 函数,
        并返回执行结果

        `apply` 方法是同步执行的, 必须等到线程函数执行完毕后返回, 如果要并行执行
        则可通过 `apply_async` 方法, 返回一个句柄, 稍后可通过句柄对象的 `get`
        方法获取线程执行结果
        """
        # 保存结果的数组
        rs = []

        # 实例化线程池对象, 共有 n_threads 个线程
        # with 的使用可以简化线程池对象的 close 函数调用
        with ThreadPool(processes=self.n_threads) as pool:
            # 循环给线程池传递 10 个任务
            for i in range(10):
                # 异步起动任务, 防止循环被阻塞
                # args 参数为一个元组, 即为传递给 is_prime 函数的参数
                # 返回一个句柄, 表示一个异步结果, 通过 get 方法可以获得结果
                h = pool.apply_async(self.is_prime, args=(i, "test"))
                rs.append(h)

            # 通过执行 get 方法获取线程执行结果
            rs = [r.get() for r in rs]

        rs.sort(key=lambda x: x[0])

        # 确认结果正确
        assert rs == [
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

    def test_map(self) -> None:
        """
        通过线程池管理线程
        `map` 方法通过一个参数列表依次将参数和线程入口函数放入线程池执行

        `pool.map(func, [a1, a2, a3, a4])` 表示: 依次将参数 `a1`, `a2`, `a3`, `a4`
        绑定到 `func` 函数上, 并从线程池中取一个线程执行. 并返回每次线程执行的结果集合

        另一个 `map_sync` 方法可以异步的调用线程池, 即不必等待所有任务执行完毕即可返回一个句柄对象

        ```python
        h = pool.map_sync(func, [a1, a2, a3, a4])
        ```

        稍后可以通过 `h.get()` 方法获取线程池执行的结果
        """
        # 实例化一个线程池对象
        # with 的使用可以简化线程池对象的 close 函数调用
        with ThreadPool(processes=self.n_threads) as pool:
            # 向线程池中放置 10 个任务
            # 第二个参数为一个列表, 列表中的每一项会作为传递给 is_prime 函数的参数
            # 返回所有执行结果的列表
            # 由于 map 不直接支持多参数传递, 所以需要通过 partial 函数预设一个参数,
            # 将两个参数的函数变为一个参数
            r = pool.map(
                partial(self.is_prime, name="test"),  # 预设 name 参数
                range(10),
            )

        r.sort(key=lambda x: x[0])

        # 确认线程执行结果
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

    def test_starmap(self) -> None:
        """
        通过线程池管理线程
        `starmap` 方法通过一个入口函数和一组 Tuple 类型的参数列表确认线程执行的次数

        `pool.starmap(func, [(a1, b1, c1), (a2, b2, c2), (a3, b3, c3)])` 表示
        将参数列表中的每个 `Tuple` 作为入参绑定到 `func` 函数,从线程池中获取一个线程来
        执行, 并返回每次线程执行的结果集合

        `starmap` 方法更适合调用多参数的线程入口函数

        另一个 `starmap_async` 方法可以异步的调用线程池, 即不必等待所有任务执行完毕即可返回一个句柄对象

        ```python
        h = pool.starmap_async(
            func,
            [(a1, b1, c1), (a2, b2, c2), (a3, b3, c3)],
        )
        ```

        稍后可以通过 `h.get()` 方法获取线程池执行的结果
        """
        # 实例化线程池对象
        # with 的使用可以简化线程池对象的 close 函数调用
        with ThreadPool(self.n_threads) as pool:
            # 向线程池中放置 10 个任务
            # 第二个参数之所以使用 zip 是因为要产生 10 个元组的列表, 即 [(1,), (2,), ..., (9,)]
            # 每个元组即是一组传递给 is_prime 函数的参数
            # 返回所有执行结果的列表
            r = pool.starmap(self.is_prime, zip(range(10), ["test"]*10))

        r.sort(key=lambda x: x[0])

        # 确认线程执行结果
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

    def test_executor_submit(self) -> None:
        """
        `concurrent.futures` 包下的 `ThreadPoolExecutor` 类表示一个线程池执行器
        和线程池 `ThreadPool` 类相比, 使用更灵活

        通过 `submit` 方法可以为执行器提交一个任务, 任务包含一个入口函数和对应的参数, 参数的
        传递方式为 `*args` 和 `**kwargs`

        `submit` 方法返回一个 `Future` 对象, 表示一个正在执行 (或即将执行) 的任务

        通过 `wait` 函数可以对一组 `Future` 对象进行等待, 直到任务执行完毕或等待超时

        `wait` 函数返回一个 `DoneAndNotDoneFutures` 对象, 包含已完成和未完成的异步任务对象,
        所有已完成的任务对象可以通过 `result` 方法获取执行结果; 未完成的对象可以继续等待
        """
        # 实例化一个线程池执行器对象
        # 通过 with 可以简化对执行器对象的 shutdown 方法调用
        with ThreadPoolExecutor(self.n_threads) as executor:
            # 向执行器提交 10 个任务
            # submit 方法向执行器提交一个任务, 后续的参数表示传递给 is_prime 函数的参数
            # 返回一个 Future 对象, 表示正在执行的任务
            futures = [
                executor.submit(self.is_prime, n, "test") for n in range(10)
            ]

            # 通过 concurrent.futures 包下的 wait 函数, 等待一系列异步任务执行完毕
            # 本次最长等待 1 秒, 一秒后无论是否还有任务为执行完毕, wait 函数都结束阻塞
            # wait 函数返回 DoneAndNotDoneFutures 对象, 包含了已完成和未完成的异步任务
            futures = wait(futures, timeout=1)
            # 确保所有任务都已完成
            assert len(futures.not_done) == 0

            # 遍历所有已完成异步任务, 获取结果
            r = [f.result() for f in futures.done]
            r.sort(key=lambda x: x[0])

            # 确保结果正确
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

    def test_executor_map(self) -> None:
        """
        `concurrent.futures` 包下的 `ThreadPoolExecutor` 类表示一个线程池执行器
        和线程池 `ThreadPool` 类相比, 使用更灵活

        `map` 方法相当于 `submit` 方法的一个批处理简化, 内部调用的仍是 `submit` 方法,
        并对返回的 `Future` 对象进行等待, 返回所有已完成任务执行结果的列表

        `map` 方法第二个之后的参数表示传递给 `is_prime` 函数的参数列表, 其中:
            - `range(10)` 表示所有传递给 `is_prime` 函数的第一个参数
            - `["test"]*10` 表示所有传递给 `is_prime` 函数的第二个参数
        `map` 方法内部会通过 `zip(...)` 将所有单个参数的集合转为一组参数 `tuple` 的集合
        """
        # 实例化一个线程池执行器对象
        # 通过 with 可以简化对执行器对象的 shutdown 方法调用
        with ThreadPoolExecutor(self.n_threads) as executor:
            # range(10) 集合的每一项会作为传递给 is_prime 函数的第一个参数
            # ["test"]*10 集合的每一项会作为传递给 is_prime 函数的第二个参数
            r = executor.map(self.is_prime, range(10), ["test"]*10, timeout=1)

            # 返回结果转为 list
            r = list(r)
            r.sort(key=lambda x: x[0])

            # 确认返回结果正确
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
