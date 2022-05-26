import logging
import os
import re
from logging import config

_LOG_CONF = {
    "version": 1,
    # 日志格式化器, 通过指定的日志模板输出日志内容
    "formatters": {
        "standard": {
            "format": (
                "[%(asctime)s][%(name)s][%(levelname)s][%(filename)-8s]"
                "[%(lineno)s]: %(message)s"
            ),
        },
        "short": {
            "format": "%(message)s"
        }
    },
    # 日志处理器, 将输出的日志进行处理 (写入文件或控制台等)
    "handlers": {
        "file": {
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": None,
            "maxBytes": 5000000,
            "backupCount": 10
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "WARN"  # Special level for 'console' handle
        }
    },
    # 日志定义
    "loggers": {
        "default": {  # 日志名称
            "level": "DEBUG",  # 日志等级
            "handlers": ["file", "console"],  # 日志处理器
            "propagate": True  # 是否传播
        },
        "debug": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"]
    }
}


def _read_first_line(filename: str) -> str:
    """
    读取文件内容的第一行

    Args:
        filename (str): 要读取的文件名

    Returns:
        str: 文件内容第一行
    """
    with open(filename, 'r') as pf:
        return pf.readline()


# 用于分割日志内容的正则表达式
PATTERN = re.compile(r"(\[.+?\])|(:[\s\w]+)")

# 获取当前路径
CUR_DIR = os.path.dirname(__file__)


def test_conf_by_dic() -> None:
    """
    测试通过 dict 配置日志

    本例中会写入一条日志, 并读取验证其正确性
    """
    # 生成日志文件的路径文件名
    log_file = os.path.abspath(
        os.path.join(CUR_DIR, "demo.log")
    )

    # 配置日志
    conf = _LOG_CONF.copy()
    # 设置 dict 中日志文件名
    conf["handlers"]["file"]["filename"] = log_file  # type: ignore
    # 配置日志
    config.dictConfig(conf)

    try:
        # 获取名为 default 的日志对象
        log = logging.getLogger("default")

        # 输出一行日志
        log.debug("Log demo")
    finally:
        # 确认日志文件存在
        assert os.path.exists(log_file)
        # 读取一行日志
        line = _read_first_line(log_file).strip()

        # 将日志内容通过正则表达式分割
        r = PATTERN.findall(line)
        # 确认日志内容正确
        assert r[1][0] == "[default]"
        assert r[2][0] == "[DEBUG]"
        assert r[3][0] == "[test_conf.py]"
        assert r[5][1] == ": Log demo"

        # 删除日志文件
        os.remove(log_file)


def test_conf_by_ini() -> None:
    # 生成 ini 配置文件路径
    ini_file = os.path.abspath(
        os.path.join(CUR_DIR, "conf.ini")
    )

    # 生成日志文件的路径文件名
    log_file = os.path.abspath(
        os.path.join(CUR_DIR, "demo.log")
    )

    # 通过 ini 文件配置日志
    config.fileConfig(ini_file)

    try:
        # 获取名为 default 的日志对象
        log = logging.getLogger("default")

        # 输出一行日志
        log.debug("Log demo")
    finally:
        # 确认日志文件存在
        assert os.path.exists(log_file)
        # 读取一行日志
        line = _read_first_line(log_file).strip()

        # 将日志内容通过正则表达式分割
        r = PATTERN.findall(line)
        # 确认日志内容正确
        assert r[1][0] == "[default]"
        assert r[2][0] == "[DEBUG]"
        assert r[3][0] == "[test_conf.py]"
        assert r[5][1] == ": Log demo"

        # 删除日志文件
        os.remove(log_file)
