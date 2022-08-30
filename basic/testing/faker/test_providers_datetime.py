# 演示时间日期相关的测试用例提供者
import re

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

    ```
    date(
        pattern: str = '%Y-%m-%d',
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
    - `end_datetime` 参数, 最大的时间
    """
