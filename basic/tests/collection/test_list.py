from pytest import raises


def test_as_stack() -> None:
    """列表集合的 LIFO (后进先出) 方式操作

    列表集合可以当作栈使用
    """
    c = [1, 2]

    # 弹出最后一个元素 2
    r = c.pop()
    assert r == 2

    # 弹出第一个元素 1
    r = c.pop()
    assert r == 1

    # 列表为空, 无法弹出元素, 抛出异常
    with raises(IndexError):
        c.pop()

    # 添加元素 1 和 2
    c.append(1)
    c.append(2)

    # 弹出最后一个元素 2
    r = c.pop()
    assert r == 2


def test_slice_function() -> None:
    """测试切片对象

    `slice(a, b, c)` 函数返回一个切片对象, 切片对象可以将数组按指定要求进行切割

    Python 中, 可以通过 `x[a:b:c]` 语法直接对列表对象进行切片, 结果和通过切片对象一致
    """
    c = [1, 2, 3, 4, 5]

    # 获取列表前两项
    assert c[slice(2)] == [1, 2]
    assert c[slice(2)] == c[:2]

    # 获取列表后两项
    assert c[slice(3, 5)] == [4, 5]
    assert c[slice(3, 5)] == c[3:]

    # 获取列表第 4 项
    assert c[slice(3, -1)] == [4]
    assert c[slice(3, -1)] == c[3:-1]

    # 获取列表第 2~5 项
    assert c[slice(2, 5)] == [3, 4, 5]
    assert c[slice(2, 5)] == c[2:5]

    # 获取列表第 2~5 项, 步长为 2
    assert c[slice(2, 5, 2)] == [3, 5]
    assert c[slice(2, 5, 2)] == c[2:5:2]


def test_extend_function() -> None:
    """测试集合内容扩展

    对列表集合的扩展, 相当于在列表的末尾连接新的列表

    注意: `extend` 方法会改变列表对象本身, 相当于列表的 `+=` 运算符
    """
    c = ["a", "b", "c"]
    c.extend(["x", "y", "z"])
    assert c == ["a", "b", "c", "x", "y", "z"]

    c = ["a", "b", "c"]
    c += ["x", "y", "z"]
    assert c == ["a", "b", "c", "x", "y", "z"]


def test_2_dimensional_list() -> None:
    """测试二阶数组"""

    # 定义一个二阶数组
    m = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]

    # 数组转置 (求 T)
    m_t = [list(n) for n in zip(*m)]
    assert m_t == [
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
    ]

    # 数组旋转 (逆时针 90°)
    m_r = [list(n) for n in zip(*m)][::-1]
    assert m_r == [
        [3, 6, 9],
        [2, 5, 8],
        [1, 4, 7],
    ]
