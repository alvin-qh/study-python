import time
from dataclasses import dataclass, field, is_dataclass
from datetime import datetime, timezone

import pytest


@dataclass
class User:
    """定义一个数据类型

    数据类型是普通类型的快捷封装, 默认重写了类型的 `__init__`, `__eq__` 和 `__repr__` 方法, 使其更适合数据类型的定义

    该类型等价于如下类定义:

    ```python
    class User:
        def __init__(self, id: str, name: str, age: int, gender: str):
            self.id = id
            self.name = name
            self.age = age
            self.gender = gender

        def __repr__(self) -> str:
            return f"User(id='{self.id}', name='{self.name}', age={self.age}, gender='{self.gender}')"

        def __eq__(self, other) -> bool:
            if not isinstance(other, User):
                return False

            return (self.id == other.id and
                    self.name == other.name and
                    self.age == other.age and
                    self.gender == other.gender)
    ```
    """

    # 通过字段定义即可告诉 `@dataclass` 所需定义及初始化的字段
    id: str
    name: str
    age: int
    gender: str


def test_dataclass_attributes() -> None:
    """测试 dataclass 类型对象的属性"""
    # 创建一个 dataclass 类型对象
    u = User("100", "Tom", 18, "Male")

    # 确认字段值正确
    assert u.id == "100"
    assert u.name == "Tom"
    assert u.age == 18
    assert u.gender == "Male"

    # 确认字段的属性可以被修改
    u.id = "200"
    u.name = "Jerry"
    assert u.id == "200"
    assert u.name == "Jerry"


def test_dataclass_methods() -> None:
    """测试 dataclass 类型的方法"""
    # 实例化两个字段值相同的 dataclass 类型对象
    u = User("100", "Tom", 18, "Male")

    # 判断对象类型是否为 dataclass
    assert is_dataclass(u)

    # 确认 __eq__ 方法生效
    ou = User("100", "Tom", 18, "Male")
    assert (u is not ou) and (u == ou)

    # 确认 __repr__ 方法生效
    assert f"{u}" == "User(id='100', name='Tom', age=18, gender='Male')"


@dataclass(
    init=True,  # 自动生成 __init__ 方法
    frozen=True,  # 令属性均为只读属性
    repr=True,  # 自动生成 __repr__ 方法
    eq=True,  # 自动生成 __eq__ 方法
    order=True,  # 自动生成 __lt__, __gt__, __le__, __ge__ 方法
    unsafe_hash=True,  # 自动生成 __hash__ 方法
    slots=False,  # 是否使用 __slots__ 方法优化内存
    weakref_slot=False,  # 是否允许弱引用
)
class Value:
    """定义一个 dataclass 类型, 并指定自动生成的成员方法

    可以通过 `@dataclass` 装饰器的参数来指定要生成类的成员方法, 包括:

    - `init`: 自动生成 __init__ 方法
    - `frozen`: 令属性均为只读属性
    - `repr`: 自动生成 __repr__ 方法
    - `eq`: 自动生成 __eq__ 方法
    - `order`: 自动生成 __lt__, __gt__, __le__, __ge__ 方法
    - `unsafe_hash`: 自动生成 __hash__ 方法
    - `slots`: 是否使用 __slots__ 方法优化内存
    - `weakref_slot`: 是否允许弱引用
    """

    value: int | float


def test_dataclass_options() -> None:
    """测试 dataclass 类型的选项

    具体测试内容参见 `Value` 类型的定义以及 `Value` 类型的 `@dataclass` 装饰器的参数
    """
    # 创建一个 dataclass 类型对象, 确认 __init__ 方法生效
    v = Value(100)

    # 确认对象为 dataclass 类型
    assert is_dataclass(v)

    # 确认字段的属性值可读
    assert v.value == 100

    # 确认字段的属性不可写
    with pytest.raises(AttributeError):
        v.value = 200  # type: ignore[misc]

    # 确认 __repr__ 方法生效
    assert f"{v}" == "Value(value=100)"

    # 确认 __eq__ 方法生效
    assert v == Value(100)
    assert v != Value(200)

    # 确认 __lt__, __gt__, __le__, __ge__ 方法生效
    assert v < Value(200)
    assert Value(200) > v
    assert v <= Value(100)
    assert Value(100) >= v

    # 确认 __hash__ 方法生效
    assert hash(v) == 2279747396317938166


