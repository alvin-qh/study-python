"""绘制一个茶壶 3D 图形"""

from functools import partial
from math import pi
from os import path
from typing import Iterable, List

from common.transform import rotate_x, triangulate
from common.typedef import Triangle, Vector3D
from common.vector import add, as_vector3d, scale

# 打开模型文件
with open(path.join(path.dirname(__file__), "models/teapot.off")) as f:
    lines = f.readlines()

# 读取模型文件的第一行, 包含了向量, 面和边的数量
# 前 `vertex_count` 行保存向量, 格式为: x y z
# 前 `vertex_count~face_count` 行保存面 (三角形), 格式为: 4 向量1行数 向量2行数 向量3行数
vertex_count, face_count, edge_count = map(int, lines[1].split())


def load_vertices() -> List[Vector3D]:
    """读取模型中的向量

    `teapot.off` 文件的每一行为一个三维向量

    Returns:
        `List[Vector3D]`: 读取的结果
    """
    # 获取将向量放大两倍的函数
    scale_by = partial(scale, 2)

    # 获取将向量沿 y 轴顺时针转动 90° 的函数
    rotate_x_by = partial(rotate_x, -pi / 2)

    # 将向量的 x 轴和 z 轴移动一段距离的函数
    translate_by = partial(add, (-0.5, 0, -0.6))

    # 保存向量返回值
    vs = []

    # 从第三行开始, 逐行读取模型文件内容
    for i in range(2, 2 + vertex_count):
        # 从读取的行中获取一个三维向量
        v = tuple(list(map(float, lines[i].split())))

        # 对向量进行移动
        v = as_vector3d(translate_by(v))  # type: ignore
        # 对向量转动 90°
        v = rotate_x_by(v)
        # 将向量长度放大 2 被
        v = as_vector3d(scale_by(v))

        vs.append(v)

    return vs


def load_triangles() -> Iterable[List[Vector3D]]:
    """读取组成多面体的三角形向量集合

    三角形以每两个组成一个四边形的形式表示

    Returns:
        `Polygons`: 向量集合, 每组向量由 `4` 个三维向量组成
    """
    # 读取模型向量
    vertices = load_vertices()

    # 获取所有的平面定义行
    for i in range(2 + vertex_count, 2 + vertex_count + face_count):
        cols = lines[i].split()

        # 每行数据格式为 4 324 306 304 317, 表示对应 324, 306, 304, 317 这几行数据表示的向量
        # 即读取由四个向量组成的集合, 组成了空间中的一个四边形 (由两个三角形组成)
        yield list(map(vertices.__getitem__, map(int, cols[1:])))


def load_model() -> List[Triangle]:
    """读取所有的多面体的组成向量集合

    Returns:
        `Polygons`: 多面体的组成向量集合
    """
    # 读取所有的多面体向量
    return [tri for quad in load_triangles() for tri in triangulate(quad)]
