from loguru import logger

"""
要将文件作为输出目标, 只需要将 `add` 方法的 `sink` 参数设置为一个路径名即可, 之后的日志都会写入该路径表示的文件中

和文件相关的参数包括:
- `rotate`: 指定关闭当前日志文件并创建新文件的条件; 此参数值可以是 `int`, `datetime` 或 `str`, 建议使用 `str`, 更易于阅读:
    - 如果是 `int` 值, 它对应于当前文件在创建新文件之前允许保留的最大字节数;
    - 如果是 `datetime.timedelta` 值时, 它指示文件每次旋转的频率, 而 `datetime.time` 指定每个文件旋转应在一天中发生的时间;
    - 如果是 `str` 值, 这是上述类型的变体, 例如: "100 MB", "0.5 GB", "1 month 2 weeks", "4 days", "10h", "monthly",
      "18:00", "sunday", "w0", "monday at 12:00" 等;
    - 创建新日志文件后, 之前的日志文件的文件名将按照 `basename(.*).ext(.*)` 格式重新命名;
- `retention`: 指定当日志达到指定数量后 (或时间) 后, 删除旧日志文件的策略, 此参数值可以为 `int`, `datetime` 或 `str`:
    - 如果是 `int` 值, 它对应于当前文件在创建新文件之前允许保留的最大日志数量;
    - 如果是 `datetime.timedelta` 值时, 表示被删除日志文件的最大存在时间;
    - 如果是 `str` 值时, 表示被删除日志文件的最大存在时间的字符串, 比较易读, 可以为 "1 week", "3 days", "2 months" 等;
- `compression`: 如果设置此选项, 日志文件将转换为指定的压缩格式, 格式包括: "gz", "bz2", "xz", "lzma", "tar", "tar.gz",
  "tar.bz2", "tar.xz", "zip";
- `delay`: 如果设置为 `True`, 则新日志文件的创建将延迟到推送第一条日志消息;
- `mode`, `buffering`, `encoding`: 这些参数将被传递给 Python 的 `open` 函数, 该函数决定了 Python 将如何打开日志文件;
"""

logger.add(
    "logs/demo-log.log",
    format=(
        "[{time:YYYY-MM-DD HH:mm:ss}]"
        "[{level:<8}]"
        "[{name}:{function}:{line}]"
        "- {message}"
    ),
    level="DEBUG",
    enqueue=True,
    rotation="1KB",  # 每 1KB 创建一个新文件
    retention=2,  # 最多保留 2 个历史日志文件
    delay=True,
    backtrace=True,
    diagnose=True,
    colorize=False,
    compression="zip",  # 历史日志文件压缩为 zip 格式
    catch=True,
)