@dataclass(
    repr=True,
    order=True,
    unsafe_hash=True,
)
class Staff:
    """通过 field 函数定义字段属性默认值

    `field` 函数可以为 dataclass 类型定义复杂字段, 包括:

    - `default`: 字段默认值
    - `default_factory`: 字段默认工厂函数
    - `init`: 是否在 __init__ 方法中初始化字段
    - `repr`: 是否在 __repr__ 方法中显示字段
    - `hash`: 是否在 __hash__ 方法中计算字段
    - `compare`: 是否在 __eq__, __lt__, __gt__, __le__, __ge__ 方法中比较字段
    - `metadata`: 字段属性的元数据

    本例中为类型 `name`, `created_at` 和 `sn` 三个字段属性的默认值以及字段相关属性, 并通过 `__post_init__` 方法为字段 `sn` 赋值
    """

    # 通过 field 定义字段属性默认值, 并指定字段属性的选项
    name: str = field(
        default="Anonymous",
        init=True,
        repr=True,
        hash=False,
        compare=True,
        metadata={"label": "姓名"},
    )

    # 通过 field 默认工厂函数定义字段属性默认值, 并指定字段属性的选项
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
        init=True,
        repr=False,
        hash=False,
        compare=True,
        metadata={"label": "创建时间"},
    )

    # 通过 field 默认工厂函数定义字段属性默认值, 并指定字段属性的选项
    sn: str = field(
        default="",
        init=True,
        repr=True,
        hash=True,
        compare=False,
        metadata={"label": "编号"},
    )

    def __post_init__(self) -> None:
        self.sn = f"SN-{self.created_at:%Y%m%d%H%M%S%f}"


def test_dataclass_fields() -> None:
    """测试 dataclass 类型的静态方法"""
    # 创建一个 Staff 类对象
    s1 = Staff()

    # 间隔 100 毫秒后, 再次创建一个 Staff 类对象, 按类型定义, 两个对象的 name 属性值相同, sn 和 created_at 属性不同
    time.sleep(0.01)
    s2 = Staff()

    # 确认两个对象的 name 属性值相同
    assert s1.name == s2.name == "Anonymous"

    # 确认两个对象的 sn 属性和 created_at 属性值不同
    assert s1.sn != s2.sn
    assert s1.created_at != s2.created_at

    # 确认两个对象的 sn 属性值和 created_at 属性值的关系
    # 该关系在 Staff 类的 __post_init__ 方法中定义
    assert s1.sn == f"SN-{s1.created_at:%Y%m%d%H%M%S%f}"
    assert s2.sn == f"SN-{s2.created_at:%Y%m%d%H%M%S%f}"

    # 确认两个对象的比价关系, 两个对象的比较涉及 name 和 created_at 属性
    assert s1 < s2

    # 改变 sn 属性值, 不改变两个对象的比较关系
    s1.sn = "ZN-20230101000000000"
    assert s1 < s2

    # 改变 created_at 属性值, 改变两个对象的比较关系
    s1.created_at = datetime.now(timezone.utc)
    assert s1 > s2

    # 改变 name 属性值, 改变两个对象的比较关系
    s2.name = "Bnonymous"
    assert s1 < s2

    # 确认两个对象的 __repr__ 方法返回的字符串结果
    assert str(s1) == f"Staff(name='{s1.name}', sn='{s1.sn}')"
    assert str(s2) == f"Staff(name='{s2.name}', sn='{s2.sn}')"

    # 确认两个对象的 __hash__ 方法返回的 hash 值, 对象的 hash 值仅依赖 sn 属性值
    # 计算对象原始 hash 值
    hv = hash(s1)

    # 改变对象 name 属性值, 不影响对象的 hash 值
    s1.name = "Tom"
    assert hash(s1) == hv

    # 改变对象 created_at 属性值, 不影响对象的 hash 值
    s1.created_at = datetime.now(timezone.utc)
    assert hash(s1) == hv

    # 改变对象 sn 属性值, 改变对象的 hash 值
    s1.sn = "SN-20230101000000000"
    assert hash(s1) != hv
