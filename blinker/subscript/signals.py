from datetime import datetime
from typing import Any, Callable, Tuple

from blinker import NamedSignal, Signal, signal


def create_named_signal(name: str) -> NamedSignal:
    """
    创建一个命名的信号

    Args:
        name (str): 信号的名称

    Returns:
        NamedSignal: 返回命名信号对象
    """
    return signal(name)


# 创建一个名为 "initialized" 的命名信号对象
# 具备相同名称的信号对象表现为 "单例", 即无论创建多少次, 相同名称的信号对象都是同一个对象
on_initialized = create_named_signal("initialized")


class AnonymousSignals:
    """
    匿名信号对象
    匿名信号对象不具备名称, 所以无法表达为单例模式, 需要通过变量对其进行存储
    """
    # 实例化两个信号对象
    on_ready = Signal()
    on_complete = Signal()

    def go(self, fn: Callable) -> Tuple[Any, Any, Any]:
        """
        演示匿名信号的调用
        会在回调函数调用前和调用后, 发送两次信号, 引发对应的事件处理程序

        Args:
            fn (Callable): 回调函数对象

        Returns:
            Tuple[Any, Any, Any]: 第一项为回调函数调用前事件处理返回值;
            第二项为回调函数返回值; 第三项为回调函数调用后的事件处理返回值
        """
        r1 = self.on_ready.send(self, timeit=datetime.utcnow())
        r2 = fn(r1)
        r3 = self.on_complete.send(self, timeit=datetime.utcnow())

        return r1, r2, r3


anonymous_signals = AnonymousSignals()
