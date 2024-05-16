import logging
from logging import config

from log.conf import load_log_config
from log.filter import LogContextFilter


def test_log_filter() -> None:
    """
    为日志对象设置过滤器
    """
    conf = load_log_config(handlers=("console",))

    # 配置日志对象
    config.dictConfig(conf)

    # 扩展参数
    extra_dict = {"s_name": "Alvin", "s_org": "alvin.study"}

    # 获取 root 日志对象
    log = logging.getLogger()

    # 为日志对象增加过滤器
    log.addFilter(LogContextFilter(extra=extra_dict))
    log.info("Hello")
