from dataclasses import dataclass, field, is_dataclass
from datetime import datetime
from typing import Self

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

-
@dataclass
class Staff:
    name: str = field(default="NoName")
    sn: str = field(default_factory=Self._sn_factory)

    @staticmethod
    def _sn_factory() -> str:
        return f"SN-{datetime.now():%Y%m%d%H%M%S%f}"
