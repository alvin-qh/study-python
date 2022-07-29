"""
绘制一个茶壶 3D 图形
"""

from math import pi
from os import path
from typing import List, cast

from transforms import rotate_x_by, scale_by, translate_by
from vectors import Vector, Vector3D

# 打开模型文件
with open(path.join(path.dirname(__file__), "teapot.off")) as f:
    lines = f.readlines()

# 读取模型文件的第一行, 包含了向量, 面和边的数量
vertex_count, face_count, edge_count = map(int, lines[1].split())


def triple(xs: map) -> Vector:
    """
    将一个 `map` 对象转为三维向量

    Args:
        xs (map): `map` 对象

    Returns:
        Vector3D: 三维向量
    """
    xss = list(xs)
    return (xss[0], xss[1], xss[2])


def load_vertices() -> List[Vector]:
    f_scale = scale_by(2)
    f_rotate = rotate_x_by(-pi / 2)
    f_translate = translate_by((-0.5, 0, -0.6))

    # 保存向量返回值
    vertices = []

    # 从第三行开始, 逐行读取模型文件内容
    for i in range(2, 2 + vertex_count):
        # 从读取的行中
        v = triple(map(float, lines[i].split()))

        vertices.append(f_scale(f_rotate(cast(Vector3D, f_translate(v)))))

    return vertices


def load_polygons():
    polys = []
    vertices = load_vertices()
    for i in range(2+vertex_count, 2+vertex_count+face_count):
        poly = list(map(vertices.__getitem__, map(int, lines[i].split()[1:])))
        polys.append(poly)
    return polys


def triangulate(poly):
    if len(poly) < 3:
        raise ValueError("polygons must have at least 3 vertices")

    for i in range(1, len(poly) - 1):
        yield (poly[0], poly[i+1], poly[i])


def load_triangles():
    tris = []
    polys = load_polygons()

    for poly in polys:
        for tri in triangulate(poly):
            assert(len(tri) == 3)

            for v in tri:
                assert(len(v) == 3)

            tris.append(tri)

    return tris
