""" 需要安装 `python-dateutil` 包 """
from datetime import date, datetime

from dateutil import rrule as rr


def test_create_date_sequence_by_rule() -> None:
    """基于规则产生日期

    `dateutil.rrule` 包下的 `rrule` 函数用于产生一个 `rrule` 对象, 可以根据规则产生所需的日期时间, 参数包括:
        - `freq` 单位值，包含如下值：
            - `YEARLY` 按年为间隔产生序列
            - `MONTHLY` 按月为间隔产生序列
            - `WEEKLY` 按周为间隔产生序列
            - `DAILY` 按天为间隔产生序列
        - `cache` 布尔值, 默认为 `False`, 表示是否缓冲计算结果. 如果调用同一个 `rrule` 对象多次, 应该将该参数设为 `True` 以提高性能
        - `dtstart` `datetime` 对象, 表示序列日期时间的起始值
        - `until` `datetime` 对象, 表示序列日期时间的终止值
        - `interval` 整数值, 默认为 `1`, 表示序列中值的间隔
        - `wkst` 可以为 `MO`, `TU`, `WE` 等常量值或者整数值, 默认为 `None` (周日), 表示每一周起始的星期数
        - `count` 整数值, 默认为 `None` (不限制), 表示序列中产生结果的数量
        - `bysetpos` 整数序列或整数值, 默认为 `None`, 表示序列中每个 `datetime` 对象的偏移量, 例如 `rrule` 的结果为
          `[2012-01-01, 2012-02-01]`, 且 `freq=MONTHLY`, 如果设置 `bysetpos=1`, 则结果变为 `[2012-01-01]` (取第一个),
          如果设置为 `-1`, 则结果变为 `[2012-02-01]` (取最后一个)
        - `bymonth` 整数序列或整数值, 默认为 `None`, 表示在结果中包含指定的月份
        - `bymonthday` 整数序列或整数值, 默认为 `None`, 表示在结果中包含指定的月天数 (一月的第几天)
        - `byyearday` 整数序列或整数值, 默认为 `None`, 表示在结果中包含指定的天数 (一年的第几天)
        - `byweekno` 整数序列或整数值, 默认为 `None`, 表示在结果中包含指定的周数 (一年的第几周)
        - `byweekday` 整数序列或整数值, 默认为 `None`, 表示在结果中包含指定的星期数 (周几)
        - `byeaster` 整数序列或整数值, 默认为 `None`, 和复活节有关的星期数
    """

    # 设定起始日期
    start = date(2022, 4, 1)

    # 生成 3 项的日期序列, 以天为间隔, 每天一条数据
    rules = rr.rrule(freq=rr.DAILY, count=3, dtstart=start)
    assert list(rules) == [
        datetime(2022, 4, 1),
        datetime(2022, 4, 2),
        datetime(2022, 4, 3),
    ]

    # 生成 3 项的日期序列, 以天为间隔, 每 3 天一条数据
    rules = rr.rrule(freq=rr.DAILY, count=3, dtstart=start, interval=3)
    assert list(rules) == [
        datetime(2022, 4, 1),
        datetime(2022, 4, 4),
        datetime(2022, 4, 7),
    ]

    # 生成 3 项的日期序列, 以年为间隔, 每年一条数据
    rules = rr.rrule(freq=rr.YEARLY, count=3, dtstart=start)
    assert list(rules) == [
        datetime(2022, 4, 1),
        datetime(2023, 4, 1),
        datetime(2024, 4, 1),
    ]

    # 在指定的到达时间内, 按周为间隔产生数据
    # 结果是指定时间段内的所有周一日期
    rules = rr.rrule(freq=rr.WEEKLY, dtstart=start, until=date(2022, 5, 1))
    assert list(rules) == [
        datetime(2022, 4, 1),
        datetime(2022, 4, 8),
        datetime(2022, 4, 15),
        datetime(2022, 4, 22),
        datetime(2022, 4, 29),
    ]

    # 计算指定时间段内的两个特定天数的日期
    rules = rr.rrule(
        freq=rr.YEARLY,
        dtstart=start,
        until=date(2023, 1, 1),
        byyearday=(100, 200),
    )
    assert list(rules) == [
        datetime(2022, 4, 10),
        datetime(2022, 7, 19),
    ]

    # 计算指定时间段内每个月的最后一天
    rules = rr.rrule(
        freq=rr.MONTHLY,
        dtstart=start,
        until=date(2022, 10, 1),
        bymonthday=-1,
    )
    assert list(rules) == [
        datetime(2022, 4, 30),
        datetime(2022, 5, 31),
        datetime(2022, 6, 30),
        datetime(2022, 7, 31),
        datetime(2022, 8, 31),
        datetime(2022, 9, 30),
    ]

    # 计算指定时间段内每月的第一个周二, 周三或周四
    rules = rr.rrule(
        freq=rr.MONTHLY,
        dtstart=start,
        until=date(2022, 10, 1),
        byweekday=(rr.TU, rr.WE, rr.TH),  # 取值范围为周二, 周三或周四
        bysetpos=1,  # 取第一个值
    )
    dates = [(r.date(), rr.weekday(r.weekday())) for r in rules]
    assert dates == [
        (date(2022, 4, 5), rr.TU),
        (date(2022, 5, 3), rr.TU),
        (date(2022, 6, 1), rr.WE),
        (date(2022, 7, 5), rr.TU),
        (date(2022, 8, 2), rr.TU),
        (date(2022, 9, 1), rr.TH),
    ]


