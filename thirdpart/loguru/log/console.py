import sys
from loguru import logger


def add_console_sink() -> None:
    """为 `logger` 添加一个输出目标, 输出到标准输出流, 并自定义日志输出格式

    如果要令日志输出支持颜色或字体样式, 则需要将 `colorize` 参数设置为 `True`, 支持的样式包括:

    | 文本颜色         | 文本样式            |
    |-----------------|-------------------|
    | `black` (`k`)   | `bold` (`b`)      |
    | `blue` (`e`)    | `dim` (`d`)       |
    | `cyan` (`c`)    | `normal` (`n`)    |
    | `green` (`g`)   | `italic` (`i`)    |
    | `magenta` (`m`) | `underline` (`u`) |
    | `red` (`r`)     | `strike` (`s`)    |
    | `white` (`w`)   | `reverse` (`r`)   |
    | `yellow` (`y`)  | `blink` (`l`)     |
    |                 | `hide` (`h`)      |

    例如:

    | 描述      | 前景色                       | 背景色                       |
    |----------|-----------------------------|-----------------------------|
    | 基础颜色   | `<red>`, `<r>`              | `<GREEN>`, `<G>`           |
    | 浅色      | `<light-blue>`, `<le>`      | `<LIGHT-CYAN>`, `<LC>`     |
    | 8 位色    | `<fg 86>`, `<fg 255>`       | `<bg 42>`, `<bg 9>`        |
    | 16 进制色 | `<fg #00005f>`, `<fg #EE1>` | `<bg #AF5FD7>`, `<bg #fff>` |
    | RGB 色    | `<fg 0,95,0>`               | `<bg 72,119,65>`           |

    | 描述      | 范例                                   |
    |----------|---------------------------------------|
    | 文本样式   | `<bold>`, `<b>`, `<underline>`, `<u>` |

    日志中可包含的内容占位符包括:

    | 占位符       | 描述                                   | 属性                            |
    |-------------|---------------------------------------|---------------------------------|
    | `elapsed`   | 从程序启动到记录日志的时间间隔              | 参考 `datetime.datetime`        |
    | `exception` | 程序抛出的任意异常, 未抛出异常则忽略         | `type`, `value`, `traceback`   |
    | `extra`     | 从用户绑定字典中获取指定值, 参考 `bind` 方法 | 参考 `datetime.datetime`        |
    | `file`      | 记录日志的文件名                         | `name` (default), `path`        |
    | `function`  | 函数名                                 |                                 |
    | `level`     | 日志级别                                | `name` (default), `no`, `icon` |
    | `line`      | 行号                                   |                                |
    | `message`   | 日志内容                                |                                |
    | `module`    | 记录日志的模块名称                        |                                |
    | `name`      | 日志名称                                |                                |
    | `process`   | 进程 ID                                | `name`, `id` (default)         |
    | `thread`    | 线程 ID                                | `name`, `id` (default)         |
    | `time`      | 日志记录时间                             | 参考 `datetime.datetime`       |

    对于 `time` 占位符, 可进一步定义格式, 例如 `{time:YYYY-MM-DD HH:mm:ss}`, 支持的格式占位符包括:

    |              | 占位符    | 输出                           |
    |--------------|----------|-------------------------------|
    | 年            | `YYYY`   | 2000, 2001, 2002 … 2012, 2013 |
    |              | `YY`     | 00, 01, 02 … 12, 13           |
    | 季度          | `Q`      | 1 2 3 4                       |
    | 月            | `MMMM`   | January, February, March …   |
    |              | `MMM`    | Jan, Feb, Mar …               |
    |              | `MM`     | 01, 02, 03 … 11, 12           |
    |              | `M`      | 1, 2, 3 … 11, 12              |
    | 年度天数       | `DDDD`   | 001, 002, 003 … 364, 365     |
    |              | `DDD`    | 1, 2, 3 … 364, 365            |
    | 日期          | `DD`     | 01, 02, 03 … 30, 31           |
    |              | `D`      | 1, 2, 3 … 30, 31              |
    | 星期          | `dddd`   | Monday, Tuesday, Wednesday …  |
    |              | `ddd`    | Mon, Tue, Wed …               |
    |              | `d`      | 0, 1, 2 … 6                   |
    | 标准星期 (ISO) | `E`      | 1, 2, 3 … 7                   |
    | 小时          | `HH`     | 00, 01, 02 … 23, 24           |
    |              | `H`      | 0, 1, 2 … 23, 24              |
    |              | `hh`     | 01, 02, 03 … 11, 12           |
    |              | `h`      | 1, 2, 3 … 11, 12              |
    | 分钟          | `mm`     | 00, 01, 02 … 58, 59           |
    |              | `m`      | 0, 1, 2 … 58, 59              |
    | 秒            | `ss`    | 00, 01, 02 … 58, 59           |
    |              | `s`      | 0, 1, 2 … 58, 59              |
    | 毫秒          | `S`      | 0 1 … 8 9                     |
    |              | `SS`     | 00, 01, 02 … 98, 99           |
    |              | `SSS`    | 000 001 … 998 999             |
    |              | `SSS...` | 000[0..] 001[0..] … 998[0..]  |
    | 上下午        | `A`      | AM, PM                        |
    | 时区          | `Z`      | -07:00, -06:00 … +06:00       |
    |              | `ZZ`     | -0700, -0600 … +0600, +0700   |
    |              | `zz`     | EST CST … MST PST             |
    | 时间戳 (秒级)  | `X`      | 1381685817, 1234567890.123    |
    | 时间戳 (毫秒级) | `x`     | 1234567890123                 |
    """
    logger.add(
        sink=sys.stdout,
        colorize=True,
        format=(
            "<green>[{time:YYYY-MM-DD HH:mm:ss}]</green>"
            "<level>[{level:<8}]</level>"
            "<cyan>[{name}:{function}:{line}]</cyan>"
            "- <level>{message}</level>"
        ),
        level="TRACE",
    )
