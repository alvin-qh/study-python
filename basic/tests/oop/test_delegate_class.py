from typing import Any, cast

from basic.oop.delegate import Delegate


def test_create_class_dynamically() -> None:
    """测试动态创建类型

    通过 `type` 函数可以动态创建一个类型, 创建的类型和通过 `class` 关键字定义的类型一致

    `type` 函数的参数如下：

    - 参数 1 为类型名称
    - 参数 2 为类型的父类集合
    - 参数 3 为类型的属性和方法
    """

    def _demo_class_init_method(self: Any, value: int) -> None:
        """定义 `DemoClass` 的构造方法

        Args:
            `self` (`Any`): 该函数所绑定类型的实例对象
            `value` (`int`): 属性值
        """
        setattr(self, "_value", value)

    def _demo_class_get_value_property(self: Any) -> int:
        """定义 `DemoClass` 的 `value` 属性的 getter 方法

        Args:
            `self` (`Any`): 该函数所绑定类型的实例对象

        Returns:
            `int`: 属性值
        """
        return cast(int, getattr(self, "_value"))

    def _demo_class_set_value_property(self: Any, value: int) -> None:
        """类型 `ADemoClass` 的 `value` 属性的 setter 方法

        Args:
            `self` (`Any`): 该函数所绑定类型的实例对象
            `value` (`int`): 属性值
        """
        setattr(self, "_value", value)

    # 定义 DemoClass 类型
    DemoClass = type(
        "DemoClass",  # 类型名称
        (object,),  # 类型的父类
        {
            # 指定类型的构造方法
            "__init__": _demo_class_init_method,
            # 指定类型的 value 属性, 包括 getter 和 setter 方法
            "value": property(
                fget=_demo_class_get_value_property,
                fset=_demo_class_set_value_property,
            ),
            # 定义类型的类方法
            "who_am_i": classmethod(lambda cls: cls),
            # 定义类型的静态方法
            "say_hello": staticmethod(lambda: "Hello World!"),
            # 定义类型的 work 方法
            "work": lambda self, x: getattr(self, "_value") + x,
        },
    )

    # 测试动态创建类的类方法
    assert DemoClass.who_am_i() is DemoClass  # type: ignore[attr-defined]
    assert DemoClass.say_hello() == "Hello World!"  # type: ignore[attr-defined]

    # 通过类型d创建对象
    c = DemoClass(100)  # pyright: ignore[reportCallIssue]
    assert isinstance(c, DemoClass)
    assert c.value == 100  # type: ignore[attr-defined]

    c.value = 10  # type: ignore[attr-defined]
    assert c.value == 10  # type: ignore[attr-defined]
    assert c.work(1) == 11  # type: ignore[attr-defined]


def test_delegate_class() -> None:
    """测试代理类型"""

    class Class1:
        """定义被代理类型"""

        def run[T: (int, float)](self, a: T, b: T) -> T:
            return a + b

    class Class2:
        """接口实现定义被代理类型类"""

        def run[T: (int, float)](self, a: T, b: T) -> T:
            return a * b

    # 实例化被代理对象
    c1, c2 = Class1(), Class2()

    # 确认被代理对象执行方法的返回值
    assert c1.run(1, 2) == 3
    assert c2.run(1, 2) == 2

    # 创建代理对象
    c1_d = Delegate(c1)
    c2_d = Delegate(c2)

    # 验证代理对象执行被代理方法的返回值
    assert c1_d.run(1, 2) == "Result is: 3"
    assert c2_d.run(1, 2) == "Result is: 2"

    # 验证代理对象可以访问被代理对象的实例
    assert c1_d.instance is c1
    assert c2_d.instance is c2
