import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar

from pytest import raises

from .automate import Automate
from .delegate import Delegate

_dir = dir()


def test_dir_function_and_method() -> None:
    """
    `dir` 有如下几个作用
    - 在全局位置调用时, 返回一个包含所有全局变量 (包含全局魔法变量) 名称的集合
    - 在局部位置使用时, 返回包含局部变量名称的集合
    """
    # 确认
    assert "List" in _dir
    # 此时
    assert "a" not in dir()

    n = 100  # noqa
    assert "n" in dir()

    class A:
        def __init__(self) -> None:
            self._name = "Alvin"

        def get_name(self) -> str:
            return self._name

        @property
        def name(self) -> str:
            return self._name

    a = A()
    # 验证指定的方法和属性包含在 dir 函数返回的集合中
    assert "__init__" in dir(a)
    assert "get_name" in dir(a)
    assert "name" in dir(a)

    class B:
        def __dir__(self) -> List[str]:
            """
            可以通过 `__dir__` 魔法方法指定 dir 函数返回的结果

            Returns:
                List[str]: _description_
            """
            return ["a", "b", "c"]

    b = B()
    # 验证 dir 函数返回的结果
    assert dir(b) == ["a", "b", "c"]


def test_property_function() -> None:
    """
    通过 `property` 函数可以给类型增加属性

    属性可具备 `fget`, `fset` 和 `fdel` 三类行为
    - `fget` 指向一个无参 (除 `self` 外) 但有返回值的类方法, 表示如何获取类属性
    - `fset` 指向一个单一参数 (除 `self` 外), 无返回值的类方法, 表示如何设置类属性
    - `fdel` 指向一个无参 (除 `self` 外) 且无返回值的方法, 表示如何删除类属性
    """
    class C:
        """
        演示 `property` 函数使用的类
        """

        def __init__(self, val: Any) -> None:
            """
            初始化对象, 传入任意参数表示对象属性

            Args:
                val (Any): 对象属性值
            """
            self._val = val

        def _get(self) -> Any:
            """
            获取属性值

            Returns:
                Any: 属性值
            """
            return self._val

        def _set(self, val: Any) -> None:
            """
            设置属性值

            Args:
                val (Any): 属性值
            """
            self._val = val

        def _del(self) -> None:
            """
            删除属性
            """
            del self._val

        # 定义名为 value 的属性, 将所需方法进行对应
        value = property(
            fget=_get, fset=_set, fdel=_del,
            doc="get/set/delete value property",
        )

    # 实例化一个对象并赋予属性值
    c = C("Hello")

    # 获取属性值
    assert c.value == "Hello"

    # 设置属性值
    c.value = 100
    assert c.value == 100

    # 删除属性值
    del c.value
    with raises(AttributeError):
        c.value


def test_property_decorator() -> None:
    """
    通过 `property` 装饰器, 也可以实现对象属性

    - 装饰为 `@property` 的方法用于获取属性值
    - 装饰为 `@属性名.setter` 的方法用于设置属性值
    - 装饰为 `@属性名.deleter` 的方法用于删除属性

    同一个属性相关的方法名称必须相同
    """
    class C:
        """
        演示 `@property` 装饰器使用的类
        """

        def __init__(self, val: Any) -> None:
            """
            初始化对象, 传入任意参数表示对象属性

            Args:
                val (Any): 对象属性值
            """
            self._val = val

        @property
        def value(self) -> Any:
            """
            表示获取 `value` 属性值的方法

            Returns:
                Any: 属性值
            """
            return self._val

        @value.setter
        def value(self, val: Any) -> None:
            """
            当 `value` 标识为 `@property` 后, `@value.setter` 表示设置属性值的方法

            Args:
                val (Any): 属性值
            """
            self._val = val

        @value.deleter
        def value(self) -> None:
            """
            当 `value` 标识为 `@property` 后, `@value.deleter` 表示设置属的方法
            """
            del self._val

    # 实例化一个对象并赋予属性值
    c = C("Hello")

    # 获取属性值
    assert c.value == "Hello"

    # 设置属性值
    c.value = 100
    assert c.value == 100

    # 删除属性值
    del c.value
    with raises(AttributeError):
        c.value


