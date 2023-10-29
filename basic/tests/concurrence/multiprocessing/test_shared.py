from ctypes import c_bool, c_int
from multiprocessing import Pipe, Process, Queue, Value

from concurrence.multiprocessing import ProcessGroup


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
        nv[0].value = n  # type: ignore

        if n <= 1:
            # 设置第二个 Value 对象, 表示数字是否是质数
            nv[1].value = False  # type: ignore
            return

        for i in range(2, n):
            if n % i == 0:
                # 设置第二个 Value 对象, 表示数字是否是质数
                nv[1].value = False  # type: ignore
                return

        # 设置第二个 Value 对象, 表示数字是否是质数
        nv[1].value = True  # type: ignore

    # 启动一组进程
    group = ProcessGroup(target=is_prime, arglist=zip(range(len(nvs)),))
    group.start_and_join()

    # 结果转换为普通值
    r = [(n.value, v.value) for n, v in nvs]  # type: ignore
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
    in_que: Queue = Queue()
    # 定义传出结果的队列 (出参队列)
    out_que: Queue = Queue()

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
    in_que: Queue = Queue()
    # 定义传出结果的队列 (出参队列)
    out_que: Queue = Queue()

    def is_prime() -> None:
        """
        进程入口函数

        从一个消息队列中获取整数, 判断其是否为质数, 并将结果写入另一个消息队列
        """
        n: int = 0
        # 持续循环, 直到传递 0 或超时
        while True:
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
        n: int = 0
        while True:
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
