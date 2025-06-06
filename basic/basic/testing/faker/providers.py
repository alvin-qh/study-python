import random

from faker.providers import BaseProvider, DynamicProvider


class RandomNumberProvider(BaseProvider):
    """自定义静态用例生成器类型"""

    def number(self, min_value: int, max_value: int) -> int:
        """提供一个随机整数测试用例

        Args:
            - `min_value` (`int`): 随机整数的最小值
            - `max_value` (`int`): 随机整数的最大值

        Returns:
            `int`: 随机整数测试用例值
        """
        return random.randint(min_value, max_value)


# 实例化一个动态生成器对象, 用于产生医学专业前缀
MedicalProfessionsProvider = DynamicProvider(
    provider_name="medical_profession",
    elements=[
        "dr.",
        "doctor",
        "nurse",
        "surgeon",
        "clerk",
    ],
)
