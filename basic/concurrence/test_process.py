import time
import timeit
from concurrent.futures import ProcessPoolExecutor, wait
from ctypes import c_bool, c_int
from functools import partial
from itertools import repeat
from multiprocessing import (Manager, Pipe, Pool, Process, Queue, Value,
                             cpu_count)
from multiprocessing.managers import BaseManager
from typing import Dict, Iterator, List, Tuple

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


def test_shared_value() -> None:
    """
    测试 `multiprocessing` 包的 `Value` 类型

    `Value` 类型可以在进程中共享简单类型, 并可以在不同进程中反应共享值的变化
    """

    # 定义一组保存进程函数输出结果元组的 List 集合
    # 该集合对象会被复制到每个子进程内存空间中, 但在进程中相互独立 (隔离)
    # 该集合中的 Value 对象可以在进程间共享, 但 List 对象不会
    nvs = [(Value(c_int), Value(c_bool)) for _ in range(10)]

    def is_prime(n: int) -> None:
        """
        进程入口函数

        计算参数 n 是否为质数

        Args:
            n (int): 带判断的整数
        """
        # 从集合中
        nv = nvs[n]
        # 在子进程中将 nvs 集合清空, 但这个操作不会影响任何其它进程
        nvs.clear()

        # 设置第一个 Value 对象, 表示数字
        nv[0].value = n

        if n <= 1:
            # 设置第二个 Value 对象, 表示数字是否是质数
            nv[1].value = False
            return

        for i in range(2, n):
            if n % i == 0:
                # 设置第二个 Value 对象, 表示数字是否是质数
                nv[1].value = False
                return

        # 设置第二个 Value 对象, 表示数字是否是质数
        nv[1].value = True

    # 启动一组进程
    group = ProcessGroup(target=is_prime, arglist=zip(range(len(nvs)),))
    group.start_and_join()

    # 结果转换为普通值
    r = [(n.value, v.value) for n, v in nvs]
    r.sort(key=lambda x: x[0])

    # 确保结果符合预期
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


def test_shared_queue() -> None:
    """
    测试 `multiprocessing` 包的 `Queue` 类型

    `Queue` 类型定义了一个消息队列, 可以在一个进程中入队, 在另一个进程中出队
    """

    # 定义传入数据的队列 (入参队列)
    in_que = Queue()
    # 定义传出结果的队列 (出参队列)
    out_que = Queue()

    def is_prime() -> None:
        """
        进程入口函数

        从一个消息队列中获取整数, 判断其是否为质数, 并将结果写入另一个消息队列
        """
        # 从入参队列中获取一个整数
        n = in_que.get(timeout=1)

        if n <= 1:
            # 将结果写入出参队列中
            out_que.put((n, False))
            return

        for i in range(2, n):
            if n % i == 0:
                # 将结果写入出参队列中
                out_que.put((n, False))
                return

        # 将结果写入出参队列中
        out_que.put((n, True))

    # 定义一组进程
    group = ProcessGroup(
        target=is_prime,
        count=10,
    )
    # 启动进程
    group.start()

    # 向入参队列中写入 10 个值
    for n in range(len(group)):
        in_que.put(n)

    # 从出参队列中读取结果
    r = [out_que.get() for _ in range(len(group))]
    r.sort(key=lambda x: x[0])

    # 确保结果符合预期
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


def test_event_queue() -> None:
    """
    测试消息队列

    将进程队列用作消息队列. 可以在一个进程中向队列中写入消息, 并在另一个进程中从该队列中
    读取消息, 整个过程是原子方式的

    当队列为空时, 通过 `get` 方法读取消息可以被阻塞, 直到有消息写入或超时 (抛出 `Empty`
    异常); 也可以通过 `get_nowait` 方法进行不阻塞读取, 如果队列为空则抛出 `Empty` 异常
    """
    # 定义传入数据的队列 (入参队列)
    in_que = Queue()
    # 定义传出结果的队列 (出参队列)
    out_que = Queue()

    def is_prime() -> None:
        """
        进程入口函数

        从一个消息队列中获取整数, 判断其是否为质数, 并将结果写入另一个消息队列
        """
        # 持续循环, 直到传递 0 或超时
        while 1:
            # 从入参消息队列获取一个整数
            n = in_que.get(timeout=1)
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
            out_que.put((n, r))

        # 在消息队列中写入表示结束的消息
        out_que.put((n, None))

    # 启动进程, 传入两个消息队列作为参数
    p = Process(target=is_prime)
    p.start()

    # 向消息队列中写入三个数字
    in_que.put(1)
    in_que.put(2)
    in_que.put(3)

    # 从队列中获取三个结果
    assert out_que.get() == (1, False)
    assert out_que.get() == (2, True)
    assert out_que.get() == (3, True)

    # 向消息队列写入 0 表示结束
    in_que.put(0)
    assert out_que.get() == (0, None)


