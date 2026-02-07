import json
from typing import Any, Self, cast

import pytest

from basic.oop.automate import Automate


def test_slots_magic_member() -> None:
    """`__slots__` 魔法字段用于定义对象具备的属性集合

    Python 作为解释型语音, 可以为对象添加任意属性而无需类型定义, 添加的属性以字典形式在对象内
    部以 `__dict__` 魔法字段存储

    `__slots__` 字段用于声明一个类型规定的字段集合, 设置了 `__slots__` 字段后, 对象能使用的
    属性就会约束在其定义范围内, 且不再通过 `__dict__` 字段存储对象属性
    """

    class NoSlots:
        """定义不包含 `__slots__` 字段的类型"""

        pass

    class WithSlots:
        """定义包含 `__slots__` 字段的类型

        定义了 `__slots__` 字段后, 添加的属性将无法通过 `__dict__` 字段访问, 而只能通过 `__slots__` 字段访问,
        相当于为类型提供了属性约束, 类型能用的属性必须在 `__slots__` 定义的列表中
        """

        # 定义可访问属性列表
        __slots__ = ("name", "age")

    # 实例化对象
    no_slots, with_slots = NoSlots(), WithSlots()

    # 操作对象的未定义属性, 类型检查失败 (可正常运行)
    no_slots.name = "Alvin"  # type: ignore[attr-defined]
    assert no_slots.name == "Alvin"  # type: ignore[attr-defined]

    # 操作对象的未定义属性, 类型检查失败 (可正常运行)
    no_slots.age = 41  # type: ignore[attr-defined]
    assert no_slots.age == 41  # type: ignore[attr-defined]

    # 检查对象属性字典
    assert no_slots.__dict__ == {
        "name": "Alvin",
        "age": 41,
    }

    with_slots.name = "Alvin"  # type: ignore[attr-defined]
    assert with_slots.name == "Alvin"  # type: ignore[attr-defined]

    with_slots.age = 41  # type: ignore[attr-defined]
    assert with_slots.age == 41  # type: ignore[attr-defined]

    # 定义了 __slots__ 字段后, 对象不再具备 __dict__ 字段, 可访问的属性均由 __slots__ 字段定义
    assert not hasattr(with_slots, "__dict__")

    # 如果访问了未定义在 __slots__ 列表中的属性, 则会抛出异常
    with pytest.raises(AttributeError):
        with_slots.gender = "M"  # type: ignore[attr-defined]


def test_slots_magic_member_for_automate_class() -> None:
    """测试自动装配类

    `Automate` 可根据类中定义的 `__slots__` 字段自动装配对象属性值
    """

    class Member(Automate):  # type: ignore[misc,unused-ignore]
        # 定义可用的属性名
        __slots__ = ("id", "name", "price")

    class Group(Automate):  # type: ignore[misc,unused-ignore]
        # 定义可用的属性名
        __slots__ = ("id", "name", "members")

        # 定义特殊属性的类型
        members: list[Member]

    # 实例化自动装配类型的对象
    group = Group(
        1,
        "G-1",
        [
            Member(1, "S-1", 12.5),
            Member(2, "S-2", 22),
        ],
    )

    # 验证对象属性值
    assert group.id == 1
    assert group.name == "G-1"
    assert len(group.members) == 2

    member = group.members[0]
    assert member.id == 1
    assert member.name == "S-1"
    assert member.price == 12.5

    member = group.members[1]
    assert member.id == 2
    assert member.name == "S-2"
    assert member.price == 22

    # 验证对象转为 json
    assert (
        json.dumps(group, indent=2)
        == """{
  "id": 1,
  "name": "G-1",
  "members": [
    {
      "id": 1,
      "name": "S-1",
      "price": 12.5
    },
    {
      "id": 2,
      "name": "S-2",
      "price": 22
    }
  ]
}"""
    )

    # 测试通过 Dict 对象作为入参
    group = Group(
        **{
            "id": 1,
            "name": "G-1",
            "members": [
                {"id": 1, "name": "S-1", "price": 12.5},
                {"id": 2, "name": "S-2", "price": 22},
            ],
        }
    )

    # 验证对象属性值
    assert group.id == 1
    assert group.name == "G-1"
    assert len(group.members) == 2

    member = group.members[0]
    assert member.id == 1
    assert member.name == "S-1"
    assert member.price == 12.5

    member = group.members[1]
    assert member.id == 2
    assert member.name == "S-2"
    assert member.price == 22


