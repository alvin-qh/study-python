from cmath import pi
from math import atan2, sqrt, tan
from typing import List, Sequence

import pytest
from utils.typedef import Vector
from utils.vector import (
    add,
    angle_between,
    as_matrix,
    as_matrix3d,
    as_polygons,
    as_triangle,
    as_vector,
    as_vector2d,
    as_vector3d,
    component,
    cross,
    distance,
    dot,
    length,
    linear_combination,
    multiply_matrix_vector,
    normal,
    perimeter,
    scale,
    subtract,
    to_2d_projection,
    to_cartesian,
    to_degree,
    to_polar,
    to_radian,
    translate,
    unit,
    vertices,
)


def test_as_vector2d() -> None:
    """测试将数值序列转为二维向量"""
    with pytest.raises(StopIteration):
        as_vector2d([10])

    assert as_vector2d([10, 20]) == (10, 20)
    assert as_vector2d([10, 20, 30]) == (10, 20)


def test_as_vector3d() -> None:
    """测试将数值序列转为三维向量"""
    with pytest.raises(StopIteration):
        as_vector3d([10])

    with pytest.raises(StopIteration):
        as_vector3d([10, 20])

    assert as_vector3d([10, 20, 30]) == (10, 20, 30)
    assert as_vector3d([10, 20, 30, 40]) == (10, 20, 30)


def test_as_vector() -> None:
    """测试将数值序列转为 N 维向量"""
    assert as_vector([10]) == (10,)
    assert as_vector([10, 20]) == (10, 20)
    assert as_vector([10, 20, 30]) == (10, 20, 30)
    assert as_vector([10, 20, 30, 40]) == (10, 20, 30, 40)
    assert as_vector([n for n in range(100)]) == tuple(n for n in range(100))


def test_as_triangle() -> None:
    """测试将三维向量序列转为三角形"""
    with pytest.raises(StopIteration):
        as_triangle([[1, 2, 3], [4, 5, 6]])

    with pytest.raises(StopIteration):
        as_triangle([[1, 2, 3], [4, 5, 6], [7, 8]])

    assert as_triangle([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
    )


def test_as_matrix3d() -> None:
    """测试将三维向量序列转为三维矩阵值"""
    with pytest.raises(StopIteration):
        as_matrix3d([[1, 2, 3], [4, 5]])

    assert as_matrix3d([[1, 2, 3]]) == [(1, 2, 3)]

    assert as_matrix3d([[1, 2, 3], [4, 5, 6]]) == [(1, 2, 3), (4, 5, 6)]

    assert as_matrix3d([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
    ]

    assert as_matrix3d([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]) == [
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        (10, 11, 12),
    ]


def test_as_matrix() -> None:
    """测试将 N 维矩阵序列转为 N 维矩阵值"""
    with pytest.raises(ValueError, match="Invalid vector length 2"):
        as_matrix([[1, 2, 3], [4, 5]])

    assert as_matrix([[1]]) == [(1,)]
    assert as_matrix([[1, 2]]) == [(1, 2)]
    assert as_matrix([[1, 2, 3]]) == [(1, 2, 3)]
    assert as_matrix([[1, 2, 3], [4, 5, 6]]) == [(1, 2, 3), (4, 5, 6)]
    assert as_matrix([[1, 2, 3, 4], [4, 5, 6, 7]]) == [(1, 2, 3, 4), (4, 5, 6, 7)]
    assert as_matrix(
        [[1, 2, 3, 4, 5, 6], [4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15]]
    ) == [(1, 2, 3, 4, 5, 6), (4, 5, 6, 7, 8, 9), (10, 11, 12, 13, 14, 15)]


def test_as_polygons() -> None:
    """测试将向量序列的序列转为一个多面体"""
    assert as_polygons([[[1, 2, 3], [4, 5, 6], [7, 8, 9]]]) == [
        ((1, 2, 3), (4, 5, 6), (7, 8, 9))
    ]

    assert as_polygons(
        [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[11, 22, 33], [44, 55, 66], [77, 88, 99]]]
    ) == [
        (
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9),
        ),
        (
            (11, 22, 33),
            (44, 55, 66),
            (77, 88, 99),
        ),
    ]


def test_vertices() -> None:
    """测试从一个多面体中获取不重复的向量集合"""
    polygon = [
        [
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9),
        ],
        [
            (1, 2, 3),
            (4, 5, 6),
            (10, 11, 12),
        ],
    ]
    assert vertices(polygon) == [(7, 8, 9), (1, 2, 3), (10, 11, 12), (4, 5, 6)]


def test_length() -> None:
    """测试求向量长度"""

    # 测试求二维向量长度
    v: Vector = (1, 2)
    assert length(v) == sqrt(1 + 4)

    # 测试求三维向量长度
    v = (1, -2, 3)
    assert length(v) == sqrt(1 + 4 + 9)


def test_add() -> None:
    """测试向量加法"""

    # 测试二维向量相加
    vs: List[Vector] = [(1, 2), (3, 4)]
    assert add(*vs) == (1 + 3, 2 + 4)

    # 测试三维向量相加
    vs = [(1, 2, 3), (4, -5, 6)]
    assert add(*vs) == (1 + 4, 2 - 5, 3 + 6)


def test_subtract() -> None:
    """测试向量减法"""

    # 测试二维向量相减
    vs: List[Vector] = [(1, 2), (3, 4)]
    assert subtract(*vs) == (1 - 3, 2 - 4)

    # 测试三维向量相减
    vs = [(1, 2, 3), (4, -5, 6)]
    assert subtract(*vs) == (1 - 4, 2 + 5, 3 - 6)


