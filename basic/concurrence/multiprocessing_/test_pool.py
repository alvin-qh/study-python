from concurrent.futures import ProcessPoolExecutor, wait
from functools import partial
from itertools import repeat
from multiprocessing import Pool, cpu_count
from typing import Tuple

# 可以启动的进程总数
_n_processes = cpu_count()


def _is_prime(n: int, name: str) -> Tuple[int, bool]:
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
            h = pool.apply_async(_is_prime, args=(i, "test"))
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
            partial(_is_prime, name="test"),  # 预设 name 参数
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
            partial(_is_prime, name="test"),
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
            _is_prime,
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
            executor.submit(_is_prime, n, "test") for n in range(10)
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
            _is_prime,
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
