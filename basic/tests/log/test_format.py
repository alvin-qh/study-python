import logging
from logging import config

from log import RequestFormatter
from log.conf import load_log_config

# 定义日志格式化模板
# %(s_org)s 和 %(s_name)s 表示 RequestFormatter 中设定的变量
_FORMAT = (
    "[%(asctime)s][%(name)s][%(levelname)s][%(filename)-8s]"
    "[%(lineno)s]: %(s_org)s:%(s_name)s:%(message)s"
)


def test_log_format() -> None:
    """
    测试为日志设置格式化器

    格式化器可以输出特殊格式的日志字符串, 也可以为日志对象 (LogRecord) 增加额外的参数
    """
    conf = load_log_config(_FORMAT, ("console",))

    # 配置 root log
    config.dictConfig(conf)

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
