from functools import cmp_to_key
from random import Random
from typing import Any


def test_cmp_to_key() -> None:
    """
    测试 cmp_to_key 函数

    cmp_to_key 函数参数是一个比较函数 (返回 -1, 0, 1). 返回一个可比较的类.
    通过返回的类可以构造一个对象, 两个同类型对象可以根据定义的比较函数参数进行比较
    """
    # 传入比较函数, 返回一个可比较的类
    cmp = cmp_to_key(lambda a, b: a - b)  # type:ignore

    # 实例化可比较类, 通过之前定义的比较函数进行比较
    # 相当于 lambda 10, 20: 10 - 20 结果为 -10, 表示小于
    r = cmp(10) == cmp(20)
    assert r is False

    r = cmp(10) > cmp(20)
    assert r is False

    r = cmp(10) < cmp(20)
    assert r is True


def test_sort_simple() -> None:
    """
    测试简单排序
    """
    # 随机数对象
    r = Random()
    c = [1, 2, 3, 4, 5]

    # 打乱集合内容顺序
    r.shuffle(c)

    # 对集合进行排序
    cs = sorted(c)
    assert cs == [1, 2, 3, 4, 5]  # 从小到大的排序

    # 对集合进行排序 (倒序)
    cs = sorted(c, reverse=True)
    assert cs == [5, 4, 3, 2, 1]  # 从大到小的排序

    # 通过一个 cmp_to_key 返回一个可比较类型
    # 通过实例化可比较类型的对象后, 进行集合元素的比较
    # 参见: test_cmp_to_key 范例
    cs = sorted(c, key=cmp_to_key(lambda a, b: a - b))  # type:ignore
    assert cs == [1, 2, 3, 4, 5]


class Foo:
    """
    测试排序的类
    """

    def __init__(self, name: str, value: Any) -> None:
        """
        初始化对象

        Args:
            name (str): 名称
            value (Any): 值
        """
        self.name = name
        self.value = value

    def __eq__(self, other: Any) -> bool:
        """
        判断两个对象是否相等, 用于测试中断言等值判断

        Args:
            other (Any): 被比较的对象

        Returns:
            bool: 两个对象是否相等
        """
        if not isinstance(other, Foo):
            return False

        return (
            self.name == other.name
            and self.value == other.value
        )


def test_sort_objects() -> None:
    # 定义对象集合
    c = [Foo("a", 400), Foo("b", 300), Foo("c", 200), Foo("d", 100)]

    # 根据对象的 name 字段排序
    cs = sorted(c, key=lambda x: x.name, reverse=True)
    assert cs == [Foo("d", 100), Foo("c", 200), Foo("b", 300), Foo("a", 400)]

    # 根据对象的 value 字段排序
    cs = sorted(c, key=lambda x: x.value)
    assert cs == [Foo("d", 100), Foo("c", 200), Foo("b", 300), Foo("a", 400)]

    # 通过 cmp_to_key 函数进行排序
    cs = sorted(c, key=cmp_to_key(  # type:ignore
        lambda a, b: b.name.casefold() > a.name.casefold())  # type:ignore
    )
    assert cs == [Foo("a", 400), Foo("b", 300), Foo("c", 200), Foo("d", 100)]