def test_dir_magic_member() -> None:
    """覆盖 dir 函数

    通过 `__dir__` 魔法方法, 可以覆盖 dir 函数的默认行为.
    """

    class DemoClass:
        def __dir__(self) -> list[str]:
            """可以通过 `__dir__` 魔法方法指定 dir 函数返回的结果

            Returns:
                list[str]: _description_
            """
            return ["a", "b", "c"]

    c = DemoClass()
    # 验证 dir 函数返回的结果
    assert dir(c) == ["a", "b", "c"]


def test_attribute_magic_member() -> None:
    """属性访问

    对于 Python 对象, 其属性访问实际上是通过如下几个魔术成员方法进行的, 包括:

    - `__getattr__`: 获取属性值
    - `__setattr__`: 设置属性名和属性值
    - `__delattr__`: 删除属性

    本例通过一个动态类来演示对象的属性访问, 通过上述属性访问方法, 利用类中的一个字典来实现为对象设置任意属性并进行访问或删除
    """

    class DemoClass:
        """定义动态类型

        本类型内部定义了一个 `_props` 字典字段, 用于存储对象属性名和属性值, 并通过 `__getattr__`, `__setattr__` 以及
        `__delattr__` 魔术方法来实现属性访问, 设置和删除
        """

        # 存储属性名和属性值的字典对象
        _props: dict[str, Any]

        def __init__(self) -> None:
            """初始化对象

            为当前对象设置存储键值对的 `_props` 字段
            """
            # 注意, _props 字段需要设置在父类上
            # 否则会调用当前对象的 __setattr__ 方法, 而 __setattr__ 方法中又调用了 _props 字段,
            # 会造成循环调用
            super().__setattr__("_props", {})

        def __getattr__(self, name: str) -> Any:
            """可以通过 `__getattr__` 魔法方法指定属性访问行为

            Args:
                name (str): 属性名

            Returns:
                str: 属性值
            """
            try:
                return self._props[name]
            except KeyError:
                raise AttributeError(name)

        def __setattr__(self, name: str, value: Any) -> None:
            """设置属性名和属性值

            Args:
                `name` (`str`): 属性名
                `value` (`Any`): 属性值
            """
            try:
                self._props[name] = value
            except KeyError:
                raise AttributeError(name)

        def __delattr__(self, name: str) -> None:
            """根据属性名删除属性

            Args:
                `name` (`str`): 属性名
            """
            try:
                del self._props[name]
            except KeyError:
                # 确保幂等性
                pass

    # 实例化类对象
    c = DemoClass()

    # 设置对象属性值
    c.name = "Alvin"
    c.age = 45

    # 确认对象属性值设置正确
    assert c.name == "Alvin"
    assert c.age == 45

    # 删除指定的属性
    del c.name

    # 确认属性已被删除
    with pytest.raises(AttributeError):
        # 确保属性已被删除
        c.name


def test_singleton_class() -> None:
    """测试单例类型

    可以通过 `__new__` 魔术方法完成单例, 即让一个类型只能实例化一个对象
    """

    class SingletonClass:
        """单例类型"""

        # 保持单例的类字段
        _inst: Self | None = None

        def __new__(cls: type[Self], *args: Any, **kwargs: Any) -> "SingletonClass":
            """创建实例

            为了保证创建实例时单例, 无论执行多少次创建实例方法, 均返回 `_inst` 字段引用的对象

            Args:
                `cls` (`type[Self]`): 当前类型

            Returns:
                `SingletonClass`: 当前类型的单例实例
            """
            if not cls._inst:
                # 如果单例未被创建, 则创建单例实例, 并引用到 _inst 字段上
                cls._inst = super().__new__(cls)

            # 返回单例实例
            return cast(SingletonClass, cls._inst)

        def __init__(self, value: Any) -> None:
            """初始化对象, 设置对象的属性

            Args:
                `value` (`Any`): 属性值
            """
            self.value = value

    # 第一次创建单例实例
    c1 = SingletonClass(100)
    assert c1.value == 100

    # 再次创建单例实例
    c2 = SingletonClass(200)

    # 确认两次创建的单例实例是同一个对象
    assert id(c1) == id(c2)

    # 确认第二次创建对象设置的属性值覆盖了第一次创建对象的属性值
    assert c2.value == c1.value == 200
