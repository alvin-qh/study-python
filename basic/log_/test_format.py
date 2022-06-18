import logging
from logging import Formatter, LogRecord, config
from typing import Dict, Optional


class RequestFormatter(Formatter):
    """
    自定义 `log` 内容格式化器
    """

    def __init__(
            self,
            fmt: Optional[str] = None,
            datefmt: Optional[str] = None,
            style="%",
            extra: Optional[Dict[str, str]] = None) -> None:
        """
        初始化格式化器

        Args:
            fmt (Optional[str], optional): 日志格式化模板. Defaults to None.
            datefmt (Optional[str], optional): 日期格式化模板. Defaults to None.
            style (str, optional): 日志模板中变量的前缀字符串. Defaults to "%".
            extra (Optional[Dict[str, str]], optional): 扩展参数. Defaults to None.
        """
        super().__init__(fmt, datefmt, style)
        self._extra = extra

    def format(self, record: LogRecord) -> str:
        """
        格式化 `log` 内容

        Args:
            record (LogRecord): log 内容对象, 表示一条日志

        Returns:
            str: 格式化后的日志字符串
        """
        # 可以为 record 对象增加自定义变量的值
        # 自定义变量可以通过日志模板中的 %(<变量名>)s 进行替换输出
        if self._extra:
            # 遍历 extera 字典
            for k, v in self._extra.items():
                # 将字典的键值对作为扩展变量设置到日志对象上
                record.__setattr__(k, v)

        return super().format(record)


# 定义日志格式化模板
# %(s_org)s 和 %(s_name)s 表示 RequestFormatter 中设定的变量
_FORMAT = (
    "[%(asctime)s][%(name)s][%(levelname)s][%(filename)-8s]"
    "[%(lineno)s]: %(s_org)s:%(s_name)s:%(message)s"
)


_LOG_CONF = {
    "version": 1,
    "formatters": {
        "standard": {
            "format": _FORMAT
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"]
    }
}


def test_log_format() -> None:
    """
    测试为日志设置格式化器

    格式化器可以输出特殊格式的日志字符串, 也可以为日志对象 (LogRecord) 增加额外的参数
    """
    # 配置 root log
    config.dictConfig(_LOG_CONF)

    # 扩展参数
    extra_dict = {
        "s_name": "Alvin",
        "s_org": "alvin.study"
    }

    # 获取 root 日志对象
    log = logging.getLogger()

    # 遍历所有的日志处理器
    for h in log.handlers:
        # 为每个日志处理器设置格式化器对象
        h.setFormatter(RequestFormatter(fmt=_FORMAT, extra=extra_dict))

    log = logging.getLogger()
    log.info("Hello")
