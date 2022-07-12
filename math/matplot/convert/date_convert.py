from datetime import datetime
from typing import Optional, Union

from matplotlib import dates as mdates


def bytespdate2num(
    b: Union[str, bytes, bytearray],
    encoding="utf-8",
    default: Optional[datetime] = None,
) -> float:
    """
    将 `bytes` 类型或 `bytearray` 类型表示的时间日期串转换为数值

    Args:
        b (Union[bytes, bytearray]): `bytes` 类型或 `bytearray` 类型的日期串
        encoding (str, optional): 日期串的字符串编码. Defaults to `"utf-8"`.
        default (Optional[datetime], optional): 默认的时间日期值. Defaults to `None`.

    Returns:
        float: 转化后的整数值
    """
    if isinstance(b, str):
        s = b
    else:
        s = b.decode(encoding)

    return mdates.datestr2num(s, default=default)
