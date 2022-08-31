# 演示时间日期相关的测试用例提供者
import re
from datetime import date, datetime, timedelta

import pytz
from dateutil.relativedelta import relativedelta
from faker import Faker

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
