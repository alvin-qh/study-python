import math
from typing import Iterable, List, Sequence, TypeVar, cast

from utils.types import (
    Matrix,
    Matrix3D,
    Number,
    Polar,
    Triangle,
    Vector,
    Vector2D,
    Vector3D,
)


def as_vector2d(v: Iterable[Number]) -> Vector2D:
    """将数值序列的前两个值转为二维向量值

    Args:
        `v` (`Iterable[Number]`): 数值序列

    Returns:
        `Vector2D`: 二维向量值
    """
    iv = iter(v)
    return (next(iv), next(iv))


def as_vector3d(v: Iterable[Number]) -> Vector3D:
    """将数值序列的前三个值转为三维向量值

    Args:
        `v` (`Iterable[Number]`): 数值序列

    Returns:
        `Vector3D`: 三维向量值
    """
    iv = iter(v)
    return (next(iv), next(iv), next(iv))


def as_vector(v: Iterable[Number]) -> Vector:
    """将数值序列的前 N 个值转为 N 维向量值

    Args:
        `v` (`Iterable[Number]`): 数值序列

    Returns:
        `Vector`: N 维向量值
    """
    return v if isinstance(v, tuple) else tuple(v)


def as_triangle(t: Iterable[Iterable[Number]]) -> Triangle:
    """将三维向量序列的前三项转为三角形值

    在 3D 绘图技术中, 一个三角形表示一个面 (Face), 一个三维图像是由若干个三角形组合而成

    Args:
        `t` (`Iterable[Iterable[Number]]`): 三维向量序列

    Returns:
        `Triangle`: 三角形值
    """
    it = iter(t)
    return (
        as_vector3d(next(it)),
        as_vector3d(next(it)),
        as_vector3d(next(it)),
    )


def as_matrix3d(t: Iterable[Iterable[Number]]) -> Matrix3D:
    """将三维向量序列转为三维矩阵值

    Args:
        `t` (`Iterable[Iterable[Number]]`): 三维向量序列

    Returns:
        `Triangle`: 三维矩阵值
    """
    return [as_vector3d(v) for v in t]


def as_matrix(t: Iterable[Iterable[Number]]) -> Matrix:
    """将 N 维矩阵序列转为 N 维矩阵值

    Args:
        `t` (`Iterable[Iterable[Number]]`): N 维向量序列

    Returns:
        `Triangle`: N 维矩阵值
    """
    it = iter(t)
    v1 = as_vector(next(it))

    d = len(v1)

    def as_n_vector(ns: Iterable[Number]) -> Vector:
        v = as_vector(ns)
        if len(v) != d:
            raise ValueError(f"Invalid vector length {len(v)}")

        return v

    return [v1, *(as_n_vector(ns) for ns in it)]


def as_polygons(p: Iterable[Iterable[Iterable[Number]]]) -> List[Triangle]:
    """将向量序列的序列转为三角形序列 (即一个多面体)

    若干个三角形组成一个多面体 (Polygon), 即一个三维图形

    Args:
        `p` (`Iterable[Iterable[Iterable[Number]]]`): 向量序列的序列

    Returns:
        `List[Triangle]`: 三角形集合, 表示一个多面体
    """
    return [as_triangle(t) for t in p]


VT = TypeVar("VT", Vector, Vector2D, Vector3D)


def vertices(polygon: Iterable[Iterable[VT]]) -> List[VT]:
    """从一个多面体中获取不重复的向量集合

    Args:
        `polygon` (`Iterable[Iterable[VT]]`): 多面体

    Returns:
        `Vector`: 向量点坐标
    """
    return list({v for face in polygon for v in face})


def length(v: VT) -> float:
    """计算一个 N 维向量的长度

    Args:
        `v` (`Vector`): 一个 N 维向量

    Returns:
        `float`: 向量长度
    """
    return math.sqrt(sum(coord**2 for coord in v))


