import os

from .conf import load_log_config
from .formatter import RequestFormatter

__all__ = [
    "make_log_conf_path",
    "make_log_file_path",
    "load_log_config",
    "RequestFormatter",
]


# 获取当前路径
_CUR_DIR = os.path.dirname(__file__)


def make_log_conf_path() -> str:
    """创建日志配置文件路径

    Returns:
        `str`: 配置文件路径名
    """
    return os.path.join(_CUR_DIR, "conf.ini")


def make_log_file_path(filename: str) -> str:
    """创建日志文件路径

    Returns:
        `str`: 日志文件路径
    """
    return os.path.join(_CUR_DIR, filename)
