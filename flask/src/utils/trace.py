def is_debug() -> bool:
    """检查当前环境是否为调试环境

    本函数的原理为: 检查当前环境中是否具备 `trace`(追踪器) 对象

    追踪器对象可以通过 `sys.gettrace` 函数获取, 如果 `sys` 模块不具备 `gettrace` 函数, 或者 `gettrace` 函数返回 `None`,
    都可以认为当前环境不存在追踪器, 即不是调试环境; 反之可以认为在调试环境中

    Returns:
        bool: 是否为调试环境
    """
    import sys

    return hasattr(sys, "gettrace") and sys.gettrace() is not None


def attach_logger(app: "Flask") -> "Flask":  # type: ignore
    """附加日志

    Args:
        - `app` (`Flask`): Flask 对象
    """
    import logging
    from typing import cast

    from paste.translogger import TransLogger

    from flask import Flask

    gunicorn_logger: logging.Logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    return cast(Flask, TransLogger(app, setup_console_handler=False))
