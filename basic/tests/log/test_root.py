import logging
from logging import config

from log.conf import load_log_config


def test_root_log() -> None:
    """
    测试 `root` 日志

    `root` 是日志的默认名称, 通过 `logging.getLogger()` 无参调用返回的即为 `root` 日志对象
    """
    conf = load_log_config(handlers=("console",))

    # 配置 root log
    config.dictConfig(conf)

    # 获取 root log, 无参调用 getLogger 默认返回 root log
    log = logging.getLogger()
    log.info("Hello")
