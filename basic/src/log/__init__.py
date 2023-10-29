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
    return os.path.join(_CUR_DIR, "conf.ini")


def make_log_file_path() -> str:
    return os.path.join(_CUR_DIR, "demo.log")
