from cmath import pi
from math import atan2, sqrt, tan
from typing import List

from common import Vector

from .vector import (add, cross, distance, dot, length, scale, subtract,
                     to_cartesian, to_degree, to_polar, to_radian, translate)


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


def test_to_radian() -> None:
    """
    测试角度转弧度
    """
    assert to_radian(45) == pi / 4
    assert to_radian(60) == pi / 3
    assert to_radian(90) == pi / 2
    assert to_radian(180) == pi
    assert to_radian(270) == pi * 3 / 2
    assert to_radian(360) == pi * 2


def test_to_degree() -> None:
    """
    测试弧度转角度
    """
    assert round(to_degree(pi / 4)) == 45.0
    assert round(to_degree(pi / 3)) == 60.0
    assert round(to_degree(pi / 2)) == 90.0
    assert round(to_degree(pi)) == 180.0
    assert round(to_degree(pi * 3 / 2)) == 270.0
    assert round(to_degree(pi * 2)) == 360.0


def test_to_cartesian() -> None:
    """
    测试极坐标转为笛卡尔坐标
    """
    v = (3, 13)

    # 将极坐标转为
    r = to_cartesian(
        (length(v), atan2(v[1], v[0])),
    )

    # 验证极坐标转为笛卡尔坐标
    assert (round(r[0]), round(r[1])) == v


def test_to_polar() -> None:
    """
    测试笛卡尔坐标转为极坐标
    """
    v = (3, 12)

    # 笛卡尔坐标转为极坐标
    po = to_polar(v)

    # 测试极坐标的两个维度
    assert (
        po[0] == length(v)  # 验证极坐标向量长度
        and
        round(tan(po[1])) == 12.0 / 3  # 验证极坐标向量角度
    )


def test_scale() -> None:
    """
    测试向量和标量相乘
    """
    n = 10

    # 测试二维向量和标量相乘
    v: Vector = (3, 12)
    assert scale(v, n) == (30, 120)

    # 测试三维向量和标量相乘
    v = (3, 12, -5)
    assert scale(v, n) == (30, 120, -50)


def test_dot() -> None:
    """
    测试向量点积
    """
    u: Vector
    v: Vector

    # 测试二维向量点积
    u, v = (1, 2), (3, 4)
    r = dot(u, v)
    assert r == 1 * 3 + 2 * 4

    # 测试三维向量点积
    u, v = (1, 2, 3), (4, 5, 6)
    r = dot(u, v)
    assert r == 1 * 4 + 2 * 5 + 3 * 6


def test_distance() -> None:
    """
    测试计算向量距离
    """
    v1: Vector
    v2: Vector
    
    # 计算定义在 x 和 y 轴的向量的距离
    v1, v2 = (3, 0), (0, 4)
    r = distance(v1, v2)
    assert r == 5.0
    
    v1, v2 = (3, 0, 0), (0, 4, 0)
    r = distance(v1, v2)
    assert r == 5.0


def test_cross() -> None:
    """
    测试三维向量向量积
    """
    u, v = (1, 2, 3), (4, 5, 6)
    r = cross(u, v)
    assert r == (-3, 6, -3)
