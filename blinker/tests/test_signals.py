from typing import Any, List

from subscript.events import (handle_complete_event,
                              handle_initialized_again_event,
                              handle_initialized_event, handle_ready_event)
from subscript.signals import (anonymous_signals, create_named_signal,
                               on_initialized)


def test_named_signals() -> None:
    """
    测试命名信号
    """

    # 同一个名称创建的信号对象是单例, 多次创建返回同一个对象
    assert on_initialized is create_named_signal("initialized")

    # 不同名称场景的信号对象是不同对象
    assert on_initialized is not create_named_signal("initialize")


def test_subscript() -> None:
    """
    测试发送命名信号
    """

    # 通过 "on_initialized" 信号对象发送信号, 此时 "handle_initialized_event" 函数会被调用, 并返回结果
    # 返回结果格式类似于 [(subscript_func1, return_value1), ..., (subscript_funcN, return_valueN)]
    received = on_initialized.send(None, name="Alvin", message="Hello")

    # 返回 2 个结果, 表示信号被处理了两次
    assert len(received) == 2

    # 第一个结果由 handle_initialized_event 处理函数返回
    assert received[0][0] == handle_initialized_event
    assert received[0][1] == "The sender \"Alvin\" send a message: \"Hello\""

    # 第一个结果由 handle_initialized_again_event 处理函数返回
    assert received[1][0] == handle_initialized_again_event
    assert received[1][1] == "The message \"Hello\" was sent from \"Alvin\""


def test_anonymous_signals() -> None:
    """
    测试发送匿名信号
    """

    def callback_fn(received: List[Any]) -> str:
        """
        用于作为测试参数的回调函数

        Args:
            received (List[Any]): 回调函数调用前, 调用信号触发的处理函数返回的值

        Returns:
            str: 回调函数返回的值
        """
        assert len(received) == 1
        assert received[0][0] == handle_ready_event
        assert received[0][1].startswith("ready at")
        return "callback"

    # 调用测试函数, 传入回调函数参数
    result = anonymous_signals.go(callback_fn)

    # 返回值包含三部分: 第一个信号处理函数返回值; 回调函数返回值; 第二个处理函数返回值
    assert len(result) == 3

    # 判断返回值的第一部分是否为 handle_ready_event 处理函数的返回值
    r1 = result[0]
    assert len(r1) == 1
    assert r1[0][0] == handle_ready_event
    assert r1[0][1].startswith("ready at")

    # 判断返回值的第二部分是否为 回调函数 的返回值
    r2 = result[1]
    assert r2 == "callback"

    # 判断返回值的第二部分是否为 handle_complete_event 处理函数的返回值
    r3 = result[2]
    assert len(r3) == 1
    assert r3[0][0] == handle_complete_event
    assert r3[0][1].startswith("completed at")
