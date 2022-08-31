# 演示最基本的 providers, 包括字符, 字符串和数字的生成策略

import random
import re
from string import ascii_letters, ascii_lowercase, ascii_uppercase

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


def test_provider_bothify() -> None:
    """
    通过 `bothify` 方法产生任意数字和字母组合的字符串, 其定义如下:

    ```
    bothify(
        text: str = "## ??",
        letters: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ) -> str
    ```

    其中:
    - `text` 参数为一个模板字符串, 可以包含占符和其它字符
        - `#` 占位符表示一个数字
        - `?` 占位符表示一个字母
    - `letters` 参数表示字符的取值范围, 默认为全部英文字母 (含大小写)
    """
    value = fake.bothify("###:??", letters="AB")
    assert re.match(r"^\d{3}:[AB]{2}$", value)


def test_provider_filter_by_length() -> None:
    """
    对输入的集合依照长度进行过滤, 集合表示任意具有 `__len__` 操作符的集合对象, 如 `list`,
    `str`, `set` 等, 其定义如下:

    ```
    staticfilter_by_length(
        elements: Collection[T] = ("a", "b", "c"),
        max_element_length: Optional[int] = None,
        min_element_length: Optional[int] = None
    ) -> Collection[T]  # 返回符合要求的集合列表
    ```

    其中:
    - `elements` 参数表示一组集合组成的列表
    - `max_element_length` 参数表示允许的集合最大长度
    - `min_element_length` 参数表示允许的集合最小长度
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


def test_provider_hexify() -> None:
    """
    产生任意一位 16 进制数字, 其定义如下:

    ```
    hexify(
        text: str = "^^^^",
        upper: bool = False
    ) -> str
    ```

    其中:
    - `text` 参数为一个模板字符串, 可以包含占位符和其它字符
        - `^` 占位符表示一位 16 进制数字
    - `upper` 参数为 `True` 表示 `A`~`F` 用大写字母
    """
    value = fake.hexify(text="MAC Address: ^^:^^:^^:^^:^^:^^")
    assert re.match(r"MAC Address: (:?[0-9a-f]{2}){6}", value)


def test_provider_language_code() -> None:
    """
    产生一个随机的 i18n 语言代码 (例如: `en`, `zh`), 其定义如下:

    ```
    language_code(
        min_length: Optional[int] = None,
        min_length: Optional[int] = None
    ) -> str
    ```

    其中:
    - `min_length` 表示所产生的语言代码的最小长度, 默认为 2
    - `max_length` 表示所产生的语言代码的最大长度, 默认为 3
    """
    # 获取语言代码
    value = fake.language_code()

    # 确认语言代码的长度范围
    assert 2 <= len(value) <= 3


def test_provider_lexify() -> None:
    """
    生成任意字符, 其定义如下:

    ```
    lexify(
        text: str = "????",
        letters: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ) -> str
    ```

    其中:
    - `text` 参数为一个模板字符串, 可以包含占位符和其它字符
        - `?` 占位符表示一个任意字符
    - `letters` 参数表示字符集, 即字符的取值范围
    """
    # 产生由一组随机字符组成的字符串
    value = fake.lexify(text="Random Identifier: ??????????")

    # 确认字符串的组成符合字符集规定
    assert re.match(r"Random Identifier: [a-zA-Z]{10}", value)


def test_provider_locale() -> None:
    """
    生成随机的 i18n 本地化地区代码, 其定义如下:

    ```
    locale() -> str
    ```

    地区代码由 `2`~`3` 位小写语言代码 + `_` + `2` 位大写国家代码组成
    """
    # 产生一个本地化地区代码
    value = fake.locale()

    # 确认地区代码的组成符合规范
    assert re.match(r"[a-z]{2,3}_[A-Z]{2}", value)


def test_provider_numerify() -> None:
    """
    产生随机数字, 其定义如下:

    ```
    numerify(text: str = "###") -> str
    ```

    其中:
    - `text` 参数为一个模板字符串, 可以包含占位符和其它字符
        - `#` 占位符表示一个 `0`~`9` 之间的数字
        - `%` 占位符表示一个 `1`~`9` 之间的数字
        - `!` 占位符表示一个任意数字或空
        - `@` 占位符表示一个非零的任意数字或空
    """
    value = fake.numerify(text="Intel Core i%-%%##K vs AMD Ryzen % %%##X")
    assert re.match(
        r"Intel Core i\d\-\d{4}K vs AMD Ryzen \d \d{4}X",
        value,
    )


def test_provider_random_choices() -> None:
    """
    从已知集合中挑选指定个数的任意元素组成新的集合, 其定义如下:

    ```
    random_choices(
        elements: Collection[T] = ("a", "b", "c"),
        length: Optional[int] = None
    ) -> Sequence[T]
    ```

    其中:
    - `elements` 参数表示原集合, 从该集合中挑选元素
    - `length` 参数表示组成新集合的长度, 可以比原集合大或小, 默认为随机
    """
    elements = ["a", "b", "c", "d"]

    # 在已知集合中随机挑选元素组成新集合
    value = fake.random_choices(
        elements=elements
    )

    # 确认结果是已知集合的子集
    assert len(value) <= len(elements)
    assert all(n in elements for n in value)


def test_provider_random_digit() -> None:
    """
    产生 `0`~`9` 之间的随机数字, 其定义如下:

    ```
    random_digit() -> int
    ```
    """
    value = fake.random_digit()
    assert 0 <= value <= 9


def test_provider_random_digit_not_null() -> None:
    """
    产生 `1`~`9` 之间的随机数字, 其定义如下:

    ```
    random_digit_not_null() -> int
    ```
    """
    value = fake.random_digit_not_null()
    assert 1 <= value <= 9


def test_provider_random_digit_not_null_or_empty() -> None:
    """
     产生 `1`~`9` 之间的随机数字或一个空字符串, 其定义如下:

    ```
    random_digit_not_null_or_empty() -> Union[int, str]
    ```
    """
    value = fake.random_digit_not_null_or_empty()
    if isinstance(value, str):
        assert value == ""
    else:
        assert 1 <= value <= 9


def test_provider_random_digit_or_empty() -> None:
    """
     产生 `0`~`9` 之间的随机数字或一个空字符串, 其定义如下:

    ```
    random_digit_or_empty() -> Union[int, str]
    ```
    """
    value = fake.random_digit_or_empty()
    if isinstance(value, str):
        assert value == ""
    else:
        assert 0 <= value <= 9


def test_provider_random_element() -> None:
    """
    从集合中随机选取一个元素, 其定义如下:

    ```
    random_element(
        elements: Collection[T] = ("a", "b", "c"),
        min_element_length: Optional[int] = None,
        max_element_length: Optional[int] = None
    ) -> T
    ```

    其中:
    - `elements` 参数, 要筛选元素的集合
    - `min_element_length` 参数, 选取元素的最小范围
    - `max_element_length` 参数, 选取元素的最大范围
    """
    elements = ["a", "b", "c", "d"]

    value = fake.random_element(elements=elements)
    assert value in elements


def test_provider_random_elements() -> None:
    """
    从集合中随机选取任意若干元素并组成新的集合, 其定义如下:

    ```
    random_elements(
        elements: Collection[T] = ("a", "b", "c"),
        length: Optional[int] = None,
        unique: bool = False,
        use_weighting: Optional[bool] = None,
        min_element_length: Optional[int] = None,
        max_element_length: Optional[int] = None
    ) -> Sequence[T]
    ```

    其中:
    - `elements` 参数, 要筛选元素的集合
    - `length` 参数, 产生的新集合的长度, 可以大于或小于原集合
    - `unique` 参数, 筛选元素是否具备唯一性
    - `use_weighting` 是否使用加权计算
    - `min_element_length` 参数, 选取元素的最小范围
    - `max_element_length` 参数, 选取元素的最大范围
    """
    elements = ["a", "b", "c", "d"]

    value = fake.random_elements(
        elements=elements,
        unique=True,
    )
    assert len(value) <= len(elements)
    assert all(n in elements for n in value)


def test_provider_random_int() -> None:
    """
    产生一个随机数字, 其定义如下:

    ```
    random_int(
        min: int = 0,
        max: int = 9999,
        step: int = 1
    ) -> int
    ```

    其中:
    - `min` 参数, 表示随机数的最小值
    - `max` 参数, 表示随机数的最大值
    - `step` 参数, 表示随机数的步长
    """
    # 从 `min` 值开始, 每隔 `step` 随机取数, 直到 `max` 结束, 在此范围内随机取一个数
    value = fake.random_int(min=0, max=10, step=2)

    # 确认取值范围
    assert 0 <= value <= 10
    assert value % 2 == 0


def test_provider_random_letter() -> None:
    """
    产生一个随机字母, 包含大小写, 其定义如下:

    ```
    random_letter() -> str
    ```
    """
    # 产生一个随机字符
    value = fake.random_letter()

    # 确认产生的字符在预期范围内
    assert value in ascii_letters


def test_provider_random_letters() -> None:
    """
    产生一组指定长度的随机字母集合, 包含大小写, 其定义如下:

    ```
    random_letters(length: int = 16) -> Sequence[str]
    ```
    """
    # 产生一个随机字符
    value = fake.random_letters(length=8)

    # 确认产生的字符在预期范围内
    assert len(value) == 8
    assert all(c in ascii_letters for c in value)


def test_provider_random_lowercase_letter() -> None:
    """
    产生一个随机小写字母, 其定义如下:

    ```
    random_lowercase_letter() -> str
    ```
    """
    # 产生一个小写随机字符
    value = fake.random_lowercase_letter()

    # 确认产生的字符在预期范围内
    assert value in ascii_lowercase


def test_provider_random_number() -> None:
    """
    产生一个随机整数, 其定义如下:

    ```
    random_number(
        digits: Optional[int] = None,
        fix_len: bool = False
    ) -> int
    ```

    其中:
    - `digits` 参数, 如果为 `None` (默认值), 则生成任意随机整数; 如果为其它整数值 `n`,
      则生成 `n` 位整数
    - `fix_len` 参数, 如果为 `False`, 则生成不超过 `digits` 位数的随机整数; 如果为
      `True` 则生成等于 `digits` 位数的随机整数
    """
    value = fake.random_number(digits=3, fix_len=True)
    assert isinstance(value, int)
    assert len(str(value)) == 3


def test_provider_random_sample() -> None:
    """
    依据一个集合, 随机生成其子集合
    """
    elements = ["a", "b", "c", "d", "e", "f"]

    # 从 elements 集合中随机产生长度为 4 的子集合
    value = fake.random_sample(elements=elements, length=4)

    # 确认返回值的类型
    assert isinstance(value, list)

    # 确认返回的确是原集合的子集
    assert all(n in elements for n in value)

    # 确认返回的子集长度
    assert len(value) == 4


def test_provider_random_uppercase_letter() -> None:
    """
    产生一个随机的大写字母, 其定义如下:

    ```
    random_uppercase_letter() -> str
    ```
    """
    # 产生一个大写字母
    value = fake.random_uppercase_letter()

    # 确认产生的是大写字母
    assert value in ascii_uppercase


def test_provider_randomize_nb_elements() -> None:
    """
    产生一个在指定值附近的随机数

    ```
    randomize_nb_elements(
        number: int = 10,
        le: bool = False,
        ge: bool = False,
        min: Optional[int] = None,
        max: Optional[int] = None
    ) -> int
    ```

    其中:
    - `le` 参数: 如果为 `False` (默认值), 允许生成最多为 `number` 的 `140%`; 如果为
      `True`, 则生成的上限为 `100%`
    - `ge` 参数: 如果为 `False` (默认值), 则允许生成数量减少到 `60%`; 如果为
      `True`, 则下限生成上限为 `100%`
    - `min` 参数: 如果提供了 `min` 的数值, 则生成小于 `min` 的值不小于 `min`
      值; 如果提供了 `max` 的数值, 则生成大于 `max` 的值不大于 `max`

    如果 `le` 和 `ge` 都为 `True`, 则 `number` 的值将自动返回, 而不管 `min` 和
    `max` 的值是多少
    """
    base = 100

    # 产生一个在 100 附近, 不小于 60 且 不大于 140 的随机整数
    value = fake.randomize_nb_elements(number=base, min=60, max=140)

    # 确认在 le 和 ge 参数为 False 时, 产生的随机数和 base 值得偏差范围
    if value < base:
        assert value / base > 0.6
    elif value > base:
        assert value / base < 1.4

    # 确认产生的值得取值范围
    assert 60 <= value <= 140
