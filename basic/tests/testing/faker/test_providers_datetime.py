# 演示时间日期相关的测试用例提供者
import re
from datetime import date, datetime, time, timedelta, tzinfo
from typing import Iterable

import pytz
from dateutil.relativedelta import relativedelta
from faker import Faker

from basic.testing.faker import last_day_of_month

fake = Faker()


def test_provider_am_pm() -> None:
    """随机产生 AM 或 PM 的标记

    其定义如下:

    ```python
    am_pm() -> str
    ```
    """
    value = fake.am_pm()
    # 确认产生的值是 AM 或 PM
    assert value in {"AM", "PM"}


def test_provider_century() -> None:
    """产生 `1`~`12` 的罗马数字

    其定义如下:

    ```python
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
    """产生一个从 1970-01-01 到当前时间的随机日期字符串

    其定义如下:

    ```python
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
    """产生一个在指定时间范围内的日期字符串

    ```python
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
    """产生一个在指定时间范围内的日期字符串

    产生类似于 `date_between` 方法, 但 `date_start` 或 `date_end` 参数可以非必填, 表示不设上限或下限

    ```python
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
    """产生一个从 1970-01-01 到当前时间的随机日期对象

    其定义如下:

    ```python
    date_object(
        end_datetime: datetime.datetime = None
    ) -> datetime.date
    ```

    其中:
    - `end_datetime` 参数, 最大的时间, 产生的日期不会超过这个时间
    """
    # 产生一个 2000-01-01 之前的日期
    value = fake.date_object(end_datetime=datetime.fromisoformat("2000-01-01T12:00:00"))
    assert value <= datetime.fromisoformat("2000-01-01T12:00:00").date()


def test_provider_date_of_birth() -> None:
    """产生一个指定年龄范围内的随机生日

    ```python
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
    """产生近一个世纪 (100 年) 内的随机日期

    其定义如下:

    ```python
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
    """产生近 10 年内的随机日期

    其定义如下:

    ```python
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
    """产生近 1 个月内的随机日期

    其定义如下:

    ```python
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
    """产生近 1 年内的随机日期

    其定义如下:

    ```python
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
    """获取一个从 1970-01-01 00:00 到当前时间的随机时间对象

    ```python
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
    """获取一个从公元后 (0001-01-01 00:00:00) 到当前时间的随机时间对象

    ```python
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
    # 注意, start_time 和 end_time 均为设置时区, 比较时也需要删除 value 的时区
    assert start_time <= value.replace(tzinfo=None) <= end_time


def test_provider_date_time_between() -> None:
    """获取指定两个时间之间的随机时间

    其定义如下:

    ```python
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
    start_date = date.fromisoformat("2022-10-01")
    end_date = date.fromisoformat("2022-10-15")

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
    # 注意, start_time 和 end_time 均为设置时区, 比较时也需要删除 value 的时区
    assert start_date <= value.date() <= end_date


def test_provider_date_time_between_dates() -> None:
    """获取指定两个时间之间的随机时间

    和 `date_time_between` 方法类似, 但 `datetime_start` 和 `datetime_end` 参数可以为 `None`, 表示不设限制:

    ```python
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
    # 注意, start_time 和 end_time 均为设置时区, 比较时也需要删除 value 的时区
    assert datetime_start <= value.replace(tzinfo=None) <= datetime_end


def test_provider_date_time_this_century() -> None:
    """产生近一个世纪 (100 年) 内的随机时间

    其定义如下:

    ```python
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
    """产生近 10 年内的随机时间

    其定义如下:

    ```python
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
    """产生当前月内的随机时间

    其定义如下:

    ```python
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
    value: datetime = fake.date_time_this_month(
        before_now=False,
        after_now=True,
        tzinfo=zone,
    )

    today = date.today()

    # 计算下个月 1 号 0 点的时间
    if today.month < 12:
        end_of_month = zone.localize(
            datetime(today.year, today.month + 1, 1, 0, 0, 0),
        )
    else:
        end_of_month = zone.localize(
            datetime(today.year + 1, 1, 1, 0, 0, 0),
        )

    assert value >= zone.localize(datetime.now())
    assert value < end_of_month


def test_provider_date_time_this_year() -> None:
    """产生今年内的随机时间

    其定义如下:

    ```python
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
    """获取一个随机日期, 取值从 `1`~`31`

    ```python
    day_of_month() -> str
    ```
    """
    value = fake.day_of_month()

    # 确认返回的值在指定范围内
    assert 1 <= int(value) <= 31


def test_provider_day_of_week() -> None:
    """获取一个随机星期

    取值包括: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"

    ```python
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


