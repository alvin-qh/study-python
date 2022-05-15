from abc import ABC, abstractmethod
from ctypes import c_bool, c_int
from multiprocessing import Process, Queue, Value
from typing import Any, Callable, Iterable, Tuple

# 参数列表类型
ArgList = Iterable[Iterable[Any]]


class ProcessGroup:
    """
    进程组类, 表示一组进程
    """

    def __init__(self, target: Callable, arglist: ArgList) -> None:
        """
        构造器, 构造一个进程组对象

        Args:
            target (Callable): 进程入口函数
            arglist (ArgList): 进程参数组, 每组参数为一个 Tuple, 表示传给进程入口函数的参数
        """
        # 根据参数组的数量, 实例化相同数量的进程对象, 放入列表中
        self._ps = [Process(target=target, args=args) for args in arglist]

    def start_and_join(self) -> None:
        """
        启动所有进程并等待所有进程结束
        """
        # 启动所以进程
        for p in self._ps:
            p.start()

        # 等待进程执行完毕
        for p in self._ps:
            p.join()


class Context(ABC):
    """
    进程上下文类型
    """
    @abstractmethod
    def get(self) -> Tuple[int, bool]:
        """
        获取上下文值

        Returns:
            Tuple[int, bool]: 上下文值
        """
        pass

    @abstractmethod
    def put(self, num: int, value: bool) -> None:
        """
        设置上下文值

        Args:
            value (Tuple[int, bool]): 上下文值
        """
        pass


class ValueContext(Context):
    """
    `multiprocessing` 包下的 `Value` 对象用于在进程中共享一个值

    `Value` 对象中存储了一个 C 类型的值, 必须指定具体类型 (参考 `ctypes` 包)
        - `value` 字段即存储的值, 可以对其进行读写
    """

    def __init__(self) -> None:
        """
        初始化两个 Value 对象值

        - `_num` 整数值, 存放一个数字
        - `_val` 布尔值, 存放 `_num` 数字是否为质数
        """
        self._num = Value(c_int, 0)
        self._val = Value(c_bool, False)

    def get(self) -> Tuple[int, bool]:
        # 获取两个 Value 对象的值
        return self._num.value, self._val.value

    def put(self, num: int, value: bool) -> None:
        # 设置两个 Value 对象的值
        self._num.value = num
        self._val.value = value


class QueueContext(Context):
    def __init__(self, maxsize=10) -> None:
        self._queue = Queue(maxsize=maxsize)

    def get(self) -> Tuple[int, bool]:
        return self._queue.get()

    def put(self, num: int, value: bool) -> None:
        self._queue.put((num, value))
