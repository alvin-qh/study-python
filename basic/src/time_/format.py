from datetime import datetime
from typing import Optional


def iso8601_format(t: datetime, GMT_suffix: Optional[str] = "Z") -> str:
    """将时间格式化为 ISO88601 标准格式

    Args:
        - `t` (`datetime`): 日期时间对象
        - `GMT_suffix` (`Optional[str]`, optional): 标准时间格式后缀. Defaults to `"Z"`.

    Returns:
        `str`: 格式化结果字符串
    """
    s = t.isoformat()
    if GMT_suffix:
        s = s.replace("+00:00", GMT_suffix)

    return s