def add(*vs: VT) -> VT:
    """将一个 N 维向量集合中的所有向量进行相加后返回结果

    Args:
        `vs` (`Iterable[VT]`): 向量集合

    Returns:
        `VT`: 所有向量相加后的结果
    """
    # 假设 vs = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    # 则 zip(*vs) 为 [(1, 4, 7), (2, 5, 8), (3, 6, 9)], 相当于将 vs 按列排列
    # map(sum, zip(*vs)) 相当于将每个 tuple 相加
    return cast(VT, tuple(map(sum, zip(*vs))))


def subtract(*vs: VT) -> VT:
    """将一个 N 维向量集合中所有的向量进行相减后返回结果

    Args:
        `vs` (`Iterable[VT]`): 向量集合

    Returns:
        `VT`: 所有向量相减后的结果
    """

    def sub(nums: Iterable[Number]) -> Number:
        it = iter(nums)

        r = next(it)
        while 1:
            try:
                r -= next(it)
            except StopIteration:
                break

        return r

    # 假设 vs = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    # 则 zip(*vs) 为 [(1, 4, 7), (2, 5, 8), (3, 6, 9)], 相当于将 vs 按列排列
    # map(sum, zip(*vs)) 相当于将每个 tuple 相减
    return cast(VT, tuple(map(sub, zip(*vs))))


def translate(v_off: VT, vs: Iterable[VT]) -> List[VT]:
    """移动一个向量集合中的每个向量

    最终, 向量组成的形态不变, 但向量的位置会发生变化

    Args:
        `v_off` (`VT`): 向量偏移量
        `vs` (`Iterable[VT]`): 向量集合

    Returns:
        `List[VT]`: 移动位置后的向量集合
    """
    return [add(v, v_off) for v in vs]


# 定义 1° 角度对应的弧度
ONE_DEGREE = math.pi / 180


def to_radian(angle: Number) -> Number:
    """将角度转换为弧度

    Args:
        `angle` (`Number`): 角度

    Returns:
        `Number`: 对应的弧度
    """
    return angle * ONE_DEGREE


# 定义 1 弧度对应的角度
ONE_RAD = 180 / math.pi


def to_degree(radian: Number) -> Number:
    """将弧度转换为角度

    Args:
        `radian` (`Number`): 弧度

    Returns:
        `Number`: 对应的角度
    """
    return radian * ONE_RAD


def to_cartesian(polar: Polar) -> Vector2D:
    """将极坐标向量转换为笛卡尔坐标

    Args:
        `polar` (`Polar`): 极坐标, 两个分量为 `(向量长度, 弧度)`

    Returns:
        `Vector2D`: 二维向量向量
    """
    # 获取极坐标向量分量
    length_, angle = polar[0], polar[1]

    # 通过余弦函数和正弦函数求笛卡尔 x, y 坐标
    return (length_ * math.cos(angle), length_ * math.sin(angle))


def to_polar(v: Vector2D) -> Polar:
    """将笛卡尔坐标向量转换为极坐标向量

    Args:
        `v` (`Vector2D`): 二维向量的笛卡尔坐标

    Returns:
        `Polar`: 二维向量的极坐标
    """
    # 获取笛卡尔坐标向量的分量
    x, y = v[0], v[1]

    # 利用 atan2 函数, 根据笛卡尔坐标分量求弧度
    angle = math.atan2(y, x)

    # 利用 length 函数求向量的长度, 返回极坐标向量
    return (length(v), angle)


def scale(scalar: Number, v: VT) -> VT:
    """二维向量和标量相乘

    Args:
        `scalar` (`Number`): 乘数, 即向量的放大倍数
        `v` (`VT`): N 维向量

    Returns:
        `VT`: 缩放后的向量
    """
    return cast(VT, tuple(coord * scalar for coord in v))


def dot(u: VT, v: VT) -> float:
    """计算两个 N 维向量的点积

    Args:
        `u` (`VT`): 向量 1
        `v` (`VT`): 向量 2

    Returns:
        `float`: 向量点积
    """
    return sum([coord1 * coord2 for coord1, coord2 in zip(u, v)])


