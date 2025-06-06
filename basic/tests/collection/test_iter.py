from functools import reduce

from basic.collection.iterator import Iter


def test_sum_function() -> None:
    """计算集合内数值总和和后一个值的和"""

    r = sum([1], 2)  # 1 + 2
    assert r == 3

    r = sum([1, 2, 3, 4, 5], 2)  # 15 + 2
    assert r == 17


def test_max_min_function() -> None:
    """计算一组参数 (或一个集合中) 的最大值或最小值"""

    r = max(10, 20, 30)
    assert r == 30

    r = min(10, 20, 30)
    assert r == 10

    r = max([1, 2, 3, 4, 5])
    assert r == 5

    r = min([1, 2, 3, 4, 5])
    assert r == 1


def test_zip_function() -> None:
    """测试 `zip` 函数

    将两个集合通过笛卡尔积运算合并为一个集合, 返回集合的迭代器对象
    """
    c1 = [1, 2, 3]
    c2 = [4, 5, 6]

    # 将迭代器对象转为 list 对象
    ziped = list(zip(c1, c2))
    assert ziped == [(1, 4), (2, 5), (3, 6)]


def test_all_function() -> None:
    """
    测试 `all` 函数

    如果一个集合中所有值都表示 `True`, 则返回 `True`
    """
    r = all([1, 0, 1, 2, 3])
    assert r is False

    r = all([1, 2, 3, 4, 5])
    assert r is True

    r = all([])
    assert r is True


def test_any_function() -> None:
    """
    测试 `any` 函数

    如果一个集合中所有值都表示 `False`, 则返回 `False`
    """
    r = any([1, 0, 1, 2, 3])
    assert r is True

    r = any([0, 0, 0, 0, 0])
    assert r is False


def test_enumerate_function() -> None:
    """返回一个迭代器,

    通过 `enumerate` 函数, 返回一个 List 集合每项的下标和元素值
    """
    c = ["A", "B", "C", "D"]
    r = []
    for i, v in enumerate(c):
        r.append((i, v))

    assert r == [(0, "A"), (1, "B"), (2, "C"), (3, "D")]


def test_iterator_object() -> None:
    """测试迭代器类型"""

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
    测试 `map` 和 `reduce` 函数

    - `map` 用于将集合中的每一项进行运算, 形成新的集合
    - `reduce` 用于对集合中的每一项和上一次计算结果进行计算, 得到最终结果
    """
    c = [1, 2, 3]

    # 相当于对 c 集合中的每一项执行指定函数
    r = map(lambda v: v + 1, c)
    assert list(r) == [2, 3, 4]

    # 初始值是 1, 用上次结果和集合中的每一项进行运算
    # 相当于 1(初始值) * 1 * 2 * 3 == 6
    n = reduce(lambda x, y: x * y, c, 1)
    assert n == 6

    # 测试 map 和 reduce 函数联合使用
    nums = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
    }

    # 将数字内容的字符串转为数字
    # map 操作将字符串逐字符转化为对应的数字集合
    # reduce 将 map 的结果集合进行累加
    #   n, i: n 为上次计算的结果, i 为本次要计算的值
    n = reduce(
        lambda n, i: n * 10 + i,
        map(lambda c: nums[c], "12345"),
        0,
    )
    assert n == 12345
