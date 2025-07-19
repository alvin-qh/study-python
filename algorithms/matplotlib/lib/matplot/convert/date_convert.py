from datetime import datetime
from typing import cast

import matplotlib.dates as mdates


def bytespdate2num(
    b: str | bytes | bytearray,
    encoding: str = "utf-8",
    default: datetime | None = None,
) -> float:
    """将 `bytes` 类型或 `bytearray` 类型表示的时间日期串转换为数值

    1. `matplotlib` 中不直接使用 `datetime` 类型处理时间, 而是使用 `float` 类型,
    处理时间戳数据

    2. 如果用 numpy 的 `loadtxt` 函数读取数据, 则所有的文本数据都会被读取为 `bytes` 类型,
    此时参数 `converters` 的设置必须设置为一个能将 `bytes` 类型串转为 `float` 类型数值

    本函数就是用于解决使用 numpy 时, 如何将 `bytes` 类型日期时间串转为 `float` 类型

    Args:
        `b` (`Union[bytes, bytearray]`): `bytes` 类型或 `bytearray` 类型的日期串
        `encoding` (`str`, optional): 日期串的字符串编码. Defaults to `"utf-8"`.
        `default` (`Optional[datetime]`, optional): 默认的时间日期值. Defaults to `None`.

    Returns:
        `float`: 转化后的整数值
    """
    if isinstance(b, str):
        s = b
    elif isinstance(b, (bytes, bytearray)):
        s = b.decode(encoding)
    else:
        raise TypeError("b must be str or bytes or bytearray")

    return cast(float, mdates.datestr2num(s, default=default))