def test_multi_inheritance() -> None:
    """
    测试 Python 的多重继承

    Python 支持多重继承, 子类会继承所有父类中定义的属性和方法
    一般情况下, 继承的顺序为: 最左亲近原则, 即父类在继承列表中越靠左, 越和子类亲近
    """

    class I_(ABC):
        @abstractmethod
        def f1(self) -> str:
            pass

    class B1:
        def __init__(self) -> None:
            self.value = 10

        def f1(self) -> str:
            return "B1"

    class B2:
        def __init__(self) -> None:
            self.value = 20

        def f1(self) -> str:
            return "B2"

    class C(B1, B2, I_):
        """
        在继承列表中, `B1` 在最左边, 所以父类中如果包含相同的属性和方法, 以 `B1` 为最优先, 其次时 `B2`

        因为 `I_` 是一个纯接口, 不包含实现, 所以放在最后
        """

    # 确认 C 是 I_, B1, B2 的子类
    assert issubclass(C, I_)
    assert issubclass(C, B1)
    assert issubclass(C, B2)

    # 实例化 C 类对象
    c = C()

    # 确认 c 对象同时是 I_, B1, B2 类型的对象
    assert isinstance(c, I_)
    assert isinstance(c, B1)
    assert isinstance(c, B2)

    # 确认 c 对象继承的方法以 B1 类型优先
    assert c.value == 10
    assert c.f1() == "B1"