def test_pipe() -> None:
    """
    测试管道

    管道是借助共享内存在进程间通信的一种方式, 管道有一对, 在其中一个写入, 则可以在另一个
    进行读取, 读取为阻塞方式; 反之亦然
    """

    # 实例化管道对象, 得到两个对象
    # parent_conn 用于父进程, child_conn 用于子进程
    parent_conn, child_conn = Pipe()

    def is_prime() -> None:
        """
        进程入口函数

        从子进程管道中获取整数, 判断其是否为质数, 并将结果写入管道中
        """
        # 持续循环, 直到传递 0 或超时
        while 1:
            # 从管道中读取一个数, 判断其是否为质数
            n = child_conn.recv()
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
            child_conn.send((n, r))

        # 将结束消息写入管道
        child_conn.send((n, None))

    # 启动进程
    p = Process(target=is_prime)
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


# 可以启动的进程总数
_n_processes = cpu_count()


def _pooled_is_prime(n: int, name: str) -> Tuple[int, bool]:
    """
    测试进程池的进程入口函数

    判断一个数是否质数, 当使用进程池的时候, 由于进程池不共享上下文内存, 所以无法使用闭包函数
    作为进程入口函数

    必须是全局函数或者类方法

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


def test_pool_apply() -> None:
    """
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
    with Pool(processes=_n_processes) as pool:
        # 循环给进程池传递 10 个任务
        for i in range(10):
            # 异步起动任务, 防止循环被阻塞
            # args 参数为一个元组, 即为传递给 is_prime 函数的参数
            # 返回一个句柄, 表示一个异步结果, 通过 get 方法可以获得结果
            h = pool.apply_async(_pooled_is_prime, args=(i, "test"))
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


