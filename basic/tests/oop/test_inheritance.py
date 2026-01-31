from abc import ABC, abstractmethod
from typing import override


def test_class_inheritance() -> None:
    """测试子类集成父类

    Python 支持完整的面向对象编程, 故也支持类之间的集成关系

    和其它面向对象语音语言一样, Python 的子类可以继承父类的属性和方法, 并且覆盖父类的方法

    另外, Python 作为动态类型语言, 几乎所有绑定关系都是运行时动态绑定的, 故其多态性也更为容易表达
    """

    class Base:
        def __init__(self) -> None:
            self._name = "Base"

        def who_am_i(self) -> str:
            return self._name

        def base_special(self) -> str:
            return "I'm Base"

    class Child(Base):
        def __init__(self) -> None:
            super().__init__()
            self._name = "Child"

        @override
        def who_am_i(self) -> str:
            return self._name

        def child_special(self) -> str:
            return "I'm Child"

    base = Base()
    assert base.who_am_i() == "Base"
    assert base.base_special() == "I'm Base"

    child = Child()
    assert child.who_am_i() == "Child"
    assert child.base_special() == "I'm Base"
    assert child.child_special() == "I'm Child"

    base = child
    assert base.who_am_i() == "Child"
    assert base.base_special() == "I'm Base"


def test_multi_inheritance() -> None:
    """测试 Python 的多重继承

    Python 支持多重继承, 子类会继承所有父类中定义的属性和方法,

    一般情况下, 继承的顺序为: 最左亲近原则, 即父类在继承列表中越靠左, 越和子类亲近
    """

    class Interface_1(ABC):
        """定义接口类

        该接口具备抽象方法 `f1`
        """

        @abstractmethod
        def f1(self) -> str:
            pass

    class Interface_2(ABC):
        """定义接口类

        该接口具备抽象方法 `f2`
        """

        @abstractmethod
        def f2(self) -> str:
            pass

    class Base_1:
        """定义类

        该类具备普通方法 `f1`
        """

        def f1(self) -> str:
            return "Base_1::f1"

    class Base_2:
        """定义类

        该类具备普通方法 `f1` 和 `f2`
        """

        def f1(self) -> str:
            return "Base_2::f1"

        def f2(self) -> str:
            return "Base_2::f2"

    class Child(Base_1, Base_2, Interface_1, Interface_2):
        """演示多重继承

        在继承列表中, 按从右到左的顺序继承, 故子类会按顺序继承 `Interface_2`, `Interface_1`, `Base_2`, `Base_1 中定义的属性和方法,
        对于同名的属性和方法, 则后继承的会覆盖先继承的

        故 `Base_2` 中定义的 `f1` 方法会被 `Base_1` 中定义的 `f1` 方法覆盖, 因为 `Class_1` 是按顺序最后一个被继承的类

        另外, 虽然 `Child` 类没有实现任何接口方法, 但其继承了 `Class_1` 和 `Class_2` 中的 `f1` 和 `f2` 方法,
        且继承顺序在 `Interface_1` 和 `Interface_2` 之后, 相当于 `Child` 类间接实现了 `Interface_1` 和 `Interface_2` 接口方法
        """

    # 确认 Child 类同时是 Interface_1, Interface_2, Base_1, Base_2 类的子类
    assert issubclass(Child, (Interface_1, Interface_2, Base_1, Base_2))

    # 实例化 C 类对象
    c = Child()

    # 确认 c 对象同时是 Interface_1, Interface_2, Base_1, Base_2 类的实例对象
    assert isinstance(c, (Interface_1, Interface_2, Base_1, Base_2))

    # 确认 c 对象继承的方法以 Base_1 类型优先
    assert c.f1() == "Base_1::f1"
    assert c.f2() == "Base_2::f2"
