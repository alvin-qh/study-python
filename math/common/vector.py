from math import atan2, cos, pi, sin, sqrt
from typing import Iterable, List

from . import Number, PolarVector, Vector2D


def length(v: Vector2D) -> Number:
    """
    计算一个二维向量的长度

    Args:
        v (Vector2D): 一个向量

    Returns:
        Number: 向量长度
    """
    return sqrt(v[0]**2 + v[1]**2)


def add(*vectors: Vector2D) -> Vector2D:
    """
    将一个二维向量集合中的所有向量进行相加后返回结果

    Args:
        vectors (Iterable[Vector2D]): 向量集合

    Returns:
        Vector2D: 所有向量相加后的结果
    """
    x: Number
    y: Number

    x, y = 0, 0
    for v in vectors:
        x += v[0]
        y += v[1]

    return (x, y)


def translate(offset: Vector2D, vectors: Iterable[Vector2D]) -> List[Vector2D]:
    """
    移动一个向量集合中的每个向量

    最终, 向量组成的形态不变, 但向量的位置会发生变化

    Args:
        offset (Vector2D): 向量偏移量
        vectors (Iterable[Vector2D]): 向量集合

    Returns:
        List[Vector2D]: 移动位置后的向量集合
    """
    return [add(v, offset) for v in vectors]


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


def to_angle(radian: Number) -> Number:
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
        v (Vector2D): 笛卡尔坐标向量

    Returns:
        PolarVector: 极坐标向量
    """
    # 获取笛卡尔坐标向量的分量
    x, y = v[0], v[1]
    # 利用 atan2 函数, 根据笛卡尔坐标分量求弧度
    angle = atan2(y, x)
    # 利用 length 函数求向量的长度, 返回极坐标向量
    return (length(v), angle)
