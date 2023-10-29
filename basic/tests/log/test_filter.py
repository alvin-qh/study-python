import logging
from logging import Filter, LogRecord, config
from typing import Dict, Optional

from log.conf import load_log_config


class ContextFilter(Filter):
    """
    日志过滤器类

    日志过滤器会在每条日志输出时调用一次, 传入 LogRecord 对象表示一条日志
    过滤器初始的目的是是否将该条日志输出
    """

    def __init__(self, name="", extra: Optional[Dict[str, str]] = None) -> None:
        """
        构造器

        Args:
            name (str, optional): 过滤器名称. Defaults to "".
            extra (Dict[str, str], optional): 扩展参数. Defaults to None.
        """
        super().__init__(name)
        self._extra = extra

    def filter(self, record: LogRecord) -> bool:
        """
        过滤一条日志对象

        Args:
            record (LogRecord): 一条日志的对象

        Returns:
            bool: True 则输出该条日志, False 则不输出
        """
        # 可以为 record 对象增加自定义变量的值
        # 自定义变量可以通过日志模板中的 %(<变量名>)s 进行替换输出
        if self._extra:
            # 遍历 extera 字典
            for k, v in self._extra.items():
                # 将字典的键值对作为扩展变量设置到日志对象上
                record.__setattr__(k, v)

        return True


def test_log_filter() -> None:
    """
    为日志对象设置过滤器
    """
    conf = load_log_config(handlers=("console",))

    # 配置日志对象
    config.dictConfig(conf)

    # 扩展参数
    extra_dict = {
        "s_name": "Alvin",
        "s_org": "alvin.study"
    }

    # 获取 root 日志对象
    log = logging.getLogger()

    # 为日志对象增加过滤器
    log.addFilter(ContextFilter(extra=extra_dict))
    log.info("Hello")
