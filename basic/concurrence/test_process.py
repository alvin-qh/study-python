import time
import timeit
from concurrent.futures import ProcessPoolExecutor, wait
from functools import partial
from itertools import repeat
from multiprocessing import Pipe, Pool, Process, Queue, cpu_count
from multiprocessing.connection import Connection
from typing import List, Tuple

from .context import Context, ProcessGroup, QueueContext, ValueContext


def test_multiple_processes() -> None:
    """
    `multiprocessing` 包的 `Process` 类表示一个进程, 通过一个进程入口函数和入口函数的参数列表
    即可产生一个进程对象
        - 通过 `start` 方法启动一个进程
        - 通过 `join` 方法可以等待一个进程执行完毕
    """
    # 10 以内的质数结果
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
        assert r == results[n]

    # 实例化一组进程对象, 数量和 results 集合相同
    ps = [
        Process(target=is_prime, args=(n,))
        for n in range(len(results))
    ]

    # 记录起始时间
    start = timeit.default_timer()

    # 启动所有进程
    for p in ps:
        p.start()

    # 等待所有进程执行成功
    for p in ps:
        p.join()

    # 所有进程执行时间少于 1.1 秒, 表示都是并发执行
    assert 1.0 < timeit.default_timer() - start < 1.1


class TestSharedInProcesses:
    """
    正常情况下, 进程和进程之间的地址空间是隔离的, 所以无法在进程之间直接共享变量

    可以通过内存共享, 管道, 文件和 socket 等方式在进程中共享数据
    """
    @staticmethod
    def is_prime(n: int, ctx: Context) -> None:
        """
        进程入口函数

        计算参数 n 是否为质数

        Args:
            n (int): 带判断的整数
            result (Tuple[Value, Value]): 输出一个 (n, 是否质数) 的元组
        """
        if n <= 1:
            # 设置结果值
            ctx.put(n, False)
            return

        for i in range(2, n):
            if n % i == 0:
                # 设置结果值
                ctx.put(n, False)
                return

        # 设置结果值
        ctx.put(n, True)

    def test_value_context(self) -> None:
        """
        测试 `.context` 包的 `ValueContext` 类

        该类演示了 `multiprocessing` 包的 `Value` 类用法
        """

        # 定义一组保存进程函数输出结果元组的 List 集合
        ctx = [ValueContext() for _ in range(10)]

        group = ProcessGroup(target=self.is_prime, arglist=zip(range(10), ctx))
        group.start_and_join()

        # 结果转换为普通值
        results = [c.get() for c in ctx]
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

    def test_queue_context(self) -> None:
        """
        测试 `.context` 包的 `QueueContext` 类

        该类演示了 `multiprocessing` 包的 `Queue` 类用法
        """

        # 定义一组保存进程函数输出结果元组的 List 集合
        ctx = QueueContext()

        group = ProcessGroup(
            target=self.is_prime,
            arglist=zip(range(10), repeat(ctx)),
        )
        group.start_and_join()

        # 结果转换为普通值
        results = [ctx.get() for _ in range(10)]
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

    def test_event_queue(self) -> None:
        """
        测试进程队列

        将进程队列用作消息队列. 可以在一个进程中向队列中写入消息, 并在另一个进程中从该队列中
        读取消息, 整个过程是原子方式的

        当队列为空时, 通过 `get` 方法读取消息可以被阻塞, 直到有消息写入或超时 (抛出 `Empty`
        异常); 也可以通过 `get_nowait` 方法进行不阻塞读取, 如果队列为空则抛出 `Empty` 异常
        """
        def is_prime(arg_queue_: Queue, res_queue_: Queue) -> None:
            """
            从一个消息队列中获取整数, 判断其是否为质数, 并将结果写入另一个消息队列

            Args:
                arg_queue_ (Queue): 传递整数的消息队列
                res_queue_ (Queue): 传递计算结果的消息队列
            """
            # 持续循环, 直到传递 0 或超时
            while 1:
                # 从入参消息队列获取一个整数
                n = arg_queue_.get(timeout=1)
                if n <= 0:
                    break

                r = True
                if n > 1:
                    for i in range(2, n):
                        if n % i == 0:
                            r = False
                else:
                    r = False

                # 将结果写入结果消息队列中
                res_queue_.put((n, r))

            # 在消息队列中写入表示结束的消息
            res_queue.put((n, None))

        # 入参消息队列
        arg_queue = Queue()
        # 结果消息队列
        res_queue = Queue()

        # 启动进程, 传入两个消息队列作为参数
        p = Process(target=is_prime, args=(arg_queue, res_queue))
        p.start()

        # 向消息队列中写入三个数字
        arg_queue.put(1)
        arg_queue.put(2)
        arg_queue.put(3)

        # 从队列中获取三个结果
        assert res_queue.get() == (1, False)
        assert res_queue.get() == (2, True)
        assert res_queue.get() == (3, True)

        # 向消息队列写入 0 表示结束
        arg_queue.put(0)
        assert res_queue.get() == (0, None)

    def test_pipe(self) -> None:
        """
        测试管道

        管道是借助共享内存在进程间通信的一种方式, 管道有一对, 在其中一个写入, 则可以在另一个
        进行读取, 读取为阻塞方式; 反之亦然
        """
        def is_prime(conn: Connection) -> None:
            """
            从一个消息队列中获取整数, 判断其是否为质数, 并将结果写入另一个消息队列

            Args:
                arg_queue_ (Queue): 传递整数的消息队列
                res_queue_ (Queue): 传递计算结果的消息队列
            """
            # 持续循环, 直到传递 0 或超时
            while 1:
                # 从管道中读取一个数, 判断其是否为质数
                n = conn.recv()
                if n <= 0:
                    break

                r = True
                if n > 1:
                    for i in range(2, n):
                        if n % i == 0:
                            r = False
                else:
                    r = False

                # 将结果写入管道
                conn.send((n, r))

            # 将结束消息写入管道
            conn.send((n, None))

        # 实例化管道对象, 得到两个对象
        parent_conn, child_conn = Pipe()

        # 启动进程, 将其中一个管道对象传入子进程
        p = Process(target=is_prime, args=(child_conn,))
        p.start()

        # 向管道中写入数字, 并从管道中读取结果
        parent_conn.send(1)
        assert parent_conn.recv() == (1, False)

        parent_conn.send(2)
        assert parent_conn.recv() == (2, True)

        parent_conn.send(3)
        assert parent_conn.recv() == (3, True)

        # 向管道中写入 0 表示结束
        parent_conn.send(0)
        assert parent_conn.recv() == (0, None)


