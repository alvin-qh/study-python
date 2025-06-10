from log.console import add_console_sink
from log.file import add_file_sink


def init() -> None:
    """初始化 `log` 模块, 为日志增加输出目标"""
    add_console_sink()
    add_file_sink()
