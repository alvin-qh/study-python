from turtle import color
from typing import Any, List, TypeVar

import matplotlib.pyplot as plt
import numpy as np

T = TypeVar("T")


def expand_list(l: List[T], size: int) -> List[T]:
    """
    把列表集合扩展到指定的长度

    Args:
        l (List[T]): 列表集合对象
        size (int): 指定的长度

    Returns:
        List[T]: 长度扩展到 `size` 后的集合
    """
    while len(l) < size:
        l *= 2

    return l[:size]


def test_draw_bar() -> None:
    """
    绘制 3D 柱状图

    3D 柱状图由 6 组向量集合组成, 前三组 (`x`, `y` 和 `z`) 分别表示柱状图在三维空间中三个坐标轴的位置,
    后三组 (`dx`, `dy` 和 `dz`) 表示柱状图在三维空间的尺寸, 分别表示柱状图的长宽高

    另外, 可以定义 `color` 参数表示颜色, 可以为一个值 (所有柱状图的颜色), 或和柱状图数量一致
    (即和 `x`, `y` 或 `z` 集合长度一致)
    """
    # 获取 Figure 对象
    fig = plt.figure()

    # 创建三维坐标
    ax = fig.add_subplot(111, projection='3d')
    # 设置标题
    ax.set_title("3D Bar with Shade")

    # 设置柱在三维空间中的点
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    y = np.array([5, 6, 7, 8, 2, 5, 6, 3, 7, 2])
    z = np.zeros(10)

    # 设置柱的宽度
    dx = dy = 1
    # 设置柱的高度
    dz = x + y

    # 颜色列表, 扩展到长度为 10 的集合
    colors = expand_list([
        "blue",
        "cornflowerblue",
        "mediumturquoise",
        "goldenrod",
        "yellow",
    ], 10)

    # 绘制柱状图
    ax.bar3d(  # type: ignore
        x, y, z,  # 柱在三维空间的坐标
        dx, dy, dz,  # 柱在三维空间的尺寸, 长宽高
        color=colors,  # 柱的颜色
        edgecolor="k",  # 描边颜色
        shade=True,
    )

    # 显示图形
    plt.show()


def test_draw_bar_no_shade() -> None:
    """
    绘制 3D 柱状图

    3D 柱状图由 6 组向量集合组成, 前三组 (`x`, `y` 和 `z`) 分别表示柱状图在三维空间中三个坐标轴的位置,
    后三组 (`dx`, `dy` 和 `dz`) 表示柱状图在三维空间的尺寸, 分别表示柱状图的长宽高

    另外, 可以定义 `color` 参数表示颜色, 可以为一个值 (所有柱状图的颜色), 或和柱状图数量一致
    (即和 `x`, `y` 或 `z` 集合长度一致)
    """
    # 获取 Figure 对象
    fig = plt.figure()

    # 创建三维坐标
    ax = fig.add_subplot(111, projection='3d')
    # 设置标题
    ax.set_title("3D Bar with Shade")

    # 设置柱在三维空间中的点
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    y = np.array([5, 6, 7, 8, 2, 5, 6, 3, 7, 2])
    z = np.zeros(10)

    # 设置柱的宽度
    dx = dy = 1
    # 设置柱的高度
    dz = x + y

    # 颜色列表, 扩展到长度为 10 的集合
    colors = expand_list([
        "blue",
        "cornflowerblue",
        "mediumturquoise",
        "goldenrod",
        "yellow",
    ], 10)

    # 绘制柱状图
    ax.bar3d(  # type: ignore
        x, y, z,  # 柱在三维空间的坐标
        dx, dy, dz,  # 柱在三维空间的尺寸, 长宽高
        color=colors,  # 柱的颜色
        edgecolor="k",  # 描边颜色
        shade=False,
    )

    # 显示图形
    plt.show()
