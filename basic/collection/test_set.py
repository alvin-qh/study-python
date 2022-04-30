from pytest import raises


def test_set_operators() -> None:
    """
    测试 set 对象的运算符
    """
    s1 = {1, 2, 3}
    s2 = {3, 4, 5}

    # 集合并集
    assert s1 | s2 == {1, 2, 3, 4, 5}
    assert s1 | s2 == s1.union(s2)

    # 集合交集
    assert s1 & s2 == {3}
    assert s1 & s2 == s1.intersection(s2)

    # 集合差运算
    assert s1 - s2 == {1, 2}
    assert s1 - s2 == s1.difference(s2)

    # 集合差集
    assert s1 ^ s2 == {1, 2, 4, 5}
    assert s1 ^ s2 == s1.symmetric_difference(s2)


def test_isdisjoint_method() -> None:
    """
    判断两个集合是否具备交集
    """
    s1 = {1, 2, 3}
    s2 = {3, 4, 5}

    # 此时两个集合有交集
    assert s1.isdisjoint(s2) is False

    # 移除两个集合相同的元素
    s2.discard(3)
    # 此时两个集合无交集
    assert s1.isdisjoint(s2) is True


def test_superset_subset_method() -> None:
    """
    计算两个集合相互包含关系
    """
    s1 = {1, 2, 3}
    s2 = {2, 3, 4}

    # 判断 s1 是否包含 s2
    assert s1.issuperset(s2) is False
    assert (s1 > s2) is False

    # 判断 s2 是否属于 s1
    assert s2.issubset(s1) is False
    assert (s2 < s1) is False

    # 从 s2 中删除 s1 中不存在的元素
    s2.discard(4)

    # 判断 s1 是否包含 s2
    assert s1.issuperset(s2) is True
    assert (s1 > s2) is True

    # 判断 s2 是否属于 s1
    assert s2.issubset(s1) is True
    assert (s2 < s1) is True


def test_frozenset() -> None:
    """
    frozenset 用于创建一个只读的 set 对象
    """
    s = frozenset([1, 2, 3])

    # frozenset 无法添加元素
    with raises(AttributeError):
        s.add(4)
