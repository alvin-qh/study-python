import sys
from loguru import logger

import log as _

# 删除默认的日志输出
logger.remove(0)

# 添加自定义日志输出
logger.add(
    sys.stdout,
    colorize=True,
    level="TRACE",
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
