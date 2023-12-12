import logging
from logging import LoggerAdapter, config

from log.conf import load_log_config


def test_log_adapter() -> None:
    """测试配置日志 `Adapter`

    `Adapter` 可以理解为一个 `Logger` 对象的代理, 可以为日志设置扩展变量
    """
    conf = load_log_config(handlers=("console",))

    # 配置 root 日志
    config.dictConfig(conf)

    extra_dict = {"s_name": "Alvin", "s_org": "alvin.study"}

    # 获取初始 log
    init_log = logging.getLogger()

    # 通过 adapter 代理初始 log
    log = LoggerAdapter(logger=init_log, extra=extra_dict)

    log.info("Hello")
