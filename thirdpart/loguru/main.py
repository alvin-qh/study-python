import sys
from loguru import logger

from log import init

# 初始化日志
init()


# 删除默认的日志输出
logger.remove(0)

"""
为 `logger` 添加一个输出目标

该函数通过 `sink` 参数来定义日志输出目标, 可以是 `sys.stdout`, `sys.stderr`, 文件名, 网络, 管道等

除 `sink` 参数外, 其它参数定义了日志输出方式, 其含义如下:
- `level`: 定义日志级别;
- `colorize`: `True` 表示为日志内容着色, 仅输出到终端时起作用;
- `backtrace`: 确定异常跟踪是否应该延伸到捕获错误的点之外 (设置为 `True` 时), 以便于调试;
- `diagnose`: 确定变量值是否应在异常跟踪中显示. 在生产环境中应将其设置为 `False`, 以避免泄露敏感信息;
- `enqueue`: 启用此选项会将日志记录放入队列中 (设置为 `True` 时), 以避免多个进程记录到同一目的地时发生冲突;
- `catch`: 如果在记录到指定的接收器时发生意外错误, 您可以通过将此选项设置为 `True` 来捕获该错误. 错误将打印到标准错误;
"""
logger.add(
    sys.stdout,
    level="TRACE",
    colorize=True,
    backtrace=True,
    diagnose=True,
    enqueue=True,
    catch=True,
)


def main() -> None:
    """入口函数

    为每个日志级别输出一条日志, 系统内置的日志级别包括:

    | 级别      | 值 |
    |----------|----|
    | TRACE    | 5  |
    | DEBUG    | 10 |
    | INFO     | 20 |
    | SUCCESS  | 25 |
    | WARNING  | 30 |
    | ERROR    | 40 |
    | CRITICAL | 50 |
    """
    # 输出一组日志
    logger.trace("trace message")
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    try:
        raise ZeroDivisionError("division by zero")
    except Exception:
        logger.opt(depth=1).exception("exception message")


if __name__ == "__main__":
    main()
