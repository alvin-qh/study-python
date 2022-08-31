# 演示时间日期相关的测试用例提供者
import re
from datetime import date, datetime, timedelta

import pytz
from dateutil.relativedelta import relativedelta
from faker import Faker

from .date_calculate import last_day_of_month

fake = Faker()


def test_provider_am_pm() -> None:
    """
    随机产生 AM 或 PM 的标记, 其定义如下:

    ```
    am_pm() -> str
    ```
    """
    value = fake.am_pm()
    # 确认产生的值是 AM 或 PM
    assert value in {"AM", "PM"}


def test_provider_century() -> None:
    """
    产生 `1`~`12` 的罗马数字, 其定义如下:

    ```
    century(
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ) -> str
    ```

    其中:
    - `min_length` 参数, 产生结果的最小长度
    - `max_length` 参数, 产生结果的最大长度
    """
    value = fake.century()
    # 确定结果由罗马数字组成
    assert re.match(r"^[IVX]+$", value)


def test_provider_date() -> None:
    """
    产生一个从 1970-01-01 到当前时间的随机日期字符串, 其定义如下:

    ```
    date(
        pattern: str = "%Y-%m-%d",
        end_datetime: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int,
            None
        ] = None
    ) -> str
    ```

    其中:
    - `pattern` 参数, 定义产生日期时间的格式
    - `end_datetime` 参数, 最大的时间, 产生的日期不会超过这个时间
    """
    value = fake.date(end_datetime=timedelta(days=3))
    # 确认产生的是标准 ISO 日期格式字符串
    assert date.fromisoformat(value)


def test_provider_date_between() -> None:
    """
    产生一个在指定时间范围内的日期字符串

    ```
    date_between(
        start_date: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int
        ] = "-30y",
        end_date: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int
        ] = "today"
    ) -> datetime.date
    ```

    其中:
    - `start_date` 参数表示日期范围的起始, 默认 30 天前
    - `end_date` 参数表示日期范围的终止, 默认当天
    """
    start_date = date.fromisoformat("2010-01-01")
    end_date = date.fromisoformat("2010-01-31")

    # 产生一个在 start_date 和 end_date 之间的日期
    value = fake.date_between(
        start_date=start_date,
        end_date=end_date,
    )

    assert start_date <= value <= end_date


def test_provider_date_between_dates() -> None:
    """
    产生一个在指定时间范围内的日期字符串, 类似于 `date_between` 方法, 但 `date_start`
    或 `date_end` 参数可以非必填, 表示不设上限或下限

    ```
    date_between_dates(
        date_start: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int,
            None
        ] = None,
        date_end: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int,
            None
        ] = None
    ) -> datetime.date
    ```

    其中:
    - `date_start` 参数表示日期范围的起始, 默认不限制
    - `date_end` 参数表示日期范围的终止, 默认不限制
    """
    date_start = date.fromisoformat("2010-01-01")
    date_end = date.fromisoformat("2010-01-31")

    # 产生一个在 start_date 和 end_date 之间的日期
    value = fake.date_between_dates(
        date_start=date_start,
        date_end=date_end,
    )

    assert date_start <= value <= date_end


def test_provider_date_object() -> None:
    """
    产生一个从 1970-01-01 到当前时间的随机日期对象, 其定义如下:

    ```
    date_object(
        end_datetime: datetime.datetime = None
    ) -> datetime.date
    ```

    其中:
    - `end_datetime` 参数, 最大的时间, 产生的日期不会超过这个时间
    """
    # 产生一个 2000-01-01 之前的日期
    value = fake.date_object(
        end_datetime=datetime.fromisoformat("2000-01-01T12:00:00")
    )
    assert value <= datetime.fromisoformat("2000-01-01T12:00:00").date()


def test_provider_date_of_birth() -> None:
    """
    产生一个指定年龄范围内的随机生日

    ```
    date_of_birth(
        tzinfo: Optional[datetime.tzinfo] = None,
        minimum_age: int = 0,
        maximum_age: int = 115
    ) -> datetime.date
    ```

    其中:
    - `tzinfo` 参数, 设置时区, 默认为实例化 `Faker` 对象时指定国家代码的时区
    - `minimum_age` 参数, 年级最小值
    - `maximum_age` 参数, 年级最大值
    """
    # 产生一个东八区, 18 ~ 35 岁之间的生日日期对象
    value = fake.date_of_birth(
        tzinfo=pytz.timezone("Asia/Shanghai"),
        minimum_age=18,
        maximum_age=35,
    )

    # 将计算的日期换算回年龄
    age = relativedelta(date.today(), value)
    assert 18 <= age.years <= 35


