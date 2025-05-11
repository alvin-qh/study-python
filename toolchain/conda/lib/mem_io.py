import sys
from contextlib import contextmanager
from io import StringIO
from typing import Any, Generator


@contextmanager
def stdout_redirected() -> Generator[StringIO, Any, None]:
    """定义上下文管理器, 用于重定向标准输出

    Yields:
        Generator[StringIO, Any, None]: 返回一个 `StringIO` 对象, 表示被重定向后的标准输出
    """
    # 保存标原始的准输出和错误输出
    stdout = sys.stdout
    stderr = sys.stderr

    # 创建一个 `StringIO` 对象, 用于重定向标准输出和错误输出
    s_io = StringIO()

    # 重定向标准输出和错误输出
    sys.stdout = s_io
    sys.stderr = s_io

    # 返回 `StringIO` 对象, 并执行上下文范围的的代码
    yield s_io

    # 恢复原始的输出和错误输出
    sys.stdout = stdout
    sys.stderr = stderr


@contextmanager
def stdin_redirected(input_str: str) -> Generator[None, Any, None]:
    """定义上下文管理器, 用于重定向标准输入

    Args:
        `input_str` (`str`): 输入到标准输入的字符串内容, 每次输入通过 `\n` 分割

    Yields:
        Generator[None, Any, None]: 不返回任何对象
    """
    # 保存原始的输入
    stdin = sys.stdin

    # 创建一个 `StringIO` 对象, 用于重定向标准输入
    s_io = StringIO(input_str)

    # 重定向标准输入
    sys.stdin = s_io

    # 执行上下文范围的代码
    yield None

    # 恢复原始的输入
    sys.stdin = stdin
