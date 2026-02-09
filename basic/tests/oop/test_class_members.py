import time
from functools import cached_property
from typing import Any, cast, overload

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


def test_cacheable_property_decorator() -> None:
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


def test_method_overload() -> None:
    """定义类成员方法重载

    Python 没有真正的类方法重载概念, 也就是不能在一个类内定义多个同名方法,
    所以 Python 中仍是采用不定参数结合逻辑判断对不同输入参数在方法内部进行不同处理

    Python 提供了 `@overload` 注解, 可以标识一个类方法为方法重载, 其使用形式如下:

    - 先在类中定义一个可传递多种类型参数的方法, 并完成该方法的函数体, 作为实际被调用的方法
    - 基于上面定义的方法, 通过 `@overload` 装饰器, 为该方法定义不同的方法签名 (即函数体为 `pass` 或 `...`)
    - 在调用时该方法时, 参数列表可匹配任一标记了 `@overload` 装饰器的方法签名

    注意:

    - 如果要使用 `@overload` 装饰器, 则必须要在类中定义一个可以满足所有参数传递的方法, 并在类中为该方法至少配置两个标记了 `@overload`
    装饰器的方法签名;
    - 在类中, 标记 `@overload` 装饰器的方法签名, 必须要声明在实际方法之前;

    注意: `@overload` 注解只能用于方法定义, 不能用于方法实现, 也就是说, 被 `@overload`
    装饰器标记的方法并不能真正执行, 只是代表一个方法签名的表示, 告诉调用方该方法调用时可以传递的参数和返回值
    """

    class DemoClass:
        """定义测试类

        在类中定义名为 `add` 的方法的实际执行体, 并为其声明若干重载签名
        """

        # 定义保存结果的属性字段
        _result: int | float | str | list[Any]

        # 为 `__init__` 方法定义具备两个数值类型参数的重载, 该方法返回一个数值类型值
        @overload
        def __init__(self, a: int | float, b: int | float) -> None: ...

        # 为 `__init__` 方法定义具备一个字符串类型参数和一个任意类型参数的重载, 该方法返回一个字符串类型值
        @overload
        def __init__(self, a: str, b: Any) -> None: ...

        # 为 `__init__` 方法定义具备一个列表类型参数和一个任意类型参数的重载, 该方法返回一个列表类型值
        @overload
        def __init__[T: Any](self, a: list[T], b: T) -> None: ...

        # 为 `__init__` 方法定义具备两个列表类型参数的重载, 该方法返回一个列表类型值
        @overload
        def __init__[T: Any](self, a: list[T], b: list[T]) -> None: ...

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """为 `__init__` 方法进行实际方法定义

            该方法定义必须满足上述所有同名方法的重载方法签名定义
            """
            # 匹配方法参数列表, 获取参数 a 和 b 的值

            # 尝试从 args 参数中获取参数 a 和 b 的值
            match args:
                case x if len(x) >= 2:
                    a, b = args
                case x if len(x) == 1:
                    a = args[0]

            # 尝试从 kwargs 参数中获取参数 a 和 b 的值
            if "a" in kwargs:
                a = kwargs["a"]

            if "b" in kwargs:
                b = kwargs["b"]

            # 确认参数 a 和 b 必须存在
            if "a" not in locals() or "b" not in locals():
                raise ValueError("arguments a and b must be specified")

            # 根据参数类型不同, 对参数 a 和 b 进行计算
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                self._result = a + b
            elif isinstance(a, str):
                self._result = f"{a}{b}"
            elif isinstance(a, list):
                if isinstance(b, list):
                    self._result = a + b
                else:
                    self._result = [*a, b]
            else:
                raise ValueError("invalid arguments type")

        def __int__(self) -> int:
            """将当前对象转为 `int` 类型值"""
            return cast(int, self._result)

        def __float__(self) -> float:
            """将当前对象转为 `float` 类型值"""
            return cast(float, self._result)

        def __str__(self) -> str:
            """将当前对象转为 `str` 类型值"""
            return cast(str, self._result)

        def __iter__(self) -> Any:
            """将当前对象转为迭代器"""
            if isinstance(self._result, list):
                return iter(self._result)

            return iter([self._result])

    # 测试按照不同的方法重载形式调用类的 __init__ 方法

    c = DemoClass(10, b=20)
    assert int(c) == 30

    c = DemoClass(0.1, 0.2)
    assert abs(float(c) - 0.3) < 0.00001

    c = DemoClass("Hello", 123)
    assert str(c) == "Hello123"

    c = DemoClass([1, 2, 3], 4)
    assert list(c) == [1, 2, 3, 4]

    c = DemoClass([1, 2, 3, 4], [5, 6])
    assert list(c) == [1, 2, 3, 4, 5, 6]
