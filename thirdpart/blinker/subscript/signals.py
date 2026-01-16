from dataclasses import dataclass
from datetime import UTC, datetime

from blinker import Signal, signal

# 创建一个命名信号对象
# 具备相同名称的信号对象表现为 "单例", 即无论创建多少次, 相同名称的信号对象都是同一个对象
init_signal = signal("initialized")

# 创建两个匿名信号对象
ready_signal = Signal()
complete_signal = Signal()


@dataclass
class Log:
    """日志记录类, 用于记录事件日志"""

    def __init__(self, message: str) -> None:
        """初始化日志对象
        Args:
            `message` (`str`): 日志消息
        """
        self.message = message
        self.timestamp = datetime.now(UTC)


class Worker:
    """模拟一个工作类, 在工作开始和完成时发送信号"""

    logs: list[Log]

    def __init__(self, work_id: str) -> None:
        """初始化工作对象
        Args:
            `work_id` (`str`): 工作标识
        """
        self.work_id = work_id
        self.logs = []

    def record(self, log: Log) -> None:
        """记录工作事件
        Args:
            `log` (`Log`): 事件描述
        """
        self.logs.append(log)
