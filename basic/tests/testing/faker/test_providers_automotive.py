# 演示汽车相关的测试用例提供者
import re

from faker import Faker

fake = Faker()


def test_provider_license_plate() -> None:
    """产生一组随机的车牌号码

    其定义如下:

    ```python
    license_plate() -> str
    ```
    """
    value = fake.license_plate()
    # 确认车牌号的组成规则
    assert re.match(r"[A-Z0-9]{0,3}(\-|\s)?[A-Z0-9]{3,5}", value)