def test_provider_future_date() -> None:
    """获取从当天到 `end_date` 之间的随机日期

    其定义如下:

    ```python
    future_date(
        end_date: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int
        ] = "+30d",
        tzinfo: Optional[datetime.tzinfo] = None
    ) -> datetime.date
    ```

    其中:
    - `end_date` 参数用于设置日期限制, 获取的随机日期不能大于该时间
    - `tzinfo`参数用于设置时区
    """
    today = date.today()

    end_date = today + timedelta(days=100)

    # 获取当前日期到 end_date 之间的随机日期
    value = fake.future_date(end_date=end_date)

    # 确认获取的日期在指定范围内
    assert today <= value <= end_date


def test_provider_future_datetime() -> None:
    """获取当前到 `end_date` 之间的随机时间

    其定义如下:

    ```python
    future_datetime(
        end_date: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int
        ] = "+30d",
        tzinfo: Optional[datetime.tzinfo] = None
    ) -> datetime.datetime
    ```

    其中:
    - `end_date` 参数用于设置日期限制, 获取的随机时间不能大于该时间
    - `tzinfo`参数用于设置时区
    """
    zone = pytz.timezone("Asia/Shanghai")
    now = zone.localize(datetime.now())

    end_time = now + timedelta(days=100)

    # 获取当前时间到 end_date 之间的随机时间
    value = fake.future_datetime(end_date=end_time, tzinfo=zone)

    # 确认获取的时间在指定范围内
    assert now <= value <= end_time


def test_provider_iso8601() -> None:
    """获取一个符合 iso8601 规范的时间字符串

    其定义如下:

    ```python
    iso8601(
        tzinfo: Optional[datetime.tzinfo] = None,
        end_datetime: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int,
            None
        ] = None,
        sep: str = "T",
        timespec: str = "auto"
    ) -> str
    ```

    其中:
    - `tzinfo`参数用于设置时区
    - `end_datetime` 参数用于设置日期限制, 获取的随机事件不能大于该事件
    - `sep` 参数用于设置日期和时间之间的分割字符
    - `timespec` 参数用于指定时间部分格式的说明, 包括: `"auto"`, `"hours"`,
      `"minutes"`, `"seconds"`, `"milliseconds"` 和 `"microseconds"`

    对于 `sep` 和 `timespec` 参数, 可以参考 `datetime.isoformat` 函数的说明
    """
    zone = pytz.timezone("Asia/Shanghai")
    now = zone.localize(datetime.now())

    end_time = now + timedelta(days=30)

    value = fake.iso8601(
        tzinfo=zone,
        end_datetime=end_time,
    )

    assert isinstance(value, str)

    # 确认获取的字符串符合 iso8601 格式
    assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.?\d*\+\d{2}:\d{2}$", value)


def test_provider_month() -> None:
    """产生随机的月份, 取值 `01`~`12`

    其定义如下:

    ```python
    month() -> str
    ```
    """
    all_month = {f"{m:0>2}" for m in range(1, 13)}

    value = fake.month()

    # 确认产生的月份正确
    assert value in all_month


def test_provider_month_name() -> None:
    """返回随机月份的名称

    其定义如下:

    ```python
    month_name() -> str
    ```
    """
    all_month = {
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    }

    # 获取随机的月份名称
    value = fake.month_name()

    # 判断返回值正确
    assert value in all_month


