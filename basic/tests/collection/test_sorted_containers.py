from functools import cmp_to_key

from sortedcontainers import SortedList

"""参考: https://grantjenks.com/docs/sortedcontainers/"""


def test_sorted_list() -> None:
    """测试 SortedList 类

    该类是一个自动排序的 list 类型, 具备 list 类型的所有行为, 和 list 不同的是, SortedList 会对存入的元素自动进行排序
    """

    # 定义一个 SortedList 对象
    c = SortedList(["e", "a", "c", "d", "b"])
    # 确认元素经过排序
    assert c == ["a", "b", "c", "d", "e"]
    # 对元素查找是在排序结果上进行
    assert c.index("b") == 1

    # 更新元素后, 结果依然有序
    c.update(["z", "x", "y"])
    assert c == ["a", "b", "c", "d", "e", "x", "y", "z"]

    # 添加元素后, 结果依然有序
    c.add("f")
    assert c.index("f") == 5

    # 获取一个切片, 相当于从 "c" 元素开始, 到 "z" 元素结束
    r = list(c.irange("c", "z"))
    assert r == ["c", "d", "e", "f", "x", "y", "z"]

    # 某些时候需要以特殊规则对元素进行排序
    # 和 sorted 函数类似, SortedList 对象也是通过 cmp_to_key 函数产生的 Key 类型进行比较的

    # 定义一个用于比较的 Key 类型
    K = cmp_to_key(lambda a, b: ord(b) - ord(a))  # type:ignore
    # 通过 Key 对象的比较规则定义 SortedList 对象
    c = SortedList("abcdefg", key=K)
    # 确认对象内容依据 Key 对象定义的排序规则进行
    assert list(c) == ["g", "f", "e", "d", "c", "b", "a"]

    # 如果为 SortedList 对象设置了特殊的排序规则, 则不能直接使用 irange 方法进行切片
    # 可以通过 irange_key 方法通过同样的排序 Key 对象进行切片

    # 通过两个 Key 对象进行进行切片
    r = list(c.irange_key(K("e"), K("c")))
    # 验证切片结果
    assert r == ["e", "d", "c"]

    # 利用二分查找查找待插入元素所在的位置
    # bisect_left, bisect_right 方法, 查找指定元素插入后的位置.
    # 如果指定元素已存在, 则前者返回已存在元素左侧的索引, 后者返回右侧的索引

    # 生成一个有序序列, 缺少 d 元素
    c = SortedList(["e", "a", "c", "b"])

    # 查找 d 元素所在的索引
    n = c.bisect_left("d")
    assert n == 3

    # 插入 d 元素
    c.add("d")
    # 确认 d 元素插入后的索引是 3
    assert c.index("d") == 3

    # 通过自定义排序规则的 Key 类型, 利用二分查找查找待插入元素所在的位置
    # bisect_key_left   , bisect_key_right 方法, 查找指定元素插入后的位置.
    # 如果指定元素已存在, 则前者返回已存在元素左侧的索引, 后者返回右侧的索引

    K = cmp_to_key(lambda a, b: ord(b) - ord(a))  # type: ignore
    # 通过 Key 对象的比较规则定义 SortedList 对象
    c = SortedList("abce", key=K)

    n = c.bisect_key_right(K("d"))
    assert n == 1

    c.add("d")
    assert c.index("d") == 1