class TestProcessPool:
    # 可以启动的进程总数
    n_processes = cpu_count()

    """
    测试进程池
    """
    @staticmethod
    def is_prime(n: int, name: str) -> Tuple[int, bool]:
        """
        测试进程池的进程入口函数

        判断一个数是否质数

        Args:
            n (int): 待判断的数字
            name (str): 仅用于测试传多个参的无用参数

        Returns:
            Tuple[int, bool]: 返回数字是否质数
        """
        if n <= 1:
            return n, False

        for i in range(2, n):
            if n % i == 0:
                return n, False

        return n, True

    def test_apply(self) -> None:
        """
        通过进程池管理进程

        `apply` 方法从进程池获取一个进程, 并对传递的进程入口函数和参数执行一次

        `pool.apply(func, (a1, b1, c1))` 表示将 `Tuple` 参数作为入参绑定到 `func` 函数,
        并返回执行结果

        `apply` 方法是同步执行的, 必须等到进程函数执行完毕后返回, 如果要并行执行
        则可通过 `apply_async` 方法, 返回一个句柄, 稍后可通过句柄对象的 `get`
        方法获取进程执行结果
        """
        # 保存结果的数组
        rs = []

        # 实例化进程池对象, 共有 n_threads 个进程
        # with 的使用可以简化进程池对象的 close 函数调用
        with Pool(processes=self.n_processes) as pool:
            # 循环给进程池传递 10 个任务
            for i in range(10):
                # 异步起动任务, 防止循环被阻塞
                # args 参数为一个元组, 即为传递给 is_prime 函数的参数
                # 返回一个句柄, 表示一个异步结果, 通过 get 方法可以获得结果
                h = pool.apply_async(self.is_prime, args=(i, "test"))
                rs.append(h)

            # 通过执行 get 方法获取进程执行结果
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
        通过进程池管理进程

        `map` 方法通过一个参数列表依次将参数和进程入口函数放入进程池执行

        `pool.map(func, [a1, a2, a3, a4])` 表示: 依次将参数 `a1`, `a2`, `a3`, `a4`
        绑定到 `func` 函数上, 并从进程池中取一个进程执行. 并返回每次进程执行的结果集合

        另一个 `map_sync` 方法可以异步的调用进程池, 即不必等待所有任务执行完毕即可返回一个句柄对象

        ```python
        h = pool.map_sync(func, [a1, a2, a3, a4])
        ```

        稍后可以通过 `h.get()` 方法获取进程池执行的结果
        """
        # 实例化一个进程池对象
        # with 的使用可以简化进程池对象的 close 函数调用
        with Pool(processes=self.n_processes) as pool:
            # 向进程池中放置 10 个任务
            # 第二个参数为一个列表, 列表中的每一项会作为传递给 is_prime 函数的参数
            # 返回所有执行结果的列表
            # 由于 map 不直接支持多参数传递, 所以需要通过 partial 函数预设一个参数,
            # 将两个参数的函数变为一个参数
            r = pool.map(
                partial(self.is_prime, name="test"),  # 预设 name 参数
                range(10),
            )

        r.sort(key=lambda x: x[0])

        # 确认进程执行结果
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

    def test_imap(self) -> None:
        """
        `imap` 方法和 `map` 方法类似, 但有可能比 `map` 执行慢许多

        `pool.imap(func, [a1, a2, a3, a4])` 表示: 依次将参数 `a1`, `a2`, `a3`, `a4`
        绑定到 `func` 函数上, 并从进程池中取一个进程执行. 并返回每次进程执行的结果集合

        `imap` 方法返回一个 `IMapIterator` 类型的迭代器对象, 从迭代器中可以获取每个进程执行的结果

        另一个 `imap_unordered` 返回的 `IMapIterator` 迭代器中的执行结果不会严格按照参数顺序,
        那个进程先执行完毕就在迭代器中排在前面
        """
        # 实例化进程池对象, 共有 n_processes 个进程
        # with 的使用可以简化进程池对象的 close 函数调用
        with Pool(processes=self.n_processes) as pool:
            # 向进程池中放置 10 个任务
            # 第二个参数为一个列表, 列表中的每一项会作为传递给 is_prime 函数的参数
            # 返回所有执行结果的列表
            # 由于 imap 不直接支持多参数传递, 所以需要通过 partial 函数预设一个参数,
            # 将两个参数的函数变为一个参数
            rs = pool.imap_unordered(
                partial(self.is_prime, name="test"),
                range(10),
            )
            # 从迭代器中获取每个执行结果
            rs = [r for r in rs]

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

    def test_starmap(self) -> None:
        """
        通过进程池管理进程
        `starmap` 方法通过一个入口函数和一组 Tuple 类型的参数列表确认进程执行的次数

        `pool.starmap(func, [(a1, b1, c1), (a2, b2, c2), (a3, b3, c3)])` 表示
        将参数列表中的每个 `Tuple` 作为入参绑定到 `func` 函数,从进程池中获取一个进程来
        执行, 并返回每次进程执行的结果集合

        `starmap` 方法更适合调用多参数的进程入口函数

        另一个 `starmap_async` 方法可以异步的调用进程池, 即不必等待所有任务执行完毕即可返回一个句柄对象

        ```python
        h = pool.starmap_async(
            func,
            [(a1, b1, c1), (a2, b2, c2), (a3, b3, c3)],
        )
        ```

        稍后可以通过 `h.get()` 方法获取进程池执行的结果
        """

        with Pool(processes=self.n_processes) as pool:
            r = pool.starmap(
                self.is_prime,
                zip(range(10), repeat("test", 10)),
            )

        r.sort(key=lambda x: x[0])

        # 确认进程执行结果
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
        `concurrent.futures` 包下的 `ProcessPoolExecutor` 类表示一个进程池执行器
        和进程池 `Pool` 类相比, 使用更灵活. 构造器参数为:
            - `max_workers` workers 的数量
            - `mp_context` 进程上下文
            - `initializer` 任务初始化入口
            - `initargs` 任务初始化参数

        通过 `submit` 方法可以为执行器提交一个任务, 任务包含一个入口函数和对应的参数, 参数的
        传递方式为 `*args` 和 `**kwargs`

        `submit` 方法返回一个 `Future` 对象, 表示一个正在执行 (或即将执行) 的任务

        通过 `wait` 函数可以对一组 `Future` 对象进行等待, 直到任务执行完毕或等待超时

        `wait` 函数返回一个 `DoneAndNotDoneFutures` 对象, 包含已完成和未完成的异步任务对象,
        所有已完成的任务对象可以通过 `result` 方法获取执行结果; 未完成的对象可以继续等待
        """
        # 实例化一个进程池执行器对象
        # 通过 with 可以简化对执行器对象的 shutdown 方法调用
        with ProcessPoolExecutor(self.n_processes) as executor:
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
        `concurrent.futures` 包下的 `ProcessPoolExecutor` 类表示一个进程池执行器
        和进程池 `Pool` 类相比, 使用更灵活. 构造器参数为:
            - `max_workers` workers 的数量
            - `mp_context` 进程上下文
            - `initializer` 任务初始化入口
            - `initargs` 任务初始化参数

        `map` 方法相当于 `submit` 方法的一个批处理简化, 内部调用的仍是 `submit` 方法,
        并对返回的 `Future` 对象进行等待, 返回所有已完成任务执行结果的列表

        `map` 方法第二个之后的参数表示传递给 `is_prime` 函数的参数列表, 其中:
            - `range(10)` 表示所有传递给 `is_prime` 函数的第一个参数
            - `repeat("test", 10)` 表示所有传递给 `is_prime` 函数的第二个参数
        `map` 方法内部会通过 `zip(...)` 将所有单个参数的集合转为一组参数 `tuple` 的集合
        """
        # 实例化一个进程池执行器对象
        # 通过 with 可以简化对执行器对象的 shutdown 方法调用
        with ProcessPoolExecutor(self.n_processes) as executor:
            # range(10) 集合的每一项会作为传递给 is_prime 函数的第一个参数
            # repeat("test", 10) 集合的每一项会作为传递给 is_prime 函数的第二个参数
            r = executor.map(
                self.is_prime,
                range(10),
                repeat("test", 10),
                timeout=1
            )

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


# 全局变量, 每个进程的内存空间都会具备
ctx: List[Context] = None


def pooled_initializer(ctx_: List[Context]) -> None:
    """
    进程池初始化函数

    Args:
        ctx_ (List[Context]): 进程池初始化参数, ValueContext 对象列表
    """
    global ctx

    # 这个赋值操作相当于为每个进程的 ctx 全局变量进行复制
    # 此时每个子进程的内存空间中都会存在一个 Context 列表对象的副本
    ctx = ctx_


def pooled_is_prime(n: int) -> None:
    """
    进程池入口函数

    在进程池中判断参数 `n` 是否为质数

    通过每个子进程内存空间的全局变量 `ctx`, 将结果进行保存, 由于 `ctx` 对象内部存储的 `Value`
    类型对象, 对其进行的操作会在各个进程中共享

    Args:
        n (int): 要判断是否为质数的数
    """
    if n <= 1:
        # 设置结果值
        ctx[n].put(n, False)
        return

    for i in range(2, n):
        if n % i == 0:
            # 设置结果值
            ctx[n].put(n, False)
            return

    # 设置结果值
    ctx[n].put(n, True)


def test_pool_initializer() -> None:
    """
    进程池 (`Pool` 对象) 和子进程 (`Process` 对象) 的一个很大不同之处在于:
    - 子进程是在代码上下文中产生的, 子进程在产生后, 可以继承之前的内存空间
    - 进程池则不具备这种特征, 无法通过进程间传参的方式传递同步对象 (例如 `Value` 类型对象)

    所以 `Pool` 构造器提供了一个 `initializer` 方法参数, 在进程池产生时会在各个子进程中执行该方法
    起到为进程池中每个子进程进行初始化的目的
    """
    # 声明 ValueContext 对象列表, 这个变量是在主进程内存地址空间中产生
    ctx_ = [ValueContext() for _ in range(10)]

    # 实例化进程池, 执行 pooled_initializer 方法为每个子进程进行初始化, 传递初始化参数
    with Pool(initializer=pooled_initializer, initargs=(ctx_,)) as pool:
        pool.starmap(pooled_is_prime, zip(range(10)))

    # 结果转换为普通值
    results = [c.get() for c in ctx_]
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