def test_provider_date_this_century() -> None:
    """
    产生近一个世纪 (100 年) 内的随机日期, 其定义如下:

    ```
    date_this_century(
        before_today: bool = True,
        after_today: bool = False
    ) -> datetime.date
    ```

    其中:
    - `before_today` 参数, 是否产生当日之前的日期
    - `after_today` 参数, 是否产生当日之后的日期
    """
    # 获取一个不小于当天的本世纪随机日期
    value = fake.date_this_century(
        before_today=False,
        after_today=True,
    )

    # 计算本世纪最后一天的日期
    end_of_century = date(int(date.today().year // 100 * 100) + 100, 12, 31)

    assert value >= date.today()
    assert value <= end_of_century


def test_provider_date_this_decade() -> None:
    """
    产生近 10 年内的随机日期, 其定义如下:

    ```
    date_this_decade(
        before_today: bool = True,
        after_today: bool = False
    ) -> datetime.date
    ```

    其中:
    - `before_today` 参数, 是否产生当日之前的日期
    - `after_today` 参数, 是否产生当日之后的日期
    """
    # 获取一个不小于当天的近 10 年随机日期
    value = fake.date_this_decade(
        before_today=False,
        after_today=True,
    )

    # 计算近 10 年最后一天的日期
    end_of_decade = date(int(date.today().year // 10 * 10) + 10, 12, 31)

    assert value >= date.today()
    assert value <= end_of_decade


def test_provider_date_this_month() -> None:
    """
    产生近 1 个月内的随机日期, 其定义如下:

    ```
    date_this_month(
        before_today: bool = True,
        after_today: bool = False
    ) -> datetime.date
    ```

    其中:
    - `before_today` 参数, 是否产生当日之前的日期
    - `after_today` 参数, 是否产生当日之后的日期
    """
    # 获取一个不小于当天的近一月的随机日期
    value = fake.date_this_month(
        before_today=False,
        after_today=True,
    )

    today = date.today()

    # 计算近一个月最后一天的日期
    end_of_month = date(
        today.year,
        today.month,
        last_day_of_month(today.year, today.month),
    )

    assert value >= date.today()
    assert value <= end_of_month


def test_provider_date_this_year() -> None:
    """
    产生近 1 年内的随机日期, 其定义如下:

    ```
    date_this_year(
        before_today: bool = True,
        after_today: bool = False
    ) -> datetime.date
    ```

    其中:
    - `before_today` 参数, 是否产生当日之前的日期
    - `after_today` 参数, 是否产生当日之后的日期
    """
    # 获取一个不小于当天的近一年的随机日期
    value = fake.date_this_year(
        before_today=False,
        after_today=True,
    )

    today = date.today()

    # 计算近一年年最后一天的日期
    end_of_year = date(today.year, 12, 31)

    assert value >= date.today()
    assert value <= end_of_year


def test_provider_date_time() -> None:
    """
    获取一个从 1970-01-01 00:00 到当前时间的随机时间对象

    ```
    date_time(
        tzinfo: Optional[datetime.tzinfo] = None,
        end_datetime: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int,
            None
        ] = None
    ) -> datetime.datetime
    ```

    其中:
    - `tzinfo` 参数, 表示要获取时间的时区
    - `end_datetime` 参数, 要生成时间的截止时间
    """
    zone = pytz.timezone("Asia/Shanghai")

    value: datetime = fake.date_time(tzinfo=zone, end_datetime="-2day1hour")

    tz = value.tzinfo
    assert tz

    # 计算时间的时区偏移量
    offset = tz.utcoffset(value)
    assert offset
    # 确认生成的时间日期的时区为东八区
    assert offset.seconds // 3600 == 8

    # 确认生成时间日期的范围
    end_datetime = datetime.now(tz=zone) - timedelta(days=-2, hours=-1)
    assert value <= end_datetime


def test_provider_date_time_ad() -> None:
    """
    获取一个从公元后 (0001-01-01 00:00:00) 到当前时间的随机时间对象

    ```
    date_time_ad(
        tzinfo: Optional[datetime.tzinfo] = None,
        end_datetime: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int,
            None
        ] = None,
        start_datetime: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int,
            None
        ] = None
    ) -> datetime.datetime
    ```

    其中:
    - `tzinfo` 参数, 表示要获取时间的时区
    - `end_datetime` 参数, 要生成时间的截止时间
    - `start_datetime` 参数, 要生成时间的起始时间
    """
    zone = pytz.timezone("Asia/Shanghai")
    start_time = datetime.fromisoformat("0998-01-01T12:00")
    end_time = datetime.fromisoformat("1000-01-01T00:00")

    value: datetime = fake.date_time_ad(
        tzinfo=zone,
        end_datetime=end_time,
        start_datetime=start_time,
    )

    tz = value.tzinfo
    assert tz

    # 计算时间的时区偏移量
    offset = tz.utcoffset(value)
    assert offset
    # 确认生成的时间日期的时区为东八区
    assert offset.seconds // 3600 == 8

    # 确认生成时间日期的范围
    # 注意, start_time 和 end_time 均为设置时区, 比较时也需要擅长 value 的时区
    assert start_time <= value.replace(tzinfo=None) <= end_time


def test_provider_date_time_between() -> None:
    """
    获取指定两个时间之间的随机时间, 其定义如下:

    ```
    date_time_between(
        start_date: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int
        ] = "-30y",
        end_date: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int
        ] = "now",
        tzinfo: Optional[datetime.tzinfo] = None
    ) -> datetime.datetime
    ```

    其中:
    - `start_date` 参数, 要生成时间的起始时间
    - `end_date` 参数, 要生成时间的截至时间
    - `tzinfo` 参数, 表示要获取时间的时区
    """
    zone = pytz.timezone("Asia/Shanghai")
    start_date = datetime.fromisoformat("2022-10-01T12:00")
    end_date = datetime.fromisoformat("2022-10-15T00:00")

    value: datetime = fake.date_time_between(
        start_date=start_date,
        end_date=end_date,
        tzinfo=zone,
    )

    tz = value.tzinfo
    assert tz

    # 计算时间的时区偏移量
    offset = tz.utcoffset(value)
    assert offset
    # 确认生成的时间日期的时区为东八区
    assert offset.seconds // 3600 == 8

    # 确认生成时间日期的范围
    # 注意, start_time 和 end_time 均为设置时区, 比较时也需要擅长 value 的时区
    assert start_date <= value.replace(tzinfo=None) <= end_date


def test_provider_date_time_between_dates() -> None:
    """
    获取指定两个时间之间的随机时间, 和 `date_time_between` 方法类似, 但
    `datetime_start` 和 `datetime_end` 参数可以为 `None`, 表示不设限制:

    ```
    date_time_between_dates(
        datetime_start: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int,
            None
        ] = None,
        datetime_end: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int,
            None
        ] = None,
        tzinfo: Optional[datetime.tzinfo] = None
    ) -> datetime.datetime
    ```

    其中:
    - `datetime_start` 参数, 要生成时间的起始时间
    - `datetime_end` 参数, 要生成时间的截至时间
    - `tzinfo` 参数, 表示要获取时间的时区
    """
    zone = pytz.timezone("Asia/Shanghai")
    datetime_start = datetime.fromisoformat("2022-10-01T12:00")
    datetime_end = datetime.fromisoformat("2022-10-15T00:00")

    value: datetime = fake.date_time_between_dates(
        datetime_start=datetime_start,
        datetime_end=datetime_end,
        tzinfo=zone,
    )

    tz = value.tzinfo
    assert tz

    # 计算时间的时区偏移量
    offset = tz.utcoffset(value)
    assert offset
    # 确认生成的时间日期的时区为东八区
    assert offset.seconds // 3600 == 8

    # 确认生成时间日期的范围
    # 注意, start_time 和 end_time 均为设置时区, 比较时也需要擅长 value 的时区
    assert datetime_start <= value.replace(tzinfo=None) <= datetime_end


def test_provider_date_time_this_century() -> None:
    """
    产生近一个世纪 (100 年) 内的随机时间, 其定义如下:

    ```
    date_time_this_century(
        before_now: bool = True,
        after_now: bool = False,
        tzinfo: Optional[datetime.tzinfo] = None
    ) -> datetime.datetime
    ```

    其中:
    - `before_now` 参数, 是否产生当时之前的时间
    - `after_now` 参数, 是否产生当时之后的时间
    - `tzinfo` 参数, 表示要获取时间的时区
    """
    zone = pytz.timezone("Asia/Shanghai")

    # 获取一个不小于当前时间的本世纪内的随机时间
    value = fake.date_time_this_century(
        before_now=False,
        after_now=True,
        tzinfo=zone,
    )

    # 计算下世纪第一天 0 点的时间
    end_of_century = zone.localize(
        datetime(int(date.today().year // 100 * 100) + 101, 1, 1, 0, 0, 0),
    )

    assert value >= zone.localize(datetime.now())
    assert value < end_of_century


def test_provider_date_time_this_decade() -> None:
    """
    产生近 10 年内的随机时间, 其定义如下:

    ```
    date_time_this_decade(
        before_now: bool = True,
        after_now: bool = False,
        tzinfo: Optional[datetime.tzinfo] = None
    ) -> datetime.datetime
    ```

    其中:
    - `before_now` 参数, 是否产生当时之前的时间
    - `after_now` 参数, 是否产生当时之后的时间
    - `tzinfo` 参数, 表示要获取时间的时区
    """
    zone = pytz.timezone("Asia/Shanghai")

    # 获取一个不小于当前时间的近 10 年随机时间
    value = fake.date_time_this_decade(
        before_now=False,
        after_now=True,
        tzinfo=zone,
    )

    # 计算近 11 年 1 号 0 点时间
    end_of_decade = zone.localize(
        datetime(int(date.today().year // 10 * 10) + 11, 1, 1, 0, 0, 0),
    )

    assert value >= zone.localize(datetime.now())
    assert value < end_of_decade


def test_provider_date_time_this_month() -> None:
    """
    产生当前月内的随机时间, 其定义如下:

    ```
    date_time_this_month(
        before_now: bool = True,
        after_now: bool = False,
        tzinfo: Optional[datetime.tzinfo] = None
    ) -> datetime.datetime
    ```

    其中:
    - `before_now` 参数, 是否产生当时之前的时间
    - `after_now` 参数, 是否产生当时之后的时间
    - `tzinfo` 参数, 表示要获取时间的时区
    """
    zone = pytz.timezone("Asia/Shanghai")

    # 获取一个不小于当前时间的当月的随机时间
    value = fake.date_time_this_month(
        before_now=False,
        after_now=True,
        tzinfo=zone,
    )

    today = date.today()

    # 计算下个月 1 号 0 点的时间
    end_of_month = zone.localize(
        datetime(today.year, today.month + 1, 1, 0, 0, 0),
    )

    assert value >= zone.localize(datetime.now())
    assert value < end_of_month


def test_provider_date_time_this_year() -> None:
    """
    产生今年内的随机时间, 其定义如下:

    ```
    date_time_this_year(
        before_now: bool = True,
        after_now: bool = False,
        tzinfo: Optional[datetime.tzinfo] = None
    ) -> datetime.datetime
    ```

    其中:
    - `before_now` 参数, 是否产生当时之前的时间
    - `after_now` 参数, 是否产生当时之后的时间
    - `tzinfo` 参数, 表示要获取时间的时区
    """
    zone = pytz.timezone("Asia/Shanghai")

    # 获取一个不小于当前时间的当年的随机时间
    value = fake.date_time_this_year(
        before_now=False,
        after_now=True,
        tzinfo=zone,
    )

    today = date.today()

    # 计算下一年 1 号 0 点的时间
    end_of_month = zone.localize(
        datetime(today.year + 1, 1, 1, 0, 0, 0),
    )

    assert value >= zone.localize(datetime.now())
    assert value < end_of_month


def test_provider_day_of_month() -> None:
    """
    获取一个随机日期, 取值从 `1`~`31`

    ```
    day_of_month() -> str
    ```
    """
    value = fake.day_of_month()

    # 确认返回的值在指定范围内
    assert 1 <= int(value) <= 31


def test_provider_day_of_week() -> None:
    """
    获取一个随机星期, 取值包括: "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"

    ```
    day_of_week() -> str
    ```
    """
    weeks = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    value = fake.day_of_week()

    # 确认返回的值在指定范围内
    assert 1 <= weeks.index(value) + 1 <= 7
