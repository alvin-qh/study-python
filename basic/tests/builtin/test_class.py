import json
from abc import ABC, abstractmethod
from functools import partialmethod
from typing import Any, Self, cast

from pytest import raises

from basic.builtin import Automate, Delegate

_dir = dir()






def test_dynamic_class() -> None:
    """测试动态类型

    通过 `__setattr__`, `__getattr__` 和 `__delattr__` 三个魔法方法用于获取, 设置和删除那些"未定义"的属性
    """

    class C:
        """动态类型, 可以设置和获取任意名称的属性"""

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
            """根据属性名称获取属性值

            Args:
                `name` (`str`): 属性名

            Returns:
                `Any`: 属性值
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

    # 实例化对象
    c = C()

    # 设置 x 属性
    c.x = 100

    # 确认 x 属性的属性值
    assert c.x == 100

    # 设置 y 属性
    c.y = "Hello"

    # 确认 y 属性的属性值
    assert c.y == "Hello"

    # 删除指定的属性
    del c.y
    with raises(AttributeError):
        # 确保属性已被删除
        c.y


def test_delegate_class() -> None:
    """测试代理类型"""

    class B(ABC):
        """接口类型"""

        @abstractmethod
        def run[T: (int, float)](self, a: T, b: T) -> T:
            """接口方法

            Args:
                `a` (`T`): 参数 1
                `b` (`T`): 参数 2

            Returns:
                `T`: 返回值
            """

    class C1(B):
        """接口实现类"""

        def run[T: (int, float)](self, a: T, b: T) -> T:
            """实现接口方法

            Args:
                `a` (`T`): 参数 1
                `b` (`T`): 参数 2

            Returns:
                `T`: 两个参数相加的结果
            """
            return a + b

    class C2(B):
        """接口实现类"""

        def run[T: (int, float)](self, a: T, b: T) -> T:
            """实现接口方法

            Args:
                `a` (`T`): 参数 1
                `b` (`T`): 参数 2

            Returns:
                `T`: 两个参数相乘的结果
            """
            return a * b

    # 实例化对象
    c1, c2 = C1(), C2()

    # 创建代理对象
    c1_d = Delegate(c1)
    c2_d = Delegate(c2)

    # 验证代理对象执行被代理方法的返回值
    assert c1_d.run(1, 2) == "Result is: 3"
    assert c2_d.run(1, 2) == "Result is: 2"


def test_create_dynamic_class() -> None:
    """测试创建动态类型

    通过 `type` 函数可以用于动态创建一个类型

    - 参数 1 为类型名称
    - 参数 2 为类型的父类集合
    - 参数 3 为类型的属性和方法
    """

    def A__init__(self: Any, value: int) -> None:
        """类型 `A` 的构造方法

        Args:
            `value` (`int`): 属性值
        """
        self.value = value

    # 定义类型
    A = type(
        "A",  # 类型名称
        (object,),  # 类型的父类
        {
            "__init__": A__init__,  # 类型的构造方法
            "value": 0,  # 类型的属性
            "work": lambda self, x: self.value + x,  # 类型的方法
        },
    )

    # 通过类型
    a = A(100)
    assert isinstance(a, A)
    assert a.value == 100  # type: ignore[attr-defined]

    a.value = 10  # type: ignore[attr-defined]
    assert a.value == 10  # type: ignore[attr-defined]
    assert a.work(1) == 11  # type: ignore[attr-defined]


def test_singleton_class() -> None:
    """测试单例类型

    Python 可以通过 `__new__` 魔法方法完成单例, 即让一个类型只能实例化一个对象
    """

    class C:
        """单例类型"""

        # 保持单例的类字段
        _inst: Self | None = None

        def __new__(cls: type[Self], *args: Any, **kwargs: Any) -> "C":
            """创建实例

            为了保证创建实例时单例, 无论执行多少次创建实例方法, 均返回 `_inst` 字段引用的对象

            Args:
                `cls` (`type[Self]`): 当前类型

            Returns:
                `C`: 当前类型的单例实例
            """
            if not cls._inst:
                # 如果单例未被创建, 则创建单例实例, 并引用到 _inst 字段上
                cls._inst = super().__new__(cls)

            # 返回单例实例
            return cast(C, cls._inst)

        def __init__(self, value: Any) -> None:
            """初始化对象, 设置对象的属性

            Args:
                `value` (`Any`): 属性值
            """
            self.value = value

    # 第一次创建单例实例
    c1 = C(100)
    assert c1.value == 100

    # 再次创建单例实例
    c2 = C(200)

    # 确认两次创建的单例实例是同一个对象
    assert id(c1) == id(c2)

    # 确认第二次创建对象设置的属性值覆盖了第一次创建对象的属性值
    assert c2.value == c1.value == 200


def test_currying_method() -> None:
    """测试类方法的 "柯里化"

    `partialmethod` 可以为类型增加一个方法, 该方法是将类中的另一个方法进行转换得到
    """

    class C:
        """
        测试类方法的 "柯里化" 操作
        """

        def __init__(self, value: int) -> None:
            """初始化对象, 设置对象属性

            Args:
                `value` (`int`): 属性值
            """
            self.value = value

        def set_value(self, value: int) -> None:
            """设置属性值

            Args:
                `value` (`int`): 属性值
            """
            self.value = value

        # 柯里化 set_value 方法, 方法的参数为 0 (命名传参方式)
        zero = partialmethod(set_value, value=0)

        # 柯里化 set_value 方法, 方法的参数为 1e10 (位置传参方式)
        max = partialmethod(set_value, 1e10)

    c = C(10)
    assert c.value == 10

    # 调用柯里化的方法, 将属性值设置为 0
    c.zero()
    assert c.value == 0

    # 调用柯里化的方法, 将属性值设置为 1e10
    c.max()
    assert c.value == 1e10
