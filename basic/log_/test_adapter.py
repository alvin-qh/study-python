import logging
from logging import LoggerAdapter, config

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


def test_log_adapter() -> None:
    """
    配置日志 `Adapter`.
    `Adapter` 可以理解为一个 `Logger` 对象的代理, 可以为日志设置扩展变量
    """
    # 配置 root 日志
    config.dictConfig(_LOG_CONF)

    extra_dict = {
        "s_name": "Alvin",
        "s_org": "alvin.study"
    }

    # 获取初始 log
    init_log = logging.getLogger()

    # 通过 adapter 代理初始 log
    log = LoggerAdapter(logger=init_log, extra=extra_dict)

    log.info("Hello")
