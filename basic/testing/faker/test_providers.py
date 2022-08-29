import random

from faker import Faker
from faker.providers import BaseProvider, DynamicProvider


class CustomProvider(BaseProvider):
    """
    自定义静态用例生成器类型
    """

    def number(self, min_value: int, max_value: int) -> int:
        """
        提供一个随机整数测试用例

        Args:
            min_value (int): 随机整数的最小值
            max_value (int): 随机整数的最大值

        Returns:
            int: 随机整数测试用例值
        """
        return random.randint(min_value, max_value)


fake = Faker()

# 将自定义生成器加入到 Faker 对象中管理
fake.add_provider(CustomProvider)


def test_static_custom_provider() -> None:
    """
    测试静态自定义测试用例生成器
    """
    # 调用 CustomProvider 类型的 number 方法, 产生一个随机整数值
    value = fake.number(1, 100)

    # 确认产生的结果类型
    assert isinstance(value, int)
    # 确认产生的结果范围
    assert 1 <= value <= 100


# 实例化一个动态生成器对象, 用于产生医学专业前缀
medical_professions_provider = DynamicProvider(
    provider_name="medical_profession",
    elements=["dr.", "doctor", "nurse", "surgeon", "clerk"],
)

# 将自定义生成器加入到 Faker 对象中管理
fake.add_provider(medical_professions_provider)


def test_dynamic_custom_provider() -> None:
    """
    测试动态用例生成器
    """
    # 调用 medical_professions_provider 产生测试用例值
    value = fake.medical_profession()

    # 确认用例值在指定的范围内
    assert value in {"dr.", "doctor", "nurse", "surgeon", "clerk"}
