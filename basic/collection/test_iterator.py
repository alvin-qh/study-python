from functools import reduce
from typing import Iterator


def test_sum_function() -> None:
    """
    计算集合内数值总和和后一个值的和
    """
    r = sum([1], 2)  # 1 + 2
    assert r == 3

    r = sum([1, 2, 3, 4, 5], 2)  # 15 + 2
    assert r == 17


def test_max_min_function() -> None:
    """
    计算一组参数 (或一个集合中) 的最大值或最小值
    """
    r = max(10, 20, 30)
    assert r == 30

    r = min(10, 20, 30)
    assert r == 10

    r = max([1, 2, 3, 4, 5])
    assert r == 5

    r = min([1, 2, 3, 4, 5])
    assert r == 1


def test_zip_function() -> None:
    """
    测试 zip 函数, 将两个集合通过笛卡尔积运算合并为一个集合
    返回集合的迭代器对象
    """
    c1 = [1, 2, 3]
    c2 = [4, 5, 6]

    # 将迭代器对象转为 list 对象
    ziped = list(zip(c1, c2))
    assert ziped == [(1, 4), (2, 5), (3, 6)]


def test_all_function() -> None:
    """
    测试 all 函数, 如果一个集合中所有值都表示 True, 则返回 True
    """
    r = all([1, 0, 1, 2, 3])
    assert r is False

    r = all([1, 2, 3, 4, 5])
    assert r is True

    r = all([])
    assert r is True


def test_any_function() -> None:
    """
    测试 any 函数, 如果一个集合中所有值都表示 False, 则返回 False
    """
    r = any([1, 0, 1, 2, 3])
    assert r is True

    r = any([0, 0, 0, 0, 0])
    assert r is False


def test_enumerate_function() -> None:
    """
    enumerate 返回一个迭代器, 每一项为集合一个元素 (下标, 值)
    """
    c = ["A", "B", "C", "D"]
    r = []
    for i, v in enumerate(c):
        r.append((i, v))

    assert r == [(0, "A"), (1, "B"), (2, "C"), (3, "D")]


class Iter:
    """
    定义一个迭代器类
    具备 __next__ 方法的类对象可被迭代访问, 即通过 next 函数获取序列值
    具备 __iter__ 方法的类对象被认为是一个迭代器对象, 可以在 for ... in ... 循环中使用
    """

    def __init__(self, min_: int, max_: int) -> None:
        """
        初始化迭代器
        该迭代器表示一个 [min, max) 区间的递增数列

        Args:
            min_ (int): 起始值
            max_ (int): 结束值
        """
        # self._cur 保存当前迭代的值
        self._min = self._cur = min_
        self._max = max_

    def __iter__(self) -> Iterator[int]:
        """
        获取迭代器
        由于 Iter 类本身就是可迭代的, 所以该方法只是返回当前对象

        Returns:
            Iterator[int]: 返回一个迭代器对象
        """
        return self

    def __next__(self) -> int:
        """
        具备 __next__ 方法的类可被迭代, 即可通过 next(...) 函数返回迭代对象的下一项

        Raises:
            StopIteration: 迭代器终止

        Returns:
            int: 下一项值
        """
        if self._cur == self._max:
            # 抛出该异常表示迭代结束
            raise StopIteration()

        # 返回当前值
        _cur = self._cur
        # 当前值变为下一个值
        self._cur += 1
        return _cur


def test_iterator_object() -> None:
    """
    测试迭代器类型
    """
    it = Iter(1, 10)
    assert next(it) == 1
    assert next(it) == 2

    it = Iter(1, 10)
    # 测试迭代器转 list 对象
    assert list(it) == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    it = Iter(1, 10)
    # 测试迭代器在 for ... in ... 中的使用
    assert [n for n in it] == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_map_reduce() -> None:
    """
    测试 map 和 reduce 函数

    map 用于将集合中的每一项进行运算, 形成新的集合
    reduce 用于对集合中的每一项和上一次计算结果进行计算, 得到最终结果
    """
    c = [1, 2, 3]

    # 相当于对 c 集合中的每一项执行指定函数
    r = map(lambda v: v + 1, c)
    assert list(r) == [2, 3, 4]

    # 初始值是 1, 用上次结果和集合中的每一项进行运算
    # 相当于 1(初始值) * 1 * 2 * 3 == 6
    r = reduce(lambda x, y: x * y, c, 1)
    assert r == 6
