from typing import Any

import pytest


def _upper_attrs(attrs: dict[str, Any]) -> dict[str, Any]:
    """将属性名转为大写字母

    Args:
        `attrs` (`dict[str, Any]`): 属性字典

    Returns:
        `dict[str, Any]`: 属性名转为大写字母后的属性字典
    """
    return {key.upper(): value for key, value in attrs.items() if not key.startswith("__")}


def test_metaclass_by_function() -> None:
    """测试 `metaclass` 参数

    类型的 `metaclass` 参数用于指定一个函数, 该返回一个 `Type` 类型, 作为类的元类型
    """

    def metaclass(
        class_name: str,
        parents: tuple[Any],
        attrs: dict[str, Any],
    ) -> type[Any]:
        """元类型函数, 返回一个类型对象, 用于设置目标类型的名称, 父类以及属性值

        Args:
            `class_name` (`str`): 目标类型的类名称
            `parents` (`tuple[Any]`): 目标类型的父类集合
            `attrs` (`dict[str, Any]`): 目标类型的属性集合

        Returns:
            `Any`: 目标类型的元类型对象
        """
        # 动态产生一个类型, 作为目标类型的元类型对象
        return type(
            class_name + "_New",  # 修改目标类型的类名称
            parents,
            _upper_attrs(attrs),  # 处理目标类型的属性集合, 将属性名修改为大写
        )

    class DemoClass(metaclass=metaclass):  # type: ignore
        """定义类型, 并指定元类型为 `metaclass` 函数

        此时, `DemoClass` 类的类型定义由 `metaclass` 函数的返回值来定义
        """

        @property
        def value(self) -> int:
            """定义一个属性, 用于测试元类型将属性名修改为大写"""
            return 100

    # 创建对象
    c = DemoClass()

    # 验证类名是否被修改
    assert type(c).__name__ == "DemoClass_New"

    # 验证属性名是否为大写
    assert c.VALUE == 100  # type: ignore

    # 验证原本的小写属性名是否已经失效
    with pytest.raises(AttributeError):
        assert c.value


def test_metaclass_by_class() -> None:
    """测试通过类型来定义目标类的元类型

    目标类的 `metaclass` 既可以为函数, 也可以为一个类, 如果是一个类的话,
    必须通过 `__new__` 方法给目标类型返回类型定义
    """

    class MetaClass(type):
        """元类型, 用于创建一个描述类型的对象"""

        def __new__(
            cls,
            class_name: str,
            parents: tuple[Any],
            attrs: dict[str, Any],
        ) -> type[Any]:
            """创建实例, 根据传入的类型元数据, 返回用元数据创建的类型对象

            注意, 这个方法不能标识 `@classmethod` 装饰器, 因为 `cls` 参数是外部显式传递的.
            如果标识了 `@classmethod`, 则会重复传递 `cls` 参数

            Args:
                `class_name` (`str`): 目标类型的类名称
                `parents` (`tuple[Type]`): 目标类型的父类集合
                `attrs` (`dict[str, Any]`): 目标类型的属性集合

            Returns:
                `type[Any]`: 目标类型的元类型对象
            """
            return type(
                class_name + "_New",  # 修改目标类型的类名称
                parents,
                _upper_attrs(attrs),  # 处理目标类型的属性集合, 将属性名修改为大写
            )

    class DemoClass(metaclass=MetaClass):
        """定义类型, 并指定元类型为 `MetaClass` 类型

        此时, `DemoClass` 类的类型定义由 `MetaClass` 类型产生的对象来定义
        """

        @property
        def value(self) -> int:
            """定义一个属性, 用于测试元类型将属性名修改为大写"""
            return 100

    # 创建对象
    c = DemoClass()

    # 验证类名是否被修改
    assert type(c).__name__ == "DemoClass_New"

    # 验证属性名是否为大写
    assert c.VALUE == 100  # type: ignore

    # 验证原本的小写属性名是否已经失效
    with pytest.raises(AttributeError):
        assert c.value