def test_dynamic_class() -> None:
    """
    通过 `__setattr__`, `__getattr__` 和 `__delattr__` 三个魔法方法用于获取, 设置和删除那些"未定义"的
    属性
    """

    class C:
        """
        动态类型, 可以设置和获取任意名称的属性
        """
        # 存储属性名和属性值的字典对象
        _props: Dict[str, Any]

        def __init__(self) -> None:
            """
            初始化对象, 为当前对象设置存储键值对的 `_props` 字段
            """
            # 注意, _props 字段需要设置在父类上
            # 否则会调用当前对象的 __setattr__ 方法, 而 __setattr__ 方法中又调用了 _props 字段,
            # 会造成循环调用
            super().__setattr__("_props", {})

        def __getattr__(self, name: str) -> Any:
            """
            根据属性名称获取属性值

            Args:
                name (str): 属性名

            Returns:
                Any: 属性值
            """
            try:
                return self._props[name]
            except KeyError:
                raise AttributeError(name)

        def __setattr__(self, name: str, value: Any) -> None:
            """
            设置属性名和属性值

            Args:
                name (str): 属性名
                value (Any): 属性值
            """
            try:
                self._props[name] = value
            except KeyError:
                raise AttributeError(name)

        def __delattr__(self, name: str) -> None:
            """
            根据属性名删除属性

            Args:
                name (str): 属性名
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


# 泛型参数
T = TypeVar("T", int, float)


def test_delegate_class() -> None:
    """
    测试代理类型
    """
    class B(ABC):
        """
        接口类型
        """
        @abstractmethod
        def run(self, a: T, b: T) -> T:
            """
            接口方法

            Args:
                a (T): 参数 1
                b (T): 参数 2

            Returns:
                T: 返回值
            """

    class C1(B):
        """
        接口实现类
        """

        def run(self, a: T, b: T) -> T:
            """
            实现接口方法

            Args:
                a (T): 参数 1
                b (T): 参数 2

            Returns:
                T: 两个参数相加的结果
            """
            return a + b

    class C2(B):
        """
        接口实现类
        """

        def run(self, a: T, b: T) -> T:
            """
            实现接口方法

            Args:
                a (T): 参数 1
                b (T): 参数 2

            Returns:
                T: 两个参数相乘的结果
            """
            return a * b

    # 实例化对象
    c: B = C1()
    # 对实例进行代理
    d = Delegate(c)
    # 验证代理对象执行被代理方法的返回值
    assert d.run(1, 2) == "Result is: 3"

    # 实例化对象
    c = C2()
    # 对实例进行代理
    d = Delegate(c)
    # 验证代理对象执行被代理方法的返回值
    assert d.run(1, 2) == "Result is: 2"


def test_create_dynamic_class() -> None:
    """
    `type` 函数可以用于动态创建一个类型
    - 参数 1 为类型名称
    - 参数 2 为类型的父类集合
    - 参数 3 为类型的属性和方法
    """

    def A__init__(self, value: int) -> None:
        """
        类型 `A` 的构造方法

        Args:
            value (int): 属性值
        """
        self.value = value

    # 定义类型
    A = type(
        "A",  # 类型名称
        (object,),  # 类型的父类
        {
            "__init__":  A__init__,  # 类型的构造方法
            "value": 0,  # 类型的属性
            "work": lambda self, x: self.value + x,  # 类型的方法
        }
    )

    # 通过类型
    a = A(100)
    assert type(a) == A
    assert a.value == 100  # type: ignore

    a.value = 10  # type: ignore
    assert a.value == 10  # type: ignore
    assert a.work(1) == 11  # type: ignore


def test_class_slot() -> None:
    """
    `__slots__` 魔法字段用于定义对象具备的属性集合

    Python 作为解释型语音, 可以为对象添加任意属性而无需类型定义, 添加的属性以字典形式在对象内
    部以 `__dict__` 魔法字段存储

    `__slots__` 字段用于声明一个类型规定的字段集合, 设置了 `__slots__` 字段后, 对象能使用的
    属性就会约束在其定义范围内, 且不再通过 `__dict__` 字段存储对象属性
    """
    class C1:
        pass

    c1 = C1()

    # 操作对象的未定义属性, 类型检查失败 (可正常运行)
    c1.name = "Alvin"  # type: ignore
    assert c1.name == "Alvin"  # type: ignore

    c1.age = 41  # type: ignore
    assert c1.age == 41  # type: ignore

    assert c1.__dict__ == {
        "name": "Alvin",
        "age": 41,
    }

    class C2:
        """
        定义 `__slots__` 魔法字段, 设定可访问的对象属性列表

        定义了 `__slots__` 字段后, 相当于为类型提供了属性约束, 类型能用的属性必须在 `__slots__` 定义的列表中
        """
        # 定义可访问属性列表
        __slots__ = ("name", "age")

    c2 = C2()

    c2.name = "Alvin"  # type: ignore
    assert c2.name == "Alvin"  # type: ignore

    c2.age = 41  # type: ignore
    assert c2.age == 41  # type: ignore

    # 定义了 __slots__ 字段后, 对象不在具备 __dict__ 字段, 可访问的属性均有 __slots__ 字段定义
    assert not hasattr(c2, "__dict__")

    # 如果访问了未定义在 __slots__ 列表中的属性, 则会抛出异常
    with raises(AttributeError):
        c2.gender = "M"  # type: ignore


def test_automate_class() -> None:
    """
    测试自动装配类
    """

    class Member(Automate):
        # 定义可用的属性名
        __slots__ = ("id", "name", "price")

    class Group(Automate):
        # 定义可用的属性名
        __slots__ = ("id", "name", "members")

        # 定义特殊属性的类型
        members: List[Member]

    # 实例化自动装配类型的对象
    group = Group(1, "G-1", [
        Member(1, "S-1", 12.5),
        Member(2, "S-2", 22)
    ])

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
    assert json.dumps(group, indent=2) == """{
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

    # 测试通过 Dict 对象作为入参
    group = Group(**{
        "id": 1,
        "name": "G-1",
        "members": [{
            "id": 1,
            "name": "S-1",
            "price": 12.5
        }, {
            "id": 2,
            "name": "S-2",
            "price": 22}]
    })

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


def upper_attrs(attrs: Dict[str, Any]) -> Dict[str, Any]:
    """
    将属性名转为大写字母

    Args:
        attrs (Dict[str, Any]): 属性字典

    Returns:
        Dict[str, Any]: 属性名转为大写字母后的属性字典
    """
    new_attrs = {}

    # 遍历所有属性
    for name, value in attrs.items():
        if not name.startswith("__"):
            # 对于非私有属性, 将属性名转为大写字母
            name = name.upper()

        # 存储新的属性 Key/Value
        new_attrs[name] = value

    # 返回新的属性字典对象
    return new_attrs


def test_metaclass_by_function() -> None:
    """
    测试 `metaclass` 参数
    类型的 `metaclass` 参数用于指定一个函数, 该返回一个 `Type` 类型, 作为类的元类型
    """

    def metaclass(
        class_name: str,
        parents: Tuple[Type],
        attrs: Dict[str, Any],
    ) -> Type:
        """
        元类型函数, 返回一个 `Type` 对象, 用于设置目标类型的名称, 父类以及属性值

        Args:
            class_name (str): 目标类型的类名称
            parents (Tuple[Type]): 目标类型的父类集合
            attrs (Dict[str, Any]): 目标类型的属性集合

        Returns:
            Type: 目标类型的元类型对象
        """
        # 动态产生一个类型, 作为目标类型的元类型对象
        return type(
            class_name + "_New",  # 修改目标类型的类名称
            parents,
            upper_attrs(attrs),  # 处理目标类型的属性集合, 将属性名修改为大写
        )

    class C(metaclass=metaclass):  # type: ignore
        """
        定义类型, 并指定元类型为 `metaclass` 函数

        此时, `C` 类的类型定义由 `metaclass` 函数的返回值来定义
        """

        @property
        def value(self) -> int:
            """
            定义一个属性, 用于测试元类型将属性名修改为大写
            """
            return 100

    c = C()
    # 验证类名是否被修改
    assert type(c).__name__ == "C_New"
    # 验证属性名是否为大写
    assert c.VALUE == 100  # type: ignore

    # 验证原本的小写属性名是否已经失效
    with raises(AttributeError):
        assert c.value


def test_metaclass_by_class() -> None:
    """
    测试通过类型来定义目标类的元类型

    目标类的 `metaclass` 既可以为函数, 也可以为一个类, 如果是一个类的话, 必须通过 `__new__` 方法
    给目标类型返回类型定义
    """
    class MetaClass(type):
        """
        元类型, 用于创建一个描述类型的对象
        """
        def __new__(
            cls,
            class_name: str,
            parents: Tuple[Type],
            attrs: Dict[str, Any],
        ) -> Any:
            """
            创建实例, 根据传入的类型元数据, 返回用元数据创建的类型对象

            注意, 这个方法不能标识 `@classmethod` 装饰器, 因为 `cls` 参数是外部显式传递的.
            如果标识了 `@classmethod`, 则会重复传递 `cls` 参数

            Args:
                class_name (str): _description_
                parents (Tuple[Type]): _description_
                attrs (Dict[str, Any]): _description_

            Returns:
                Any: _description_
            """
            return type(
                class_name + "_New",  # 修改目标类型的类名称
                parents,
                upper_attrs(attrs),  # 处理目标类型的属性集合, 将属性名修改为大写
            )

    class C(metaclass=MetaClass):
        """
        定义类型, 并指定元类型为 `MetaClass` 类型

        此时, `C` 类的类型定义由 `MetaClass` 类型产生的对象来定义
        """
        @property
        def value(self) -> int:
            """
            定义一个属性, 用于测试元类型将属性名修改为大写
            """
            return 100

    c = C()
    # 验证类名是否被修改
    assert type(c).__name__ == "C_New"
    # 验证属性名是否为大写
    assert c.VALUE == 100  # type: ignore

    # 验证原本的小写属性名是否已经失效
    with raises(AttributeError):
        assert c.value


def test_singleton_class() -> None:
    """
    测试单例类型

    Python 可以通过 `__new__` 魔法方法完成单例, 即让一个类型只能实例化一个对象
    """
    class C:
        """
        单例类型
        """
        # 保持单例的类字段
        _inst: Optional["C"] = None  # noqa

        @classmethod
        def __new__(cls: type["C"], *args, **kwargs) -> "C":  # noqa
            """
            创建实例

            为了保证创建实例时单例, 无论执行多少次创建实例方法, 均返回 `_inst` 字段引用的对象

            Args:
                cls (type[&quot;C&quot;]): 当前类型

            Returns:
                C: 当前类型的单例实例
            """
            if not cls._inst:
                # 如果单例未被创建, 则创建单例实例, 并引用到 _inst 字段上
                cls._inst = super().__new__(cls)

            # 返回单例实例
            return cls._inst

        def __init__(self, value: Any) -> None:
            """
            初始化对象, 设置对象的属性

            Args:
                value (Any): 属性值
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
