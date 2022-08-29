import random
import re

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


def test_base_provider_bothify() -> None:
    """
    通过 `bothify` 方法产生任意数字和字母组合的字符串, 其定义如下:

    ```
    bothify(
        text: str = '## ??',
        letters: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ) -> str
    ```

    其中, `#` 占位符表示一个数字, `?` 占位符表示一个字母. 字母的范围由 `letters` 参数确
    定, 默认为全部英文字母 (含大小写)
    """
    value = fake.bothify("###:??", letters="AB")
    assert re.match(r"^\d{3}:[AB]{2}$", value)


def test_base_provider_filter_by_length() -> None:
    """
    对输入的集合依照长度进行过滤, 集合表示任意具有 `__len__` 操作符的集合对象, 如 `list`,
    `str`, `set` 等, 其定义如下:

    ```
    staticfilter_by_length(
        elements: Collection[T] = ('a', 'b', 'c'),
        max_element_length: Optional[int] = None,
        min_element_length: Optional[int] = None
    ) -> Collection[T]  # 返回符合要求的集合列表
    ```

    - `elements` 一组集合组成的列表
    - `max_element_length` 允许的集合最大长度
    - `min_element_length` 允许的集合最小长度
    """
    # 初始化集合, 包含 10 个列表集合, 每个列表集合的长度在 1~20 之间
    elements = [
        [n for n in range(1, random.randint(1, 20))]
        for _ in range(10)
    ]

    # 从前一个集合中过滤出长度在 1~10 之间的结果
    value = fake.filter_by_length(
        elements=elements,
        min_element_length=1,
        max_element_length=10,
    )

    assert 1 <= len(value) <= 10


def test_base_provider_hexify() -> None:
    """
    产生任意一位 16 进制数字, 其定义如下:

    ```
    hexify(
        text: str = '^^^^',
        upper: bool = False
    ) -> str
    ```

    - `^` 占位符表示一位 16 进制数字
    - `upper` 参数为 `True` 表示 `A`~`F` 用大写字母
    """
    value = fake.hexify(text="MAC Address: ^^:^^:^^:^^:^^:^^")
    assert re.match(r"MAC Address: (:?[0-9a-f]{2}){6}", value)


def test_base_provider_language_code() -> None:
    """
    产生一个随机的 i18n 语言代码 (例如: `en`, `zh`), 其定义如下:

    ```
    language_code(
        min_length: Optional[int] = None,
        min_length: Optional[int] = None
    ) -> str
    ```

    - `min_length` 表示所产生的语言代码的最小长度, 默认为 2
    - `max_length` 表示所产生的语言代码的最大长度, 默认为 3
    """
    # 获取语言代码
    value = fake.language_code()

    # 确认语言代码的长度范围
    assert 2 <= len(value) <= 3


def test_base_provider_lexify() -> None:
    """
    """
    value = fake.lexify(text='Random Identifier: ??????????')