def test_create_datetime_sequence_by_rule() -> None:
    """基于规则产生时间

    `dateutil.rrule` 包下的 `rrule` 函数用于产生一个 `rrule` 对象, 可以根据规则产生所需的日期时间, 参数包括:
    - `freq` 单位值, 包含如下值:
        - `HOURLY` 按小时为间隔产生序列
        - `MINUTELY` 按分钟为间隔产生序列
        - `SECONDLY` 按秒为间隔产生序列
    - `cache` 布尔值, 默认为 `False`, 表示是否缓冲计算结果. 如果调用同一个 `rrule`对象多次, 应该将该参数设为 `True` 以提高性能
    - `dtstart` `datetime` 对象, 表示序列日期时间的起始值
    - `until` `datetime` 对象, 表示序列日期时间的终止值
    - `interval` 整数值, 默认为 `1`, 表示序列中值的间隔
    - `count` 整数值, 默认为 `None` (不限制), 表示序列中产生结果的数量
    - `bysetpos` 整数序列或整数值, 默认为 `None`, 表示序列中每个 `datetime` 对象的偏移量, 例如:
      `rrule` 的结果为 `[2012-01-01, 2012-02-01]`, 且 `freq=MONTHLY`, 如果设置`bysetpos=1`, 则结果变为 `[2012-01-03]`
      (取第一个), 如果设置为 `-1`, 则结果变为 `[2012-02-01]` (取最后一个)
    - `byhour` 整数序列或整数值, 默认为 `None`, 表示在结果中包含指定的小时数
    - `byminute` 整数序列或整数值, 默认为 `None`, 表示在结果中包含指定的分钟数
    - `bysecond` 整数序列或整数值，默认为 `None`, 表示在结果中包含指定的秒数
    """
    # 设定起始时间
    start = datetime(2020, 4, 1, 12, 0, 0)

    # 以小时为间隔, 产生 3 个时间
    times = rr.rrule(freq=rr.HOURLY, count=3, dtstart=start)
    assert list(times) == [
        datetime(2020, 4, 1, 12),
        datetime(2020, 4, 1, 13),
        datetime(2020, 4, 1, 14),
    ]

    # 以秒为间隔, 产生 3 个时间, 每个间隔 10 秒
    times = rr.rrule(freq=rr.SECONDLY, count=3, dtstart=start, interval=10)
    assert list(times) == [
        datetime(2020, 4, 1, 12, 0, 0),
        datetime(2020, 4, 1, 12, 0, 10),
        datetime(2020, 4, 1, 12, 0, 20),
    ]

    # 获取指定时间段内的每个小时
    times = rr.rrule(
        freq=rr.HOURLY,
        dtstart=start,
        until=datetime(2020, 4, 1, 23, 59, 59),
    )
    assert list(times) == [
        datetime(2020, 4, 1, 12),
        datetime(2020, 4, 1, 13),
        datetime(2020, 4, 1, 14),
        datetime(2020, 4, 1, 15),
        datetime(2020, 4, 1, 16),
        datetime(2020, 4, 1, 17),
        datetime(2020, 4, 1, 18),
        datetime(2020, 4, 1, 19),
        datetime(2020, 4, 1, 20),
        datetime(2020, 4, 1, 21),
        datetime(2020, 4, 1, 22),
        datetime(2020, 4, 1, 23),
    ]

    # 获取指定时间段内的 10 点和 20 点
    times = rr.rrule(
        freq=rr.HOURLY,
        dtstart=start,
        until=datetime(2020, 4, 2, 23, 59, 59),
        byhour=(10, 20),
    )
    assert list(times) == [
        datetime(2020, 4, 1, 20),
        datetime(2020, 4, 2, 10),
        datetime(2020, 4, 2, 20),
    ]

    # 获取指定时间段内每小时的最后一秒
    times = rr.rrule(
        freq=rr.HOURLY,
        dtstart=start,
        until=datetime(2020, 4, 1, 22),
        byminute=59,
        bysecond=59,
    )
    assert list(times) == [
        datetime(2020, 4, 1, 12, 59, 59),
        datetime(2020, 4, 1, 13, 59, 59),
        datetime(2020, 4, 1, 14, 59, 59),
        datetime(2020, 4, 1, 15, 59, 59),
        datetime(2020, 4, 1, 16, 59, 59),
        datetime(2020, 4, 1, 17, 59, 59),
        datetime(2020, 4, 1, 18, 59, 59),
        datetime(2020, 4, 1, 19, 59, 59),
        datetime(2020, 4, 1, 20, 59, 59),
        datetime(2020, 4, 1, 21, 59, 59),
    ]


def test_datetime_calculate() -> None:
    """计算时间间隔"""

    # 起始时间
    start = date(2022, 4, 1)
    # 结束时间
    until = date(2022, 4, 20)

    # 计算两个时间间隔的周
    weeks = rr.rrule(freq=rr.WEEKLY, dtstart=start, until=until)
    assert list(weeks) == [
        datetime(2022, 4, 1),
        datetime(2022, 4, 8),
        datetime(2022, 4, 15),
    ]

    # 指定休息日
    days_off = {rr.SA, rr.SU}
    # 计算工作日
    work_days = [w for w in rr.weekdays if w not in days_off]

    # 计算指定时间段内的工作日
    dates = rr.rrule(
        freq=rr.DAILY,
        dtstart=start,
        until=until,
        byweekday=work_days,
    )
    assert list(dates) == [
        datetime(2022, 4, 1),
        datetime(2022, 4, 4),
        datetime(2022, 4, 5),
        datetime(2022, 4, 6),
        datetime(2022, 4, 7),
        datetime(2022, 4, 8),
        datetime(2022, 4, 11),
        datetime(2022, 4, 12),
        datetime(2022, 4, 13),
        datetime(2022, 4, 14),
        datetime(2022, 4, 15),
        datetime(2022, 4, 18),
        datetime(2022, 4, 19),
        datetime(2022, 4, 20),
    ]
