import logging
from logging import config

# root log 的配置项
_LOG_CONF = {
    "version": 1,
    "formatters": {
        "standard": {
            "format": (
                "[%(asctime)s][%(name)s][%(levelname)s][%(filename)-8s]"
                "[%(lineno)s]: %(message)s"
            ),
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard"
        }
    },
    "root": {  # 为 root log 设定配置
        "level": "DEBUG",  # log 的级别
        "handlers": ["console"]  # log 使用的处理器
    }
}


def test_root_log() -> None:
    """
    测试 `root` 日志

    `root` 是日志的默认名称, 通过 `logging.getLogger()` 无参调用返回的即为 `root` 日志对象
    """
    # 配置 root log
    config.dictConfig(_LOG_CONF)

    # 获取 root log, 无参调用 getLogger 默认返回 root log
    log = logging.getLogger()
    log.info("Hello")
