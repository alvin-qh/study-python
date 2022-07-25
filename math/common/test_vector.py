from math import sqrt
from typing import List

from common import Vector

from .vector import add, length, subtract, translate


def test_length() -> None:
    """
    测试求向量长度
    """
    # 测试求二维向量长度
    v: Vector = (1, 2)
    assert length(v) == sqrt(1 + 4)

    # 测试求三维向量长度
    v = (1, -2, 3)
    assert length(v) == sqrt(1 + 4 + 9)


def test_add() -> None:
    """
    测试向量加法
    """
    # 测试二维向量相加
    vs: List[Vector] = [(1, 2), (3, 4)]
    assert add(*vs) == (1 + 3, 2 + 4)

    # 测试三维向量相加
    vs = [(1, 2, 3), (4, -5, 6)]
    assert add(*vs) == (1 + 4, 2 - 5, 3 + 6)


def test_subtract() -> None:
    """
    测试向量减法
    """
    # 测试二维向量相减
    vs: List[Vector] = [(1, 2), (3, 4)]
    assert subtract(*vs) == (1 - 3, 2 - 4)

    # 测试三维向量相减
    vs = [(1, 2, 3), (4, -5, 6)]
    assert subtract(*vs) == (1 - 4, 2 + 5, 3 - 6)


def test_translate() -> None:
    """
    测试向量移动
    """
    # 表示位移的向量
    u: Vector = (1, 3)
    # 要移动的向量几何
    vs: List[Vector] = [
        (1, 1),
        (1, -2),
        (2, 3),
    ]
    # 测试二维向量移动
    assert translate(u, vs) == [
        add(u, vs[0]),
        add(u, vs[1]),
        add(u, vs[2]),
    ]

    # 表示位移的向量
    u = (1, 3, 4)
    # 要移动的向量几何
    vs = [
        (1, 1, 1),
        (1, -2, 1),
        (2, 3, -3),
    ]
    # 测试三维向量移动
    assert translate(u, vs) == [
        add(u, vs[0]),
        add(u, vs[1]),
        add(u, vs[2]),
    ]
