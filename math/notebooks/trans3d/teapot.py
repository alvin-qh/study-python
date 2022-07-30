"""
绘制一个茶壶 3D 图形
"""

from math import pi
from os import path
from typing import Generator, List, cast

from transforms import rotate_x_by, scale_by, translate_by
from vectors import Polygons, Triangle, Vector3D

# 打开模型文件
with open(path.join(path.dirname(__file__), "teapot.off")) as f:
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
    f_scale = scale_by(2)
    # 获取将向量沿 y 轴顺时针转动 90° 的函数
    f_rotate = rotate_x_by(-pi / 2)
    # 将向量的 x 轴和 z 轴移动一段距离的函数
    f_translate = translate_by((-0.5, 0, -0.6))

    # 保存向量返回值
    vs = []

    # 从第三行开始, 逐行读取模型文件内容
    for i in range(2, 2 + vertex_count):
        # 从读取的行中获取一个三维向量
        v: Vector3D = triple(map(float, lines[i].split()))

        # 对向量进行移动
        v = cast(Vector3D, f_translate(v))
        # 对向量转动 90°
        v = f_rotate(v)
        # 将向量长度放大 2 被
        v = cast(Vector3D, f_scale(v))

        vs.append(v)

    return vs


def load_polygons() -> Polygons:
    """
    读取多面体数据

    Returns:
        Polygons: 多面体集合
    """
    # 读取模型向量
    vertices = load_vertices()

    # 保存多边形结果的
    polys = []

    # 获取所有的平面定义行
    for i in range(2 + vertex_count, 2 + vertex_count + face_count):
        cols = lines[i].split()

        # 将平面对应的三行定义数据取出, 转为向量后组成三角形
        poly = cast(
            Triangle,
            tuple(map(vertices.__getitem__, map(int, cols[1:]))),
        )
        polys.append(poly)

    return polys


def triangulate(poly: Triangle) -> Generator[Triangle, None, None]:
    """_summary_

    Args:
        poly (_type_): _description_

    Raises:
        ValueError: _description_

    Yields:
        _type_: _description_
    """
    if len(poly) < 3:
        raise ValueError("polygons must have at least 3 vertices")

    for i in range(1, len(poly) - 1):
        yield (poly[0], poly[i + 1], poly[i])


def load_triangles() -> Polygons:
    polys = load_polygons()

    tris = []

    for poly in polys:
        for tri in triangulate(poly):
            tris.append(tri)

    return tris