def test_provider_past_date() -> None:
    """获取从 `start_date` 到当前日期之间的随机日期

    其定义如下:

    ```python
    past_date(
        start_date : Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int
        ] = "-30d",
        tzinfo: Optional[datetime.tzinfo] = None
    ) -> datetime.date
    ```

    其中:
    - `start_date ` 参数用于设置日期限制, 获取的随机日期不小于该时间
    - `tzinfo`参数用于设置时区
    """
    zone = pytz.timezone("Asia/Shanghai")
    today = date.today()

    start_date = today - timedelta(days=100)

    # 获取 start_date 到当前日期的随机日期
    value = fake.past_date(start_date=start_date, tzinfo=zone)

    # 确认获取的日期在指定范围内
    assert start_date <= value <= today


def test_provider_past_datetime() -> None:
    """获取从 `start_date` 到当前之间的随机时间

    其定义如下:

    ```python
    past_datetime(
        start_date: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int
        ] = "-30d",
        tzinfo: Optional[datetime.tzinfo] = None
    ) -> datetime.datetime
    ```

    其中:
    - `start_date` 参数用于设置日期限制, 获取的随机时间不小于该时间
    - `tzinfo`参数用于设置时区
    """
    zone = pytz.timezone("Asia/Shanghai")
    now = zone.localize(datetime.now())

    start_date = now - timedelta(days=100)

    # 获取 start_date 到当前时间之间的随机时间
    value = fake.past_datetime(start_date=start_date, tzinfo=zone)

    # 确认获取的时间在指定范围内
    assert start_date <= value <= now


def test_provider_pytimezone() -> None:
    """产生一个随机的 timezone 对象

    可作为 `tzinfo` 参数用于 `datetime.datetime` 函数或其它 fakers

    ```python
    pytimezone(*args, **kwargs) -> Optional[datetime.tzinfo]
    ```
    """
    value = fake.pytimezone()

    # 确认返回结果为 dateutil.tz.tzfile 类型
    assert isinstance(value, tzinfo)


def test_provider_time() -> None:
    """产生一个随机时间字符串 (默认为 24 小时制)

    其定义如下:

    ```python
    time(
        pattern: str = "%H:%M:%S",
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
    - `pattern` 参数, 定义时间字符串的格式
    - `end_datetime` 参数, 定义随机时间字符串的下限
    """
    end_time = datetime.now() + timedelta(days=30)

    # 获取一个日期字符串
    value = fake.time(end_datetime=end_time)

    # 确认返回值符合定义的格式
    assert re.match(r"\d{2}:\d{2}:\d{2}", value)


def test_provider_time_delta() -> None:
    """获取一个随机的 `datetime.timedelta` 对象

    ```python
    time_delta(
        end_datetime: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int,
            None
        ] = None
    ) -> datetime.timedelta
    ```

    其中:
    - `end_datetime` 参数, 定义时间的下限, 即获取的 `timedelta` 加上当前时间不能大于这个参数值
    """
    end_time = datetime.now() + timedelta(days=30)

    value = fake.time_delta(end_datetime=end_time)

    # 确认返回值的类型
    assert isinstance(value, timedelta)

    # 确认返回值在规定范围内
    assert datetime.now() + value <= end_time


def test_provider_time_object() -> None:
    """获取一个随机时间对象

    其定义如下:

    ```python
    time_object(
        end_datetime: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int,
            None
        ] = None
    ) -> datetime.time
    ```

    其中:
    - `end_datetime` 参数, 获取的随机时间不会大于这个时间. 但注意, 这个范围是一个时间日期的上限, 但返回的结果是一个时间对象.
    """
    # 获取一个不小于当前时间 2 小时范围的时间对象
    date_val = fake.time_object(
        end_datetime=datetime.now() + timedelta(hours=2),
    )

    assert isinstance(date_val, time)

    # 由于 +2h 是在当期时间日期上加 2 小时, 所以比较时也要将返回的时间对象合并日期才能比较
    # 将获取的时间对象加上当前日期, 合并为时间日期对象
    datetime_val = datetime.combine(date.today(), date_val)

    # 确认时间对象的范围
    assert datetime_val <= datetime.now() + timedelta(hours=2)


