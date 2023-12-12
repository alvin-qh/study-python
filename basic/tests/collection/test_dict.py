from typing import Any


def test_copy_dict() -> None:
    """测试拷贝一个字典对象"""

    dict_src = {"a": 100, "b": 200}

    # 通过 copy 函数进行拷贝
    dict_copied = dict_src.copy()
    assert dict_copied == dict_src

    # 通过 ** 运算符进行拷贝
    dict_copied = {**dict_src}
    assert dict_copied == dict_src


class Foo:
    """定义一个类"""

    def __init__(self, a: Any, b: Any) -> None:
        """构造器, 设置对象字段

        Args:
            - `a` (`Any`): `a` 字段的值
            - `b` (`Any`): `b` 字段的值
        """
        self.a = a
        self.b = b

    def update(self, **kwargs: Any) -> None:
        """更新对象 __dict__ 内置字典的值"""
        self.__dict__.update(**kwargs)


def test_dict_of_objects() -> None:
    """测试对象的内置字典"""

    # 为对象设置字段 a 和 b
    foo = Foo(a=10, b="A")
    # 通过 __dict__ 获取对象的内置字典
    assert foo.__dict__ == {"a": 10, "b": "A"}

    # 更新对象的内置字典
    foo.update(c=True)
    assert foo.__dict__ == {"a": 10, "b": "A", "c": True}

    # 为对象附加字段值
    foo.d = 0.1  # type: ignore
    assert foo.__dict__ == {"a": 10, "b": "A", "c": True, "d": 0.1}


def test_generate_dict_by_for() -> None:
    """测试通过 `for` 语句遍历集合并产生字典"""

    a = [1, 2, 3, 4]
    b = ["A", "B", "C", "D"]

    # 合并两个集合, 并通过 for 操作产生字典
    # 产生一个以 a 集合的每一项为 key, 以 b 集合对应项为 value 的字典
    d = {k: v for k, v in zip(a, b)}
    assert d == {1: "A", 2: "B", 3: "C", 4: "D"}

    c = "Hello"
    # 产生一个以每个字符下标为 key, 以每个字符为 value 的字典
    d = {k: v for k, v in enumerate(c)}
    assert d == {0: "H", 1: "e", 2: "l", 3: "l", 4: "o"}
