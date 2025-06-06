import logging
import os
import re
from logging import config

from basic.io_.utils import read_file_first_line
from basic.log import load_log_config, make_log_conf_path, make_log_file_path

# 用于分割日志内容的正则表达式
PATTERN = re.compile(r"(\[.+?\])|(:[\s\w]+)")

# 获取当前路径
CUR_DIR = os.path.dirname(__file__)


def close_logger_handlers(*log_names: str) -> None:
    """关闭指定名称日志的 Handlers"""
    for log_name in log_names:
        log = logging.getLogger(log_name)
        for h in log.handlers:
            h.close()


def test_conf_by_dict() -> None:
    """测试通过 `Dict` 对象配置日志

    本例中会写入一条日志, 并读取验证其正确性
    """
    # 生成日志文件的路径文件名
    log_file = make_log_file_path("d1.log")

    # 配置日志
    conf = load_log_config()
    # 设置 dict 中日志文件名
    conf["handlers"]["file"]["filename"] = log_file
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
        line = read_file_first_line(log_file).strip()

        # 将日志内容通过正则表达式分割
        r = PATTERN.findall(line)
        # 确认日志内容正确
        assert r[1][0] == "[default]"
        assert r[2][0] == "[DEBUG]"
        assert r[3][0] == "[test_conf.py]"
        assert r[5][1] == ": Log demo"

        close_logger_handlers("default")

        # 删除日志文件
        os.remove(log_file)


def test_conf_by_ini() -> None:
    """测试通过 `ini` 配置文件配置日志"""

    # 生成 ini 配置文件路径
    ini_file = make_log_conf_path()

    # 生成日志文件的路径文件名
    log_file = make_log_file_path("d2.log")

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
        line = read_file_first_line(log_file).strip()

        # 将日志内容通过正则表达式分割
        r = PATTERN.findall(line)
        # 确认日志内容正确
        assert r[1][0] == "[default]"
        assert r[2][0] == "[DEBUG]"
        assert r[3][0] == "[test_conf.py]"
        assert r[5][1] == ": Log demo"

        close_logger_handlers("default")

        # 删除日志文件
        os.remove(log_file)