def test_translate() -> None:
    """测试向量移动"""

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
    """测试角度转弧度"""

    assert to_radian(45) == pi / 4
    assert to_radian(60) == pi / 3
    assert to_radian(90) == pi / 2
    assert to_radian(180) == pi
    assert to_radian(270) == pi * 3 / 2
    assert to_radian(360) == pi * 2


def test_to_degree() -> None:
    """测试弧度转角度"""

    assert round(to_degree(pi / 4)) == 45.0
    assert round(to_degree(pi / 3)) == 60.0
    assert round(to_degree(pi / 2)) == 90.0
    assert round(to_degree(pi)) == 180.0
    assert round(to_degree(pi * 3 / 2)) == 270.0
    assert round(to_degree(pi * 2)) == 360.0


def test_to_cartesian() -> None:
    """测试极坐标转为笛卡尔坐标"""
    v = (3, 13)

    # 将极坐标转为
    r = to_cartesian(
        (length(v), atan2(v[1], v[0])),
    )

    # 验证极坐标转为笛卡尔坐标
    assert (round(r[0]), round(r[1])) == v


def test_to_polar() -> None:
    """测试笛卡尔坐标转为极坐标向量"""
    v = (3, 12)

    # 笛卡尔坐标转为极坐标
    po = to_polar(v)

    # 测试极坐标的两个维度
    assert (
        po[0] == length(v)  # 验证极坐标向量长度
        and round(tan(po[1])) == 12.0 / 3  # 验证极坐标向量角度
    )


def test_scale() -> None:
    """测试向量和标量相乘"""
    s = 10

    # 测试二维向量和标量相乘
    v: Vector = (3, 12)
    assert scale(s, v) == (30, 120)

    # 测试三维向量和标量相乘
    v = (3, 12, -5)
    assert scale(s, v) == (30, 120, -50)


def test_dot() -> None:
    """测试向量点积"""
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
    """测试计算向量距离"""
    v1: Vector
    v2: Vector

    # 计算定义在 x 和 y 轴的向量的距离
    v1, v2 = (3, 0), (0, 4)
    r = distance(v1, v2)
    assert r == 5.0

    v1, v2 = (3, 0, 0), (0, 4, 0)
    r = distance(v1, v2)
    assert r == 5.0


def test_perimeter() -> None:
    """测试计算向量围成的周长"""
    # 计算二维向量围成的周长
    vs: Sequence[Vector] = [
        (1, 3),
        (2, 3),
        (7, 8),
    ]
    assert round(perimeter(vs), 2) == 15.88

    # 计算三维向量围成的周长
    vs = [
        (1, 3, 2),
        (2, 3, 6),
        (7, 8, 10),
    ]
    assert round(perimeter(vs), 2) == 23.43


def test_cross() -> None:
    """测试三维向量向量积"""
    u, v = (1, 2, 3), (4, 5, 6)
    r = cross(u, v)
    assert r == (-3, 6, -3)


def test_angle_between() -> None:
    """测试计算向量夹角"""
    v1: Vector
    v2: Vector

    # 定义两个互相垂直的二维向量
    v1, v2 = (1, 0), (0, 1)
    # 计算两个向量的夹角
    r = angle_between(v1, v2)
    # 确认向量夹角为 90°
    assert r == pi / 2

    # 定义两个互相垂直的三维向量
    v1, v2 = (1, 0, 0), (0, 1, 0)
    # 计算两个向量的夹角
    r = angle_between(v1, v2)
    # 确认向量夹角为 90°
    assert r == pi / 2

    # 定义两个互相垂直的三维向量
    v1, v2 = (1, 0, 0), (0, 0, 1)
    # 计算两个向量的夹角
    r = angle_between(v1, v2)
    # 确认向量夹角为 90°
    assert r == pi / 2


def test_component() -> None:
    """测试计算指定向量在指定坐标轴的分量"""
    # 定义一个向量
    v = (1, 2, 3)

    # 计算向量在 x 轴的分量
    r = component(v, (1, 0, 0))
    assert r == 1

    # 计算向量在 y 轴的分量
    r = component(v, (0, 1, 0))
    assert r == 2

    # 计算向量在 z 轴的分量
    r = component(v, (0, 0, 1))
    assert r == 3


def test_to_2d_projection() -> None:
    """测试计算三维向量在二维平面的投影"""
    v = (1, 2, 3)
    assert to_2d_projection(v) == (1, 2)

    v = (-11, 13, 22)
    assert to_2d_projection(v) == (-11, 13)


def test_unit() -> None:
    """测试获取指定向量的另一个向量, 后者和前者方向一致, 且长度为 `1`"""
    v = (12, 13, 14)

    # 获取和向量 v 相关的单位向量 (方向一致, 且长度为 1)
    v_new = unit(v)

    assert v_new == (
        0.5318906486135235,
        0.5762148693313172,
        0.6205390900491108,
    )
    assert length(v_new) == 1.0
    assert angle_between(v, v_new) == 0.0


def test_normal() -> None:
    """测试计算三维向量的法向量"""
    face = as_triangle(
        [
            (1, 10, -22),
            (11, 13, 16),
            (21, 23, 26),
        ]
    )
    assert normal(face) == (-350, 280, 70)


def test_linear_combination() -> None:
    """测试计算向量的线性组合"""
    vs = [
        (1, 3, 5),
        (10, 13, 15),
        (29, 33, 13),
    ]
    assert linear_combination([0.1, 1.5, 2], vs) == (73.1, 85.8, 49.0)


def test_multiply_matrix_vector() -> None:
    """测试计算一个矩阵和一系列向量的乘积"""
    matrix = [
        (1, 3, 5),
        (10, 13, 15),
        (29, 33, 13),
    ]

    v = (1, 3, 5)
    assert multiply_matrix_vector(matrix, v) == (176, 207, 115)
