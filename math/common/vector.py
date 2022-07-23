from math import atan2, cos, pi, sin, sqrt
from typing import Iterable, List

from . import Number, PolarVector, Vector, Vector2D, Vector3D


def length(v: Vector) -> float:
    """
    计算一个 N 维向量的长度

    Args:
        v (Vector): 一个 N 维向量

    Returns:
        float: 向量长度
    """
    return sqrt(sum(coord**2 for coord in v))


def add(*vs: Vector) -> Vector:
    """
    将一个 N 维向量集合中的所有向量进行相加后返回结果

    Args:
        vs (Iterable[Vector]): 向量集合

    Returns:
        Vector: 所有向量相加后的结果
    """
    # 获取向量的维数
    n = len(vs[0])

    # 初始化记录结果的向量
    r = [0.] * n

    for v in vs:
        for i in range(n):
            r[i] += v[i]

    return tuple(r)


def translate(v_off: Vector, vs: Iterable[Vector]) -> List[Vector]:
    """
    移动一个向量集合中的每个向量

    最终, 向量组成的形态不变, 但向量的位置会发生变化

    Args:
        v_off (Vector): 向量偏移量
        vs (Iterable[Vector]): 向量集合

    Returns:
        List[Vector]: 移动位置后的向量集合
    """
    return [add(v, v_off) for v in vs]


# 定义 1° 角度对应的弧度
ONE_DEGREE = pi / 180


def to_radian(angle: Number) -> Number:
    """
    将角度转换为弧度

    Args:
        angle (Number): 角度

    Returns:
        Number: 对应的弧度
    """
    return angle * ONE_DEGREE


# 定义 1 弧度对应的角度
ONE_RAD = 180 / pi


def to_degree(radian: Number) -> Number:
    """
    将弧度转换为角度

    Args:
        radian (Number): 弧度

    Returns:
        Number: 对应的角度
    """
    return radian * ONE_RAD


def to_cartesian(polar_vector: PolarVector) -> Vector2D:
    """
    将极坐标向量转换为笛卡尔坐标

    Args:
        polar_vector (PolarVector): 极坐标向量, 两个分量为 `(向量长度, 弧度)`

    Returns:
        Vector2D: 极坐标向量
    """
    # 获取极坐标向量分量
    length, angle = polar_vector[0], polar_vector[1]
    # 通过余弦函数和正弦函数求笛卡尔 x, y 坐标
    return (length * cos(angle), length * sin(angle))


def to_polar(v: Vector2D) -> PolarVector:
    """
    将笛卡尔坐标向量转换为极坐标向量

    Args:
        v (Vector2D): 二维向量的笛卡尔坐标

    Returns:
        PolarVector: 二维向量的极坐标
    """
    # 获取笛卡尔坐标向量的分量
    x, y = v[0], v[1]
    # 利用 atan2 函数, 根据笛卡尔坐标分量求弧度
    angle = atan2(y, x)
    # 利用 length 函数求向量的长度, 返回极坐标向量
    return (length(v), angle)


def scale(v: Vector, scalar: Number) -> Vector:
    """
    二维向量和标量相乘

    Args:
        v (Vector): N 维向量

    Returns:
        Vector: 缩放后的向量
    """
    return tuple(coord * scalar for coord in v)
