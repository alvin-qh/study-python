from typing import Callable, Tuple

from vectors import Face, Number, Vector, Vector3D, add, rotate2d, scale


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


def polygon_map(transformation, polygons: Tuple[Face]):
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
    return lambda v: scale(v, scalar)


def translate_by(translation: Vector) -> Callable[[Vector], Vector]:
    """
    获取向量参数固化后的 `add` 函数

    Args:
        translation (Vector): 要固化的 `add` 函数向量参数

    Returns:
        Callable[[Vector], Vector]: 向量参数固化后的 `add` 函数
    """
    # 向量参数固化后的 `add` 函数
    return lambda v: add(translation, v)


def rotate_z(angle: float, vector: Vector3D) -> Vector3D:
    """
    将三维向量围绕 `z` 轴进行旋转

    Args:
        angle (float): 旋转角度
        vector (Vector3D): 要选择的三维向量

    Returns:
        Vector3D: 旋转角度后的三维向量
    """
    # 获取三维分量
    x, y, z = vector
    # z 轴不变, 旋转 x, y 坐标
    new_x, new_y = rotate2d(angle, (x, y))
    # 返回旋转后的坐标
    return new_x, new_y, z


def rotate_z_by(angle: float) -> Callable[[Vector3D], Vector3D]:
    """
    将 `rotate_z` 函数的 `angle` 参数进行固化

    Args:
        angle (float): 要固化的 `angle` 参数

    Returns:
        Callable[[Vector3D], Vector3D]: 固化 `angle` 参数的 `rotate_z` 函数
    """
    return lambda v: rotate_z(angle, v)


def rotate_x(angle: float, vector: Vector3D) -> Vector3D:
    """
    将三维向量围绕 `x` 轴进行旋转

    Args:
        angle (float): 旋转角度
        vector (Vector3D): 要选择的三维向量

    Returns:
        Vector3D: 旋转角度后的三维向量
    """
    # 获取三维分量
    x, y, z = vector
    # 将三维向量在 y 和 z 两个坐标分量旋转指定角度
    new_y, new_z = rotate2d(angle, (y, z))
    # 返回旋转后的坐标
    return (x, new_y, new_z)


def rotate_x_by(angle: float) -> Callable[[Vector3D], Vector3D]:
    """
    将 `rotate_x` 函数的 `angle` 参数进行固化

    Args:
        angle (float): 要固化的 `angle` 参数 

    Returns:
        Callable[[Vector], Vector]: 固化 `angle` 参数的 `rotate_x` 函数
    """
    return lambda v: rotate_x(angle, v)


def rotate_y(angle: float, vector: Vector3D) -> Vector3D:
    """
    将三维向量围绕 `y` 轴进行旋转

    Args:
        angle (float): 旋转角度
        vector (Vector3D): 要选择的三维向量

    Returns:
        Vector3D: 旋转角度后的三维向量
    """
    # 获取三维分量
    x, y, z = vector
    # 将三维向量在 x 和 z 两个坐标分量旋转指定角度
    new_x, new_z = rotate2d(angle, (x, z))
    # 返回旋转后的坐标
    return new_x, y, new_z


def rotate_y_by(angle: float) -> Callable[[Vector3D], Vector3D]:
    """
    将 `rotate_y` 函数的 `angle` 参数进行固化

    Args:
        angle (float): 要固化的 `angle` 参数

    Returns:
        Vector3D: 固化 `angle` 参数的 `rotate_y` 函数
    """
    return lambda v: rotate_y(angle, v)


B = (
    (0, 2, 1),
    (0, 1, 0),
    (1, 0, -1)
)

v = (1, -2, -2)


def transform_standard_basis(transform):
    return transform((1, 0, 0)), transform((0, 1, 0)), transform((0, 0, 1))


def linear_combination(scalars, *vectors):
    scaled = [scale(s, v) for s, v in zip(scalars, vectors)]
    return add(*scaled)


def multiply_matrix_vector(matrix, vector):
    return linear_combination(vector, *zip(*matrix))
