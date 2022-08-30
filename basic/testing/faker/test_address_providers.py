# 介绍产生各种地址用例的操作
import re

from faker import Faker

fake = Faker()


def test_address_providers() -> None:
    """
    产生一个随机的地址, 其定义如下:

    ```
    address() -> str
    ```
    """
    value = fake.address()
    assert isinstance(value, str)


def test_address_providers_building_number() -> None:
    """
    产生一个随机的楼号, 其定义如下:

    ```
    building_number() -> str
    ```
    """
    value = fake.building_number()

    # 确认产生的楼号是数字字符组成的字符串
    assert isinstance(value, str)
    assert int(value) is not None


def test_address_providers_city() -> None:
    """
    产生一个随机的城市名称, 其定义如下:

    ```
    city() -> str
    ```
    """
    value = fake.city()
    assert isinstance(value, str)


def test_address_providers_city_suffix() -> None:
    """
    随机产生一个城市后缀, 其定义如下:

    ```
    city_suffix(
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ) -> str
    ```

    其中:
    - `min_length` 后缀的最小长度
    - `max_length` 后缀的最大长度
    """
    value = fake.city_suffix(
        min_length=2,
        max_length=10,
    )
    assert 2 <= len(value) <= 10


def test_address_providers_country() -> None:
    """
    随机产生一个国家名称, 其定义如下:

    ```
    country(
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ) -> str
    ```
    """
    value = fake.country(min_length=2, max_length=4)
    assert 2 <= len(value) <= 4


def test_address_providers_country_code() -> None:
    """
    产生一个随机的国家编码, 其定义如下:

    ```
    country_code(
        representation: str = 'alpha-2'
    ) -> str
    ```

    其中:
    - `representation` 参数表示国家代码的标准, 默认为 ISO 3166-1 alpha-2,
      ISO 3166-1 为国际标准, alpha-2 表示用 2 个字母表示
    """
    value = fake.country_code()
    assert len(value) == 2


def test_address_providers_current_country() -> None:
    """
    获取当前国家名称, 其定义如下:

    ```
    current_country_code() -> str
    ```

    注意: `Faker` 类型的默认构造器传递的本地化代码为 `"en_US"`, 所以
    `current_country` 返回的值为 "United States", 如果改为 `"zh_CN"`, 则
    `current_country` 返回的值为 "People's Republic of China"
    """
    value = fake.current_country()
    assert value == "United States"


def test_address_providers_postcode() -> None:
    """
    获取一个随机的邮政编码

    ```
    postcode() -> str
    ```
    """
    value = fake.postcode()

    # 确认产生邮编是由数字字符组成的
    assert int(value) is not None


def test_address_providers_street_address() -> None:
    """
    随机产生一个精确到街道的地址数据, 定义如下:

    ```
    street_address() -> str
    ```
    """
    # 产生一个街道地址数据
    value = fake.street_address()

    # 确认街道地址数据的格式
    assert re.match(r"\d+[\s\w]+\s*\d*", value)


def test_address_providers_street_name() -> None:
    """
    随机产生一个街道名称, 其定义如下:

    ```
    street_name() -> str
    ```
    """
    value = fake.street_name()

    # 确认街道数据符合要求
    assert re.match(r"\w+\s\w+", value)


def test_address_providers_street_suffix() -> None:
    """
    随机产生一个街道名称的后缀, 其定义如下:

    ```
    street_suffix(
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ) -> str
    ```

    其中:
    - `min_length` 参数表示后缀的最小长度
    - `max_length` 参数表示后缀的最大长度
    """
    value = fake.street_suffix(min_length=2, max_length=4)

    # 确认产生的后缀长度范围
    assert 2 <= len(value) <= 4
