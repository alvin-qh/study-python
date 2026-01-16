from typing import Any

from subscript.signals import Log, Worker, ready_signal, complete_signal, init_signal


def handle_init_event(sender: Any, **kwargs: Any) -> str:
    """初始化信号的事件处理函数

    Args:
        `sender` (`Any`): 事件发送对象, 可以为任意对象, 由事件发送方指定

    Returns:
        `str`: 事件处理结果
    """
    return f'The sender "{kwargs.get("name")}" send a message: "{kwargs.get("message")}"'


# 通过函数方式将事件处理函数与指定事件进行关联
init_signal.connect(handle_init_event)


# 通过装饰器方式将事件处理函数与指定事件进行关联


@init_signal.connect
def handle_init_again_event(sender: Any, **kwargs: Any) -> str:
    """
    通过 `@init_signal.connect` 装饰器可以同时完成事件处理函数的定义和与指定事件的关联

    Args:
        `sender` (`Any`): 发送方对象, 可以为任意对象, 由事件发送方指定

    Returns:
        `str`: 事件处理结果
    """
    return f'The message "{kwargs.get("message")}" was sent from "{kwargs.get("name")}"'


@ready_signal.connect
def handle_ready_event(sender: Worker, **kwargs: Any) -> Log:
    """
    定义 `ready_signal` 信号的事件处理函数

    Args:
        `sender` (`Worker`): 事件发送方对象

    Returns:
        `Log`: 事件处理结果
    """
    log = Log(f"Work {sender.work_id} is ready")
    # 在发送方对象中记录事件日志
    sender.record(log)

    return log


@complete_signal.connect
def handle_complete_event(sender: Worker, **kwargs: Any) -> Log:
    """定义 `complete_signal` 信号的事件处理函数

    Args:
        `sender` (`Worker`): 事件发送方对象

    Returns:
        `str`: 事件处理结果
    """
    log = Log(f"Work {sender.work_id} is complete")
    # 在发送方对象中记录事件日志
    sender.record(log)

    return log
