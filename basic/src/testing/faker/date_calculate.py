import calendar as c
from functools import lru_cache


@lru_cache(maxsize=100)
def last_day_of_month(year: int, month: int) -> int:
    """获取指定月份的最后一天日期

    Args:
        - `year` (`int`): 指定月份的年
        - `month` (`int`): 指定月份

    Returns:
        `int`: 指定月份最后一天的日期
    """
    last_week = c.monthcalendar(year, month)[-1]
    last_week.reverse()

    for d in last_week:
        if d:
            return d

    return next(d for d in last_week if d)
