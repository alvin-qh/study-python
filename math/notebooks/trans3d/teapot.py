"""
绘制一个茶壶 3D 图形
"""

from functools import partial
from math import pi
from os import path
from typing import Generator, List, Sequence, cast

from transforms import rotate_x
from vectors import Polygons, Triangle, Vector3D, add, scale

# 打开模型文件
with open(path.join(path.dirname(__file__), "models/teapot.off")) as f:
    lines = f.readlines()

# 读取模型文件的第一行, 包含了向量, 面和边的数量
# 前 vertex_count 行保存向量, 格式为: x y z
# 前 vertex_count ~ face_count 行保存面 (三角形), 格式为: 4 向量1行数 向量2行数 向量3行数
vertex_count, face_count, edge_count = map(int, lines[1].split())


def triple(xs: map) -> Vector3D:
    """
    将一个 `map` 对象转为三维向量

    Args:
        xs (map): `map` 对象

    Returns:
        Vector3D: 三维向量
    """
    xss = list(xs)
    return (xss[0], xss[1], xss[2])


def load_vertices() -> List[Vector3D]:
    """
    读取模型中的向量

    `teapot.off` 文件的每一行为一个三维向量

    Returns:
        List[Vector]: 读取的结果
    """
    # 获取将向量放大两倍的函数
    scale_by = partial(scale, scalar=2)
    # 获取将向量沿 y 轴顺时针转动 90° 的函数
    rotate_x_by = partial(rotate_x, angle=-pi / 2)
    # 将向量的 x 轴和 z 轴移动一段距离的函数
    translate_by = partial(add, (-0.5, 0, -0.6))

    # 保存向量返回值
    vs = []

    # 从第三行开始, 逐行读取模型文件内容
    for i in range(2, 2 + vertex_count):
        # 从读取的行中获取一个三维向量
        v: Vector3D = triple(map(float, lines[i].split()))

        # 对向量进行移动
        v = cast(Vector3D, translate_by(v))
        # 对向量转动 90°
        v = rotate_x_by(v=v)
        # 将向量长度放大 2 被
        v = cast(Vector3D, scale_by(v=v))

        vs.append(v)

    return vs


def load_polygons() -> Sequence[Sequence[Vector3D]]:
    """
    读取组成多面体的向量集合

    Returns:
        Sequence[Sequence[Vector3D]]: 向量集合, 每组向量由 `4` 个三维向量组成
    """
    # 读取模型向量
    vertices = load_vertices()

    # 保存多边形结果的
    polys = []

    # 获取所有的平面定义行
    for i in range(2 + vertex_count, 2 + vertex_count + face_count):
        cols = lines[i].split()

        # 每行数据格式为 4 324 306 304 317, 表示对应 324, 306, 304, 317 这几行数据表示的向量
        # 即读取由四个向量组成的集合
        poly = cast(
            Triangle,
            tuple(map(vertices.__getitem__, map(int, cols[1:]))),
        )
        polys.append(poly)

    return polys


def triangulate(poly: Sequence[Vector3D]) -> Generator[Triangle, None, None]:
    """
    将传入的四个三维向量组合成两个三角形

    Args:
        poly (Sequence[Vector3D]): 一组由四个三维向量组成的集合

    Yields:
        Generator[Triangle, None, None]: 返回一个生成器, 产生相关的两个三角形向量集合 
    """
    # 确认每个多面体都有三个向量组成
    if len(poly) < 3:
        raise ValueError("polygons must have at least 3 vertices")

    # 将四个向量坐标拆分成两个三角形
    #             * (0)
    #       * (1)
    #                   * (2)
    #               * (3)
    # 连接 0-2-1 和 0-3-2, 将一个四边形分为两个三角形
    for i in range(1, len(poly) - 1):
        yield (poly[0], poly[i + 1], poly[i])


def load_triangles() -> Polygons:
    """
    读取所有的多面体的组成向量集合

    Returns:
        Polygons: 多面体的组成向量集合
    """
    # 读取所有的多面体向量
    return [tri for poly in load_polygons() for tri in triangulate(poly)]
