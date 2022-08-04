from math import acos, atan2, cos, pi, sin, sqrt
from typing import Any, Callable, Iterable, List, TypeVar, cast

from . import Number, Polar, Triangle, Vector, Vector2D, Vector3D

# 定义泛型参数
T = TypeVar("T")
C = TypeVar("C")


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
    # 假设 vs = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    # 则 zip(*vs) 为 [(1, 4, 7), (2, 5, 8), (3, 6, 9)], 相当于将 vs 按列排列
    # map(sum, zip(*vs)) 相当于将每个 tuple 相加
    return tuple(map(sum, zip(*vs)))


def subtract(*vs: Vector) -> Vector:
    """
    将一个 N 维向量集合中所有的向量进行相减后返回结果

    Args:
        vs (Iterable[Vector]): 向量集合

    Returns:
        Vector: 所有向量相减后的结果
    """
    def sub(nums: Iterable[Number]) -> Number:
        it = iter(nums)

        r = next(it)
        while 1:
            try:
                r -= next(it)
            except StopIteration:
                return r

    return tuple(map(sub, zip(*vs)))


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


def to_cartesian(polar: Polar) -> Vector2D:
    """
    将极坐标向量转换为笛卡尔坐标

    Args:
        polar (Polar): 极坐标, 两个分量为 `(向量长度, 弧度)`

    Returns:
        Vector2D: 二维向量向量
    """
    # 获取极坐标向量分量
    length_, angle = polar[0], polar[1]

    # 通过余弦函数和正弦函数求笛卡尔 x, y 坐标
    return (length_ * cos(angle), length_ * sin(angle))


def to_polar(v: Vector2D) -> Polar:
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


def dot(u: Vector, v: Vector) -> float:
    """
    计算两个 N 维向量的点积

    Args:
        u (Vector): 向量 1
        v (Vector): 向量 2

    Returns:
        float: 向量点积
    """
    return sum([coord1 * coord2 for coord1, coord2 in zip(u, v)])


def distance(v1: Vector, v2: Vector) -> float:
    """
    计算两个向量坐标的距离

    Args:
        v1 (Vector): 向量 1
        v2 (Vector): 向量 2

    Returns:
        float: 向量的距离
    """
    return length(subtract(v1, v2))


def perimeter(vs: List[Vector]) -> float:
    """
    计算由向量围成的周长

    Args:
        vs (List[Vector]): 向量集合

    Returns:
        float: 周长
    """
    distances = [
        distance(vs[i], vs[(i + 1) % len(vs)])
        for i in range(len(vs))
    ]
    return sum(distances)


def cross(u: Vector3D, v: Vector3D) -> Vector3D:
    """
    计算三维向量的向量积

    这个公式不能很好地推广到其他维度. 它要求输入向量必须有三个分量

    Args:
        u (Vector3D): 三维向量 1
        v (Vector3D): 三维向量 2

    Returns:
        Vector3D: 两个三维向量的向量积
    """
    ux, uy, uz = u
    vx, vy, vz = v
    return (uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx)


def rotate2d(angle: float, v: Vector2D) -> Vector2D:
    l, a = to_polar(v)
    return to_cartesian((l, a + angle))


def angle_between(v1: Vector, v2: Vector) -> float:
    """
    计算两个向量的夹角

    Args:
        v1 (Vector): 向量 1
        v2 (Vector): 向量 2

    Returns:
        float: 向量的夹角弧度
    """
    return acos(min(1.0, dot(v1, v2) / (length(v1) * length(v2))))


def component(v: Vector, direction: Vector) -> float:
    """
    利用点积提取三维向量在给定方向上坐标轴的分量

    Args:
        v (Vector3D): 三维向量
        direction (Vector3D): 三维向量的方向, 为仅有一个维度为 `1` 的三维向量

    Returns:
        float: 三维向量在二维坐标指定方向的分量
    """
    return dot(v, direction) / length(direction)


def unit(v: Vector) -> Vector:
    """
    返回和输入向量方向相同, 但长度为 `1` 的向量

    Args:
        v (Vector): 输入向量

    Returns:
        Vector: 和输入向量方向一致, 但长度为 `1` 的向量
    """
    return scale(v, 1.0 / length(v))


def normal(face: Triangle) -> Vector3D:
    """
    计算一个三维面的法线 (垂直面的向量)

    Args:
        face (Triangle): 一个表示面的三角形

    Returns:
        Vector3D: 垂直三维平面的法向量
    """
    return cross(
        cast(Vector3D, subtract(face[1], face[0])),
        cast(Vector3D, subtract(face[2], face[0])),
    )


def compose(*fns: Callable[[T], T]) -> Callable[[T], T]:
    """
    将一系列向量处理组合在一起

    Returns:
        Callable[[T], T]: 返回组合处理函数
    """
    def fn(input: T) -> T:
        result = input

        # 依次执行处理函数
        for fn in reversed(fns):
            result = fn(result)

        return result

    return fn


def curry2(func: Callable[[T, C], Any]):
    """
    对一个具备两个参数的函数执行柯里化, 结果类似:

    ```
    g(x) = curry2(f(x, y))
    g(x)(y) == f(x, y)
    ```

    Args:
        func (Callable[[T, C], Any]): 返回包装第一个参数的函数
    """
    def fn_first(x: T) -> Callable[[C], Any]:
        def fn_second(y: C) -> Any:
            return func(x, y)

        return fn_second

    return fn_first


def linear_combination(scalars, *vectors):
    scaled = [scale(s, v) for s, v in zip(scalars, vectors)]
    return add(*scaled)
