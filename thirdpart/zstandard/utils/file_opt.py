from functools import wraps
from pathlib import Path
from typing import Any, Callable


def delete_file_finally(*paths: str) -> Callable[..., Callable[..., None]]:
    """创建一个装饰器函数, 定义指定文件, 当目标函数执行完毕后删除该文件

    Args:
        `paths` (`tuple[str, ...]`): 要删除的所有文件的路径

    Returns:
        `Callable[..., Callable[..., None]]`: 返回装饰器
    """

    def _decorator(func: Callable[..., Any]) -> Callable[..., None]:
        """装饰器函数, 对参数传入的函数 (`func`) 进行装饰, 当该函数执行完毕后删除指定文件

        Args:
            `func` (`Callable[..., Any]`): 被装饰的函数

        Returns:
            `Callable[..., None]`: 返回装饰后的函数
        """

        @wraps(func)
        def _wrapper() -> None:
            """装饰器: 在函数执行结束后删除指定文件"""
            try:
                func()
            finally:
                # 删除文件
                for path in paths:
                    Path(path).unlink(missing_ok=True)

        return _wrapper

    return _decorator
