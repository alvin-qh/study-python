from typing import Any

from subscript.signals import (AnonymousSignals, anonymous_signals,
                               on_initialized)


def handle_initialized_event(sender: Any, **kwargs) -> str:
    """
    初始化信号的事件处理函数

    Args:
        sender (Any): 事件发送对象, 可以为任意对象, 由事件发送方指定

    Returns:
        str: 事件处理结果
    """
    return f'The sender "{kwargs.get("name")}" send a message: "{kwargs.get("message")}"'


# 将 "initialized" 信号和事件处理函数关联
on_initialized.connect(handle_initialized_event)


@on_initialized.connect
def handle_initialized_again_event(sender: Any, **kwargs) -> str:
    """
    通过 @on_initialized.connect 装饰器可以同时完成事件处理函数的定义和与指定事件的关联

    Args:
        sender (Any): 发送方对象, 可以为任意对象, 由事件发送方指定

    Returns:
        str: 事件处理结果
    """
    return f'The message "{kwargs.get("message")}" was sent from "{kwargs.get("name")}"'


@anonymous_signals.on_ready.connect
def handle_ready_event(sender: AnonymousSignals, **kwargs) -> str:
    """
    定义 AnonymousSignals::on_ready 信号的事件处理函数

    Args:
        sender (AnonymousSignals): 事件发送方对象

    Returns:
        str: 事件处理结果
    """
    return f'ready at "{kwargs.get("timeit")}"'


@anonymous_signals.on_complete.connect
def handle_complete_event(sender: AnonymousSignals, **kwargs) -> str:
    """
    定义 AnonymousSignals::on_ready 信号的事件处理函数

    Args:
        sender (AnonymousSignals): 事件发送方对象

    Returns:
        str: 事件处理结果
    """
    return f'completed at "{kwargs.get("timeit")}"'
