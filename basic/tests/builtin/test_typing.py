from typing import Dict, Generic, List, Optional, Sequence, Union, TypeVar

# 定义类型 (< Python 3.12)
NumberA = Union[int, float]
NumberListA = Sequence[NumberA]

# 定义类型 (>= Python 3.12), 通过 `type` 关键字明确类型定义
type NumberB = int | float
type NumberListB = Sequence[NumberB]


def sum_a(numbers: NumberListA) -> NumberA:
    """定义一个函数, 参数和返回值为自定义类型

    Args:
        `numbers` (`NumberListA`): 数值集合

    Returns:
        `NumberA`: 数值集合中每个数值的总和
    """
    return sum(numbers)


def sum_b(numbers: NumberListB) -> NumberB:
    """定义一个函数, 参数和返回值为自定义类型

    Args:
        `numbers` (`NumberListB`): 数值集合

    Returns:
        `NumberB`: 数值集合中每个数值的总和
    """
    return sum(numbers)


def test_custom_types() -> None:
    """测试自定义类型"""
    # 测试参数类型为 int 类型
    assert sum_a([1, 2, 3]) == 6
    assert sum_b([1, 2, 3]) == 6

    # 测试参数类型为 float 类型
    assert sum_a([0.1, 0.2, 0.3]) == 0.6
    assert sum_b([0.1, 0.2, 0.3]) == 0.6


# 定义泛型类型, 可以是 int 或 float 类型之一
TA = TypeVar("TA", int, float)


def generic_func_a(val: TA) -> List[TA]:
    """
    定义一个函数, 参数和返回值为泛型类型

    Args:
        val (TA): 泛型参数

    Returns:
        List[TA]: 泛型返回值, 类型和参数类型一致
    """
    # 如果返回值列表元素类型和参数类型不一致, 则 mypy 检查会报错
    return [val] * 3


def generic_func_b[TB: (int, float)](val: TB) -> List[TB]:
    """
    定义一个函数, 参数和返回值为泛型类型,

    Args:
        val (TB): 泛型参数

    Returns:
        List[TB]: 泛型返回值, 类型和参数类型一致
    """
    # 如果返回值列表元素类型和参数类型不一致, 则 mypy 检查会报错
    return [val] * 3


def test_generic_method() -> None:
    """
    测试泛型函数
    """
    # 参数类型和返回值列表元素类型为 int 类型
    assert generic_func_a(3) == [3, 3, 3]
    assert generic_func_b(3) == [3, 3, 3]

    # 参数类型和返回值列表元素类型为 float 类型
    assert generic_func_a(0.1) == [0.1, 0.1, 0.1]
    assert generic_func_b(0.1) == [0.1, 0.1, 0.1]

    # 参数类型和返回值列表元素类型为 str 类型, 此时 mypy 会报错
    assert generic_func_a("A") == ["A", "A", "A"]
    assert generic_func_b("A") == ["A", "A", "A"]


# 通过 `TypeVar` 定义泛型类型
KA = TypeVar("KA", int, str)  # 定义泛型类型 KA, 可以为 `int` 或 `str`
VA = TypeVar("VA", int, float, str)  # 泛型类型 VA, 可以为 `int`, `float`, `str`


class RecordA(Generic[KA, VA]):
    """定义泛型类, 具备两个泛型参数

    一个类通过继承 `Generic` 类, 即可以定义为泛型类, 泛型参数通过 `TypeVar` 定义,
    并设置到 `Generic` 的泛型参数列表中
    """

    def __init__(self) -> None:
        """初始化对象"""
        self._dict: Dict[KA, VA] = {}

    def put(self, key: KA, value: VA) -> None:
        """添加一个键值对

        Args:
            `key` (`KA`): 键
            `value` (`VA`): 值
        """
        self._dict[key] = value

    def get(self, key: KA, default: Optional[VA] = None) -> Optional[VA]:
        """根据一个键获取对应的值

        Args:
            `key` (`KA`): 键
            `default` (`Optional[VA]`): 键不存在时返回的值, 默认为 `None`

        Returns:
            `VA`: 键 `key` 对应的值
        """
        return self._dict.get(key, default)


class RecordB[KB: (int, str), VB: (int, float, str)]:
    """定义泛型类, 具备两个泛型参数

    在 Python 3.12 版本以后, 可以在类名后通过 `[]` 的形式直接定义泛型参数,
    无需额外再继承 `Generic` 类
    """

    def __init__(self) -> None:
        """初始化对象"""
        self._dict: dict[KB, VB] = {}

    def put(self, key: KB, value: VB) -> None:
        """添加一个键值对

        Args:
            `key` (`KB`): 键
            `value` (`VB`): 值
        """
        self._dict[key] = value

    def get(self, key: KB, default: VB | None = None) -> VB | None:
        """根据一个键获取对应的值

        Args:
            `key` (`KB`): 键
            `default` (`VB` | `None`, optional): 键不存在时返回的值, 默认为 `None`

        Returns:
            VB | None: 键 `key` 对应的值
        """
        return self._dict.get(key, default)


def test_generic_class() -> None:
    """测试泛型类"""
    record_a = RecordA[str, int]()
    record_a.put("a", 1)
    assert record_a.get("a") == 1

    record_b = RecordB[str, int]()
    record_b.put("a", 1)
    assert record_b.get("a") == 1