def distance(v1: VT, v2: VT) -> float:
    """计算两个向量坐标的距离

    Args:
        `v1` (`Vector`): 向量 1
        `v2` (`Vector`): 向量 2

    Returns:
        `float`: 向量的距离
    """
    return length(subtract(v1, v2))


def perimeter(vs: Sequence[VT]) -> float:
    """计算由向量围成的周长

    Args:
        `vs` (`Sequence[Vector]`): 向量集合

    Returns:
        `float`: 周长
    """
    distances = [distance(vs[i], vs[(i + 1) % len(vs)]) for i in range(len(vs))]
    return sum(distances)


def cross(u: Vector3D, v: Vector3D) -> Vector3D:
    """计算三维向量的向量积

    这个公式不能很好地推广到其他维度. 它要求输入向量必须有三个分量

    Args:
        `u` (`Vector3D`): 三维向量 1
        `v` (`Vector3D`): 三维向量 2

    Returns:
        `Vector3D`: 两个三维向量的向量积
    """
    ux, uy, uz = u
    vx, vy, vz = v
    return (uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx)


def angle_between(v1: VT, v2: VT) -> float:
    """计算两个向量的夹角

    Args:
        `v1` (`VT`): 向量 1
        `v2` (`VT`): 向量 2

    Returns:
        `float`: 向量的夹角弧度
    """
    return math.acos(min(1.0, dot(v1, v2) / (length(v1) * length(v2))))


def component(v: VT, direction: VT) -> float:
    """利用点积提取三维向量在给定方向上坐标轴的分量

    Args:
        `v` (`VT`): 三维向量
        `direction` (`VT`): 三维向量的方向, 为仅有一个维度为 `1` 的三维向量

    Returns:
        `float`: 三维向量在二维坐标指定方向的分量
    """
    return dot(v, direction) / length(direction)


def to_2d_projection(v: Vector3D) -> Vector2D:
    """计算三维向量在二维平面的投影

    Args:
        `v` (`Vector3D`): 三维向量

    Returns:
        `Vector2D`: 三维向量在二维平面的投影
    """
    # 将三维坐标转化为二维坐标 x 和 y 轴的分量, 即组成三维坐标在二维坐标的投影
    return (component(v, (1, 0, 0)), component(v, (0, 1, 0)))


def unit(v: VT) -> VT:
    """
    返回和输入向量方向相同, 但长度为 `1` 的向量

    Args:
        v (VT): 输入向量

    Returns:
        VT: 和输入向量方向一致, 但长度为 `1` 的向量
    """
    return scale(1.0 / length(v), v)


def normal(face: Triangle) -> Vector3D:
    """计算一个三维面的法向量 (垂直面的向量)

    Args:
        `face` (`Triangle`): 一个表示面的三角形

    Returns:
        `Vector3D`: 垂直三维平面的法向量
    """
    return cross(
        as_vector3d(subtract(face[1], face[0])),
        as_vector3d(subtract(face[2], face[0])),
    )


def linear_combination(
    scalars: Sequence[Number],
    vectors: Sequence[VT],
) -> VT:
    """线性组合

    将多个向量放大后相加

    Args:
        `vectors` (`Sequence[VT]`): 向量集合
        `scalars` (`Sequence[Number]`): 每个向量的放大系数

    Returns:
        `VT`: 组合后的向量
    """
    scaled = [scale(s, v) for v, s in zip(vectors, scalars)]
    return add(*scaled)


def multiply_matrix_vector(
    matrix: Matrix,
    vector: Vector,
) -> Vector:
    """计算一个矩阵和一系列向量的乘积

    Args:
        `matrix` (`Matrix`): 矩阵
        `vector` (`Sequence[VT]`): 向量集合

    Returns:
        `VT`: 矩阵和向量集合的乘积结果
    """
    return linear_combination(vector, [as_vector(v) for v in matrix])
