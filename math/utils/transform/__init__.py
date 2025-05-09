from typing import Any, Callable, Iterable, List, Sequence, Tuple

from utils.types import Number, Triangle, Vector2D, Vector3D
from utils.vector import add, as_polygons, as_vector3d, scale, to_cartesian, to_polar


def compose[T](*fns: Callable[[T], T]) -> Callable[[T], T]:
    """将一系列向量处理组合在一起

    Returns:
        Callable[[T], T]: 返回组合处理函数
    """

    def fn(input_: T) -> T:
        result = input_

        # 依次执行处理函数
        for fn in reversed(fns):
            result = fn(result)

        return result

    return fn


def curry2[T, C](func: Callable[[T, C], Any]) -> Callable[..., Callable[[C], Any]]:
    """对一个具备两个参数的函数执行柯里化

    结果类似:

    ```python
    g(x) = curry2(f(x, y))
    g(x)(y) == f(x, y)
    ```

    Args:
        `func` (`Callable[[T, C], Any]`): 返回包装第一个参数的函数
    """

    def fn_first(x: T) -> Callable[[C], Any]:
        """第一层函数

        接受第一个参数, 返回第二个函数

        Args:
            `x` (`T`): 第一个参数

        Returns:
            `Callable[[C], Any]`: 返回第二个函数
        """

        def fn_second(y: C) -> Any:
            """第二层函数

            接收第二个参数, 执行原始的 `f(x, y)` 函数

            Args:
                y (C): 第二个参数

            Returns:
                Any: 返回结果
            """
            return func(x, y)

        return fn_second

    return fn_first


def polygon_map(
    transformer: Callable[[Vector3D], Vector3D],
    polygons: Sequence[Triangle],
) -> List[Triangle]:
    """对多边形中的每个向量进行变换

    多边形由三角形组成, 三角形由三个三维向量组成

    该方法将组成多边形的每个向量进行变化, 返回向量集合

    Args:
        `transformer` (`Callable[[Vector3D], Vector3D]`): 变换函数
        `polygons` (`Sequence[Triangle]`): 要变换的多边形

    Returns:
        `Sequence[Triangle]`: 变换后的三维向量集合
    """
    # 遍历每个三角形的三个三维向量, 进行线性变换
    return as_polygons([transformer(v) for v in triangle] for triangle in polygons)


# 假设线性变换 T 作用在标准基向量的结果为 (1, 1, 1), (1, 0, -1), (0, 1, 1)
Te1, Te2, Te3 = (1, 1, 1), (1, 0, -1), (0, 1, 1)


def apply(v: Vector3D) -> Vector3D:
    """应用线性变换 T

    由于线性变换 T 未知, 但线性变换应用于标准基向量的接过已知, 根据线性组合, 可以将标准基向量的线性变换
    应用到任意向量上, 即:

    设标准基向量为 `e1=(1, 0, 0)`, `e2=(0, 1, 0)`, `e3=(0, 0, 1)`

    由于 `v = v0*e1 + v1*e2 + v2*e3`, 所以:
    `T(v) = T(v0*e1) + T(v0*e2) + T(v1*e3) = v0*Te0 + v1*Te1 + v2*Te2`

    而 `Te0`, `Te1` 和 `Te2` 已知, 所以 `T(v)` 可求得

    Args:
        `v` (`Vector3D`): 输入三维向量

    Returns:
        `Vector3D`: 应用线性变换后的三维向量
    """
    # 通过标准基向量的线性变换结果, 计算给定向量的线性变换
    return as_vector3d(
        add(
            scale(v[0], Te1),
            scale(v[1], Te2),
            scale(v[2], Te3),
        )
    )


