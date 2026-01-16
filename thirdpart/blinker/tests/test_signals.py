import time
from datetime import UTC, datetime

from blinker import signal
from subscript.events import handle_init_again_event, handle_init_event
from subscript.signals import Worker, complete_signal, init_signal, ready_signal


def test_named_signals() -> None:
    """测试命名信号"""

    # 同一个名称创建的信号对象是单例, 多次创建返回同一个对象
    assert init_signal is signal("initialized")

    # 不同名称场景的信号对象是不同对象
    assert init_signal is not signal("initialize")


def test_named_ready_signal_subscript() -> None:
    """测试发送命名信号"""

    # 通过 "on_initialized" 信号对象发送信号, 此时 "handle_initialized_event" 函数会被调用, 并返回结果
    # 返回结果格式类似于 [(subscript_func1, return_value1), ..., (subscript_funcN, return_valueN)]
    received = init_signal.send(None, name="Alvin", message="Hello")

    # 返回 2 个结果, 表示信号被处理了两次
    assert len(received) == 2

    # 第一个结果由 handle_initialized_event 处理函数返回
    assert received[0][0] == handle_init_event
    assert received[0][1] == 'The sender "Alvin" send a message: "Hello"'

    # 第一个结果由 handle_initialized_again_event 处理函数返回
    assert received[1][0] == handle_init_again_event
    assert received[1][1] == 'The message "Hello" was sent from "Alvin"'


def test_anonymous_signals() -> None:
    """测试发送匿名信号

    本测试定义了一个模拟工作流程的函数, 在工作开始和完成时发送匿名信号 `ready_signal` 和 `complete_signal`,
    并定义 `Worker` 类对象作为事件发送方, 同时在该对象中记录工作事件日志

    测试通过检查 `Worker` 对象中的日志记录, 验证信号的发送和处理是否正确
    """

    def do_work(worker: Worker) -> None:
        """模拟工作函数, 发送 `ready_signal` 和 `complete_signal` 信号
        Args:
            `worker` (`Worker`): 工作对象
        """
        # 发送 ready_signal 信号
        ready_signal.send(worker, timeit=datetime.now(UTC))

        # 模拟工作过程
        time.sleep(0.5)

        # 发送 complete_signal 信号
        complete_signal.send(worker, timeit=datetime.now(UTC))

    # 创建工作对象
    worker = Worker("work-001")

    # 执行工作函数
    do_work(worker)

    # 检查工作对象中的事件日志
    assert len(worker.logs) == 2

    assert worker.logs[0].message == "Work work-001 is ready"
    assert worker.logs[1].message == "Work work-001 is complete"

    assert worker.logs[0].timestamp < worker.logs[1].timestamp
