from typing import Callable

from common import Vector3D
from vectors import Number, Vector, add, rotate2d, scale


def compose(*args):
    def new_function(input):
        result = input
        for f in reversed(args):
            result = f(result)

        return result

    return new_function


def curry2(f):
    def g(x):
        def new_function(y):
            return f(x, y)

        return new_function

    return g


def polygon_map(transformation, polygons):
    return [
        [transformation(vertex) for vertex in triangle]
        for triangle in polygons
    ]


def scale_by(scalar: Number) -> Callable[[Vector], Vector]:
    """
    将 `scale` 函数的 `scalar` 参数固化

    Args:
        scalar (Number): `scale` 函数的 `scalar` 参数

    Returns:
        Callable[[Vector], Vector]: 向量和指定标量相乘的结果
    """

    def fn(v: Vector) -> Vector:
        """
        返回的函数, 相当于 `scalar` 参数固定的 `scale` 函数

        Args:
            v (Vector): 相乘的向量

        Returns:
            Vector: 向量和指定标量相乘的结果
        """
        # 计算向量和标量相乘的结果
        return scale(v, scalar)

    # 返回 scalar 参数固化后的 scale 函数
    return fn


def translate_by(translation: Vector) -> Callable[[Vector], Vector]:
    """
    获取向量参数固化后的 `add` 函数

    Args:
        translation (Vector): 要固化的 `add` 函数向量参数

    Returns:
        Callable[[Vector], Vector]: 向量参数固化后的 `add` 函数
    """

    def fn(v: Vector) -> Vector:
        """
        向量参数固化后的 `add` 函数

        Args:
            v (Vector): 第二个向量参数

        Returns:
            Vector: 两个向量相加的结果
        """
        # 计算两个向量相加的结果
        return add(translation, v)

    # 向量参数固化后的 `add` 函数
    return fn


def rotate_z(angle, vector):
    x, y, z = vector
    new_x, new_y = rotate2d(angle, (x, y))
    return new_x, new_y, z


def rotate_z_by(angle):
    def new_function(v):
        return rotate_z(angle, v)

    return new_function


def rotate_x(angle: float, vector: Vector3D) -> Vector3D:
    x, y, z = vector
    # 将三维向量在 y 和 z 两个坐标分量旋转指定角度
    new_y, new_z = rotate2d(angle, (y, z))
    return (x, new_y, new_z)


def rotate_x_by(angle: float) -> Callable[[Vector], Vector]:
    """


    Args:
        angle (float): _description_

    Returns:
        Callable[[Vector], Vector]: _description_
    """

    def fn(v: Vector) -> Vector:
        """

        Args:
            v (Vector): _description_

        Returns:
            Vector: _description_
        """
        return rotate_x(angle, v)

    return fn


def rotate_y(angle, vector):
    x, y, z = vector
    new_x, new_z = rotate2d(angle, (x, z))
    return new_x, y, new_z


def rotate_y_by(angle):
    def new_function(v):
        return rotate_y(angle, v)

    return new_function


B = (
    (0, 2, 1),
    (0, 1, 0),
    (1, 0, -1)
)

v = (1, -2, -2)


def transform_standard_basis(transform):
    return transform((1, 0, 0)), transform((0, 1, 0)), transform((0, 0, 1))
