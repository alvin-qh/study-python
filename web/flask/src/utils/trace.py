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


def attach_logger(app):  # type: ignore
    """为 Flask 或 Quart 对象附加日志功能

    如果通过 Gunicorn 等 Web 服务器启动应用, 则无法在控制台输出 Flask/Quart 框架本身的日志, 因此需要为应用附加日志功能,
    使得日志能够在控制台输出.

    Args:
        - `app` (`Union["Flask", "Quart"]`): Flask/Quart 对象

    Returns:
        `Union["Flask", "Quart"]`: 返回带有日志功能的 Flask/Quart 对象
    """
    import logging

    from paste.translogger import TransLogger

    gunicorn_logger: logging.Logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    return TransLogger(app, setup_console_handler=False)
