import json

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

    通过 `__getattr__` 魔法方法, 可以覆盖属性访问行为.
    """

    class DemoClass:
        def __getattr__(self, name: str) -> str:
            """可以通过 `__getattr__` 魔法方法指定属性访问行为

            Args:
                name (str): 属性名

            Returns:
                str: 属性值
            """
