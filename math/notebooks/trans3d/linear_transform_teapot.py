####################################################################
# this code takes a snapshot to reproduce the exact figure
# shown in the book as an image saved in the "figs" directory
# to run it, run this script with command line arg --snapshot

import sys
from typing import Callable, cast

import camera
from draw_model import draw_model
from teapot import load_triangles
from vectors import Polygons, Vector3D, add, scale

if "--snapshot" in sys.argv:
    camera.default_camera = camera.Camera("fig4.35_linear_transform", [0])


def polygon_map(trans: Callable[[Vector3D], Vector3D], polygons: Polygons) -> Polygons:
    """
    对一组多边形应用线性变换

    Args:
        trans (Callable[[Vector3D], Vector3D]): 线性变换函数
        polygons (Polygons): 输入的多边形集合

    Returns:
        Polygons: 完成线性变换的多边形集合
    """
    return cast(
        Polygons,
        [
            # 遍历每个三角形的三个三维向量, 进行线性变换
            tuple([trans(vertex) for vertex in triangle])
            for triangle in polygons  # 遍历多边形集合的每个三角形
        ],
    )


# 假设线性变换 T 作用在标准基向量的结果为 (1, 1, 1), (1, 0, -1), (0, 1, 1)
Te1, Te2, Te3 = (1, 1, 1), (1, 0, -1), (0, 1, 1)


def apply(v: Vector3D) -> Vector3D:
    """
    应用线性变换 T

    由于线性变换 T 未知, 但线性变换应用于标准基向量的接过已知, 根据线性组合, 可以将标准基向量的线性变换
    应用到任意向量上, 即:

    设标准基向量为 e1=(1, 0, 0), e2=(0, 1, 0), e3=(0, 0, 1)

    由于 v = v0*e1 + v1*e2 + v2*e3, 所以:
    T(v) = T(v0*e1) + T(v0*e2) + T(v1*e3) = v0*Te0 + v1*Te1 + v2*Te2

    而 Te0, Te1 和 Te2 已知, 所以 T(v) 可求得

    Args:
        v (Vector3D): 输入三维向量

    Returns:
        Vector3D: 应用线性变换后的三维向量
    """
    return cast(
        Vector3D,
        add(  # 通过标准基向量的线性变换结果, 计算给定向量的线性变换
            scale(Te1, v[0]),
            scale(Te2, v[1]),
            scale(Te3, v[2]),
        )
    )


# 绘制茶壶模型
draw_model(polygon_map(apply, load_triangles()))
