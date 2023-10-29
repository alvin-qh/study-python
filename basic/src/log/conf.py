from typing import Any, Dict, List, Literal, Tuple, Union, cast

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

Handlers = Union[Literal["file"], Literal["console"]]


def load_log_config(format: str = "", handlers: Tuple[Handlers, ...] = ("file", "console")) -> Dict[str, Any]:
    conf = _LOG_CONF.copy()
    if format:
        conf["formatters"]["standard"]["format"] = format  # type: ignore

    delete_handlers: List[str] = []
    for handle in cast(Dict[str, Any], conf["handlers"]):
        if handle not in handlers:
            delete_handlers.append(handle)

    for handler in delete_handlers:
        del conf["handlers"][handler]  # type: ignore

    conf["loggers"]["default"]["handlers"] = list(handlers)  # type: ignore

    if "console" not in handlers:
        del conf["loggers"]["debug"]  # type: ignore

    return conf