def triangulate(vs: Sequence[Vector3D]) -> Iterable[Triangle]:
    """将一个三维向量序列转为三角形序列集合

    参数为一个三维向量序列, 可包括 N 个向量, 返回 M 个三角形, `vs` 参数包括最少 3 个向量, 否则无法组成三角形

    ```
            * (0)
    * (1)
                * (2)
            * (3)
    ```

    Args:
        `vs` (`Sequence[Vector3D]`): 一组由四个三维向量组成的集合

    Yields:
        `Iterable[Triangle]`: 返回一个生成器, 产生相关的两个三角形向量集合
    """
    # 将四个向量坐标拆分成两个三角形

    # 连接 0-2-1 和 0-3-2, 将一个四边形分为两个三角形
    for i in range(1, len(vs) - 1):
        yield (vs[0], vs[i + 1], vs[i])


def rotate2d(angle: Number, v: Vector2D) -> Vector2D:
    """将一个二维向量旋转指定弧度

    Args:
        `angle` (`Number`): 要旋转的弧度
        `v` (`Vector2D`): 要旋转的二维向量

    Returns:
        `Vector2D`: 旋转角度后的新向量
    """
    # 将向量转为极坐标
    l, a = to_polar(v)

    # 将极坐标的角度分量增加指定弧度后转为笛卡尔坐标向量
    return to_cartesian((l, a + angle))


def rotate_x(angle: Number, v: Vector3D) -> Vector3D:
    """将三维向量围绕 x 轴进行旋转

    Args:
        `angle` (`Number`): 要旋转的弧度
        `vector` (`Vector3D`): 要旋转的三维向量

    Returns:
        `Vector3D`: 旋转后的三维向量
    """
    # 获取三维分量
    x, y, z = v

    # 将三维向量在 y 和 z 两个坐标分量旋转指定角度
    new_y, new_z = rotate2d(angle, (y, z))

    # 返回旋转后的坐标
    return (x, new_y, new_z)


def rotate_y(angle: Number, v: Vector3D) -> Vector3D:
    """将三维向量围绕 y 轴进行旋转

    Args:
        `angle` (`Number`): 要旋转的弧度
        `vector` (`Vector3D`): 要旋转的三维向量

    Returns:
        Vector3D: 旋转角度后的三维向量
    """
    # 获取三维分量
    x, y, z = v

    # 将三维向量在 x 和 z 两个坐标分量旋转指定角度
    new_x, new_z = rotate2d(angle, (x, z))

    # 返回旋转后的坐标
    return new_x, y, new_z


def rotate_z(angle: Number, v: Vector3D) -> Vector3D:
    """将三维向量围绕 z 轴进行旋转

    Args:
        `angle` (`Number`): 要旋转的弧度
        `v` (`Vector3D`): 要旋转的三维向量

    Returns:
        `Vector3D`: 旋转后的三维向量
    """
    # 获取三维分量
    x, y, z = v

    # z 轴不变, 旋转 x, y 坐标
    new_x, new_y = rotate2d(angle, (x, y))

    # 返回旋转后的坐标
    return new_x, new_y, z


def stretch(v: Vector3D, sx: float = 1.0, sy: float = 1.0, sz: float = 1.0) -> Vector3D:
    """拉伸一个向量

    Args:
        `v` (`Vector3D`): 要拉伸的三维向量
        `sx` (`float`, optional): `x` 轴拉伸倍数. Defaults to `1.0`.
        `sy` (`float`, optional): `y` 轴拉伸倍数. Defaults to `1.0`.
        `sz` (`float`, optional): `z` 轴拉伸倍数. Defaults to `1.0`.

    Returns:
        `Vector3D`: 拉伸后的向量
    """
    x, y, z = v
    return (x * sx, y * sy, z * sz)


def cube_stretch(
    v: Vector3D,
    dim: Tuple[Number, Number, Number] = (1, 1, 1),
) -> Vector3D:
    """三次方拉伸一个向量, 即拉伸向量指定维度的三次方

    Args:
        `v` (`Vector3D`): 要拉伸的三维向量
        `dim` (`Vector3D`, optional): 要拉伸的纬度. Defaults to `(1, 1, 1)`.

    Returns:
        `Vector3D`: 拉伸后的三维向量
    """
    return stretch(
        v,
        sx=v[0] ** 2 if dim[0] else 1.0,
        sy=v[1] ** 2 if dim[1] else 1.0,
        sz=v[2] ** 2 if dim[2] else 1.0,
    )