def test_provider_time_series() -> None:
    """产生一个序列, 元素为 `(datetime, value)`

    `datetime` 取值在 `start_date` 和 `end_date` 参数指定的时间范围内, `value` 是一个回调函数返回的值, 其定义如下:

    ```python
    time_series(
        start_date: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int
        ] = "-30d",
        end_date: Union[
            datetime.date,
            datetime.datetime,
            datetime.timedelta,
            str,
            int
        ] = "now",
        precision: Optional[float] = None,
        distrib: Optional[Callable[[datetime.datetime], float]] = None,
        tzinfo: Optional[datetime.tzinfo] = None
    ) -> Iterator[Tuple[datetime.datetime, Any]]
    ```

    其中:
    - `start_date` 参数表示产生时间序列的起始日期时间
    - `end_date` 参数表示产生时间序列的结束时间日期
    - `precision` 参数指定了产生日期时间序列的精度
    - `distrib` 参数表示一个回调函数, 用于产生序列的第二个值
    - `tzinfo` 参数表示一个时区
    """
    zone = pytz.timezone("Asia/Shanghai")

    # 设定时间序列的起始时间
    # 需要将毫秒部分去掉
    start_date = zone.localize(datetime.now() - timedelta(days=30)).replace(
        microsecond=0
    )

    # 设定时间序列的结束时间
    # 需要将毫秒部分去掉
    end_date = zone.localize(datetime.now() + timedelta(days=10)).replace(microsecond=0)

    now = zone.localize(datetime.now())

    # 产生一个日期时间序列
    value = fake.time_series(
        start_date=start_date,
        end_date=end_date,
        distrib=lambda d: (now - d).total_seconds(),  # tuple 第二项为当前时间和产
        # 生时间相差的秒数
        tzinfo=zone,
    )
    assert isinstance(value, Iterable)

    # 查看序列中的每个时间日期对象
    for v in value:
        assert len(v) == 2

        # tuple 第一项为产生的日期时间, 确认这个时间的范围
        assert start_date <= v[0] <= end_date

        # tuple 第二项为当前日期时间和产生日期时间相差的秒数
        assert (now - v[0]).total_seconds() == v[1]


def test_provider_timezone() -> None:
    """获取一个随机的时区字符串

    例如: `"Indian/Maldives"`, `"America/Barbados"` 这样的格式, 其定义如下:

    ```python
    timezone() -> str
    ```
    """
    value = fake.timezone()

    # 确认获取的值表示一个时区
    assert value in pytz.all_timezones_set


def test_provider_unix_time() -> None:
    """产生一个随机的 unix 时间戳

    其定义如下:

    ```python
    unix_time(
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
    ) -> int
    ```

    其中:
    - `end_datetime` 参数表示产生时间戳的结束日期时间点
    - `start_datetime` 参数表示产生时间戳的起始日期时间点
    """
    now = datetime.now()

    start_datetime = now - timedelta(hours=1)
    end_datetime = now + timedelta(hours=1)

    # 产生一个在指定范围内的随机 unix 时间戳
    timestamp = fake.unix_time(
        start_datetime=start_datetime.astimezone(tz=pytz.utc),
        end_datetime=end_datetime.astimezone(tz=pytz.utc),
    )

    # 从 unix 时间戳创建时间日期对象
    # 注意: unix 时间戳是 UTC 时间
    datetime_val = datetime.fromtimestamp(timestamp)

    # 确认生成的 unix 时间戳在指定范围内
    assert start_datetime <= datetime_val <= end_datetime


def test_provider_year() -> None:
    """产生一个随机的年份

    其定义如下:

    ```python
    year() -> str
    ```
    """
    value = fake.year()
    assert 1970 <= int(value) <= 9999
