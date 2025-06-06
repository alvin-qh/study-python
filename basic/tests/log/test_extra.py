import logging
from logging import config

from basic.log.conf import load_log_config

_FORMAT_WITH_EXTRA = (
    "[%(asctime)s][%(name)s][%(levelname)s][%(filename)-8s]"
    "[%(lineno)s]: %(s_org)s:%(s_name)s:%(message)s"
)


def test_log_extra() -> None:
    """配置 `root` 日志以演示 `extra` 参数

    在输出日志时 (例如调用日志对象的 `debug` 函数), 可以通过 `extra` 参数设置扩展变量
    扩展变量可以在日志格式模板中通过 `%(<变量名>)s` 输出
    """
    conf = load_log_config(_FORMAT_WITH_EXTRA, ("console",))

    # 配置日志
    config.dictConfig(conf)

    # 获取 root 日志对象
    log = logging.getLogger()

    extra_dict = {"s_name": "Alvin", "s_org": "alvin.study"}

    # 附加扩展参数, 输出日志
    log.info("Hello", extra=extra_dict)
