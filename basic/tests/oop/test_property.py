import time
from functools import cached_property
from typing import Any

import pytest


def test_property_function() -> None:
    """通过 `property` 函数可以给类型增加属性

    属性可具备 `fget`, `fset` 和 `fdel` 三类行为:

    - `fget` 指向一个无参 (除 `self` 外) 但有返回值的类方法, 表示如何获取类属性
    - `fset` 指向一个单一参数 (除 `self` 外), 无返回值的类方法, 表示如何设置类属性
    - `fdel` 指向一个无参 (除 `self` 外) 且无返回值的方法, 表示如何删除类属性
    """

    class DemoClass:
        """演示 `property` 函数使用的类"""

        def __init__(self, val: Any) -> None:
            """初始化对象, 传入任意参数表示对象属性

            Args:
                `val` (`Any`): 对象属性值
            """
            self._val = val

        def _get(self) -> Any:
            """获取属性值

            Returns:
                `Any`: 属性值
            """
            return self._val

        def _set(self, val: Any) -> None:
            """设置属性值

            Args:
                `val` (`Any`): 属性值
            """
            self._val = val

        def _del(self) -> None:
            """删除属性"""
            del self._val

        # 定义名为 value 的属性, 将所需方法进行对应
        value = property(
            fget=_get,
            fset=_set,
            fdel=_del,
            doc="get/set/delete value property",
        )

    # 实例化一个对象并赋予属性值
    c = DemoClass("Hello")

    # 获取属性值
    assert c.value == "Hello"

    # 设置属性值
    c.value = 100
    assert c.value == 100

    # 删除属性值
    del c.value
    with pytest.raises(AttributeError):
        c.value


def test_property_decorator() -> None:
    """通过 `property` 装饰器, 也可以实现对象属性

    - 装饰为 `@property` 的方法用于获取属性值
    - 装饰为 `@属性名.setter` 的方法用于设置属性值
    - 装饰为 `@属性名.deleter` 的方法用于删除属性

    同一个属性相关的方法名称必须相同
    """

    class DemoClass:
        """演示 `@property` 装饰器使用的类"""

        def __init__(self, val: Any) -> None:
            """初始化对象, 传入任意参数表示对象属性

            Args:
                `val` (`Any`): 对象属性值
            """
            self._val = val

        @property
        def value(self) -> Any:
            """表示获取 `value` 属性值的方法

            Returns:
                `Any`: 属性值
            """
            return self._val

        @value.setter
        def value(self, val: Any) -> None:
            """当 `value` 标识为 `@property` 后, `@value.setter` 表示设置属性值的方法

            Args:
                `val` (`Any`): 属性值
            """
            self._val = val

        @value.deleter
        def value(self) -> None:
            """当 `value` 标识为 `@property` 后, `@value.deleter` 表示设置属的方法"""
            del self._val

    # 实例化一个对象并赋予属性值
    c = DemoClass("Hello")

    # 获取属性值
    assert c.value == "Hello"

    # 设置属性值
    c.value = 100
    assert c.value == 100

    # 删除属性值
    del c.value
    with pytest.raises(AttributeError):
        c.value


def test_property_cache() -> None:
    """通过 `property` 装饰器, 也可以实现对象属性

    - 装饰为 `@property` 的方法用于获取属性值
    - 装饰为 `@属性名.setter` 的方法用于设置属性值
    - 装饰为 `@属性名.deleter` 的方法用于删除属性

    同一个属性相关的方法名称必须相同
    """

    class DemoClass:
        """演示 `@property` 装饰器使用的类"""

        def __init__(self, n: int) -> None:
            """初始化对象, 传入任意参数表示对象属性

            Args:
                `n` (`int`): 对象属性值
            """
            self._n = n

        @staticmethod
        def _fib(n: int) -> int:
            """计算斐波那契数列

            Args:
                `n` (`int`): 斐波那契数列的索引

            Returns:
                `int`: 斐波那契数列的值
            """
            if n <= 0:
                return 0
            elif n == 1:
                return 1
            else:
                return DemoClass._fib(n - 1) + DemoClass._fib(n - 2)

        @cached_property
        def value(self) -> int:
            """表示获取 `value` 属性值的方法

            Returns:
                `Any`: 属性值
            """
            return self._fib(self._n)

    # 实例化一个对象并赋予属性值
    c = DemoClass(30)

    start = time.perf_counter()

    # 第一次获取属性值
    assert c.value == 832040
    assert time.perf_counter() - start > 0.1

    start = time.perf_counter()

    # 再次获取属性值, 属性值应该被缓存, 不会重新计算
    assert c.value == 832040
    assert time.perf_counter() - start < 0.1