def test_pool_map() -> None:
    """
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
    with Pool(processes=_n_processes) as pool:
        # 向进程池中放置 10 个任务
        # 第二个参数为一个列表, 列表中的每一项会作为传递给 is_prime 函数的参数
        # 返回所有执行结果的列表
        # 由于 map 不直接支持多参数传递, 所以需要通过 partial 函数预设一个参数,
        # 将两个参数的函数变为一个参数
        r = pool.map(
            partial(_pooled_is_prime, name="test"),  # 预设 name 参数
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


def test_pool_imap() -> None:
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
    with Pool(processes=_n_processes) as pool:
        # 向进程池中放置 10 个任务
        # 第二个参数为一个列表, 列表中的每一项会作为传递给 is_prime 函数的参数
        # 返回所有执行结果的列表
        # 由于 imap 不直接支持多参数传递, 所以需要通过 partial 函数预设一个参数,
        # 将两个参数的函数变为一个参数
        rs = pool.imap_unordered(
            partial(_pooled_is_prime, name="test"),
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


def test_pool_starmap() -> None:
    """
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

    with Pool(processes=_n_processes) as pool:
        r = pool.starmap(
            _pooled_is_prime,
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


def test_pool_executor_submit() -> None:
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
    with ProcessPoolExecutor(_n_processes) as executor:
        # 向执行器提交 10 个任务
        # submit 方法向执行器提交一个任务, 后续的参数表示传递给 is_prime 函数的参数
        # 返回一个 Future 对象, 表示正在执行的任务
        futures = [
            executor.submit(_pooled_is_prime, n, "test") for n in range(10)
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


def test_pool_executor_map() -> None:
    """
    `concurrent.futures` 包下的 `ProcessPoolExecutor` 类表示一个进程池执行器和进程
    池 `Pool` 类相比, 使用更灵活. 构造器参数为:
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
    with ProcessPoolExecutor(_n_processes) as executor:
        # range(10) 集合的每一项会作为传递给 is_prime 函数的第一个参数
        # repeat("test", 10) 集合的每一项会作为传递给 is_prime 函数的第二个参数
        r = executor.map(
            _pooled_is_prime,
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


"""
演示 `multiprocessing` 包的 `Manager` 类型

如果使用 `Pool` 通过进程池使用进程, 则因为无法共享内存上下文, 所以`Value`, `Queue`
等内存共享方式无法直接使用 (需要通过 `initializer` 方法对共享变量进行初始化)

而 `Manager` 类型则可以通过 Socket 方式完成底层的通信, 实现数据共享, 包括:
- `list` 方法, 得到一个可在进程间共享的列表对象
- `dict` 方法, 得到一个可在进程间共享的字典对象
- `Value` 类型, 一个可在进程间共享的简单值对象
- `Queue` 类型, 一个可在进程间共享的消息队列

可以通过 `Manager` 类型的 `register` 函数将任意类型挂载到 `Manager` 类型
"""


def _pooled_manager_list_is_prime(
    n: int, result: List[Tuple[int, bool]]
) -> None:
    """
    进程入口函数, 用于演示 `Manager` 类型的 `list` 方法产生的列表对象

    Args:
        n (int): 整数
        result (List[Tuple[int, bool]]): 保存结果的共享列表对象
    """
    if n <= 1:
        # 将结果存入列表
        result.append((n, False))
        return

    for i in range(2, n):
        if n % i == 0:
            # 将结果存入列表
            result.append((n, False))
            return

    # 将结果存入列表
    result.append((n, True))


def test_manager_list() -> None:
    """
    演示 `Manager` 类型的 `list` 方法

    `list` 方法返回一个 `List` 类型的代理对象, 可以在进程间共享这个列表对象
    """
    # 实例化 Manager 对象
    with Manager() as manager:
        # 获取一个 List 类型的共享代理对象
        r = manager.list()

        # 实例化进程池
        with Pool(processes=_n_processes) as pool:
            # 启动进程, 将共享 List 代理对象作为参数传入
            pool.starmap(
                _pooled_manager_list_is_prime,
                zip(range(10), repeat(r)),
            )

        # 将结果存放到本地的列表对象中
        # 共享的列表对象只能在 manager 的上下文中使用, 这里将共享列表的元素复制到本地列表对象中
        r = [*r]
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


def _pooled_manager_dict_is_prime(n: int, result: Dict[int, bool]) -> None:
    """
    进程入口函数, 用于演示 `Manager` 类型的 `dict` 方法产生的字典对象

    Args:
        n (int): 整数
        result (Dict[int, bool]): 保存结果的共享字典对象
    """
    if n <= 1:
        # 将结果存入字典
        result[n] = False
        return

    for i in range(2, n):
        if n % i == 0:
            # 将结果存入字典
            result[n] = False
            return

    # 将结果存入字典
    result[n] = True


def test_manager_dict() -> None:
    """
    演示 `Manager` 类型的 `dict` 方法

    `dict` 方法返回一个 `Dict` 类型的代理对象, 可以在进程间共享这个字典对象
    """

    # 实例化 Manager 对象
    with Manager() as manager:
        # 获取一个 Dict 类型的共享代理对象
        kv = manager.dict()

        # 实例化进程池
        with Pool(processes=_n_processes) as pool:
            # 启动进程, 将共享 Dict 代理对象作为参数传入
            pool.starmap(
                _pooled_manager_dict_is_prime,
                zip(range(10), repeat(kv)),
            )

        # 将结果存放到本地的列表对象中
        # 共享的列表对象只能在 manager 的上下文中使用, 这里将共享字典的元素复制到本地列表对象中
        r = [(n, r) for n, r in kv.items()]

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


class PrimeResult:
    """
    演示在 `Manager` 对象中注册自定义类型
    """

    def __init__(self) -> None:
        """
        构造器, 实例化存储结果的列表对象
        """
        self._l = []

    def put(self, n: int, r: bool) -> None:
        """
        存储一个结果

        Args:
            n (int): 数字
            r (bool): 数字是否质数的结果
        """
        self._l.append((n, r))

    def iterator(self) -> Iterator:
        """
        获取结果集合的迭代器对象

        Returns:
            Iterator: 结果集合的迭代器对象
        """
        return iter(self._l)


def _pooled_manager_register_is_prime(n: int, result: PrimeResult) -> None:
    """
    进程入口函数, 用于演示通过 `BaseManager` 类型的 `register` 方法注册的类型

    Args:
        n (int): 整数
        result (PrimeResult): PrimeResult 类型的代理对象
    """
    if n <= 1:
        # 保存结果
        result.put(n, False)
        return

    for i in range(2, n):
        if n % i == 0:
            # 保存结果
            result.put(n, False)
            return

    # 保存结果
    result.put(n, True)


def test_manager_register() -> None:
    """
    演示 `BaseManager` 类型的 `register` 方法

    `register` 方法用于注册任意类型, 并可通过注册类型的名称获取其代理对象
    获取的代理对象可以在多进程间共享

    注意: 注册类型的代理对象仅针对类型的方法进行代理, 属性和魔法方法无法使用
    """

    # 产生一个 BaseManager 类型的对象
    # Manager 类型即是从 BaseManager 类型继承的, 内置注册了一系列常用类型
    manager = BaseManager()
    # 通过 prime_result 为名称, 注册 PrimeResult 类型
    manager.register("prime_result", PrimeResult)

    with manager:
        # 通过 prime_result 名称返回 PrimeResult 的代理对象
        pr = manager.prime_result()

        # 实例化进程池
        with Pool(processes=_n_processes) as pool:
            # 启动进程, 将共享 PrimeResult 代理对象作为参数传入
            pool.starmap(
                _pooled_manager_register_is_prime,
                zip(range(10), repeat(pr)),
            )

        # 将共享对象结果复制到本地列表中
        r = [*pr.iterator()]

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


# 全局变量, 每个进程的内存空间都会具备
_values: List[Tuple[Value, Value]] = None


def _pooled_initializer(values: List[Tuple[Value, Value]]) -> None:
    """
    进程池初始化函数

    Args:
        values (List[Tuple[Value, Value]]): 进程池初始化参数, Value 对象列表
    """
    global _values

    # 这个赋值操作相当于为每个进程的 _values 全局变量进行复制
    # 此时每个子进程的内存空间中都会存在一个 Value 列表对象的副本
    _values = values


def _initialized_pooled_is_prime(n: int) -> None:
    """
    进程池入口函数

    在进程池中判断参数 `n` 是否为质数

    通过每个子进程内存空间的全局变量 `ctx`, 将结果进行保存, 由于 `ctx` 对象内部存储的 `Value`
    类型对象, 对其进行的操作会在各个进程中共享

    Args:
        n (int): 要判断是否为质数的数
    """
    num, val = _values[n]
    # 由于每个进程只会进行一次初始化操作
    # 且因为进程池会复用进程, 所以这里对某个进程的公共变量操作, 可能会在复用该进程时影响到
    # 对公共变量的访问
    # values.clear()

    num.value = n

    if n <= 1:
        # 设置结果值
        val.value = False
        return

    for i in range(2, n):
        if n % i == 0:
            # 设置结果值
            val.value = False
            return

    # 设置结果值
    val.value = True


def test_pool_initializer() -> None:
    """
    进程池 (`Pool` 对象) 和子进程 (`Process` 对象) 的不同之处在于:
    - 子进程是在代码上下文中产生的, 子进程在产生后, 可以继承之前的内存空间
    - 进程池则不具备这种特征, 无法通过进程间传参的方式传递同步对象 (例如 `Value` 类型对象)

    所以 `Pool` 构造器提供了一个 `initializer` 方法参数, 在进程池产生时会在各个子进程中执行该方法
    起到为进程池中每个子进程进行初始化的目的

    注意:
    - 进程池会复用进程, 所以一个进程对全局内存的操作可能会在该进程复用时影响到进程访问公共变量
    """
    # 声明 Value 对象列表, 这个变量是在主进程内存地址空间中产生
    values = [(Value(c_int), Value(c_bool)) for _ in range(10)]

    # 实例化进程池, 执行 _pooled_initializer 方法为每个子进程进行初始化, 传递初始化参数
    with Pool(initializer=_pooled_initializer, initargs=(values,)) as pool:
        pool.starmap(_initialized_pooled_is_prime, zip(range(10)))

    # 结果转换为普通值
    results = [(v[0].value, v[1].value) for v in values]
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
