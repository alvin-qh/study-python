import threading
from typing import Tuple


def test_start_thread() -> None:
    """演示如何指定线程入口函数并启动一个线程"""
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
    """演示通过继承的方式使用线程

    从 `Thread` 类继承, 并重写其 `run` 方法
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

        def run(self) -> None:
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
    演示如何获取当前所有启动的线程数

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

    # 记录当前线程数
    count = threading.active_count()

    # 启动线程
    t = threading.Thread(target=func)
    t.start()

    # 有新的线程启动
    assert threading.active_count() == count + 1

    # 通知锁
    with cond:
        cond.notify()
