from typing import Union
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

Point = Tuple[float, float]


def render_axis(
    xlim: Optional[Point] = None,
    ylim: Optional[Point] = None,
    grid: Tuple[Union[int, float], Union[int, float]] = (1, 1),
    axis: bool = True,
    title: str = "",
) -> None:
    """绘制坐标系, 坐标轴刻度, 原点和网格

    Args:
        `xlim` (`Optional[Point]`, optional): 设定 `x` 坐标轴数值范围. Defaults to `None`.
        `ylim` (`Optional[Point]`, optional): 设定 `y` 坐标轴数值范围. Defaults to `None`.
        `grid` (`Tuple[int, int]`, optional): 设定网格单元值. Defaults to `(1, 1)`.
        `axis` (`bool`, optional): 是否绘制坐标轴. Defaults to `True`.
        `title` (`str`, optional): 图形标题. Defaults to `""`.
    """
    if title:
        plt.title(title)

    if xlim:
        # 设定 x 坐标轴的数值范围
        plt.xlim(left=xlim[0], right=xlim[1])

    if ylim:
        # 设定 y 坐标轴的数值范围
        plt.ylim(bottom=ylim[0], top=ylim[1])

    # 绘制网格
    plt.grid(
        True,  # 允许绘制网格线
        linestyle=":",  # 网格线条样式,
        # 包括: "‐" (实线), "‐‐" (破折线), "‐." (点划线), ":" (虚线)
        linewidth=0.5,  # 网格线宽度
    )

    # 获取坐标线对象
    # 图形的坐标线分别为 "top", "left", "bottom", "right" 四条
    ax = plt.gca()

    # 设置坐标轴单位刻度
    x, y = plt.xlim(), plt.ylim()
    # 按照 x 轴的范围, 以 grid 中横坐标单位长度绘制刻度
    ax.set_xticks(np.arange(x[0], x[1], grid[0]))
    # 按照 y 轴的范围, 以 grid 中纵坐标单位长度绘制刻度
    ax.set_yticks(np.arange(y[0], y[1], grid[1]))
    # 显示刻度
    ax.set_axisbelow(True)

    if axis:
        # 绘制原点坐标轴
        # 本例中使用自行绘制的坐标轴
        ax.axhline(linewidth=2, color="k")
        ax.axvline(linewidth=2, color="k")

    # 设置坐标轴的名称
    plt.xlabel("x")
    plt.ylabel("y")


def render_axis3d(
    xlim: Optional[Point] = None,
    ylim: Optional[Point] = None,
    zlim: Optional[Point] = None,
    grid: Tuple[Union[int, float], Union[int, float], Union[int, float]] = (1, 1, 1),
    axis: bool = True,
    title: str = "",
) -> Axes3D:
    """绘制坐标系, 坐标轴刻度, 原点和网格

    Args:
        `xlim` (`Optional[Point]`, optional): 设定 `x` 坐标轴数值范围. Defaults to `None`.
        `ylim` (`Optional[Point]`, optional): 设定 `y` 坐标轴数值范围. Defaults to `None`.
        `grid` (`Tuple[int, int, int]`, optional): 设定网格单元值. Defaults to `(1, 1)`.
        `axis` (`bool`, optional): 是否绘制坐标轴. Defaults to `True`.
        `title` (`str`, optional): 图形标题. Defaults to `""`.
    """
    if title:
        plt.title(title)

    # 获取 Figure 对象
    fig = plt.gcf()

    # 添加一个 3d 坐标系
    ax: Axes3D = fig.add_subplot(111, projection="3d")
    # 初始化视图, 设置视角 (即相机位置)
    # elev 设置视角沿着 y 轴旋转
    # azim 设置视角沿着 z 轴旋转
    ax.view_init(elev=None, azim=None)

    # 设置坐标轴标签
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    if xlim:
        # 设定 x 坐标轴的数值范围
        plt.xlim(xlim[0], xlim[1])

    if ylim:
        # 设定 y 坐标轴的数值范围
        plt.ylim(ylim[0], ylim[1])

    if zlim:
        # 设定 z 坐标轴的数值范围
        ax.set_zlim(zlim[0], zlim[1])

    # 获取三个坐标轴的范围
    x, y, z = plt.xlim(), plt.ylim(), ax.get_zlim()

    # 设置 x 轴的刻度, 从 x 轴的起点到终点, 刻度间距 1
    plt.xticks(np.arange(x[0], x[1], grid[0]))
    # 设置 y 轴的刻度, 从 y 轴的起点到终点, 刻度间距 1
    plt.yticks(np.arange(y[0], y[1], grid[1]))
    # 设置 z 轴的刻度, 从 z 轴的起点到终点, 刻度间距 1
    ax.set_zticks(np.arange(z[0], z[1], grid[2]))

    if axis:
        # 绘制原点
        ax.scatter([0], [0], [0], color="k", marker="x")

        def draw_line(
            start: Tuple[float, float, float],
            end: Tuple[float, float, float],
        ) -> None:
            """
            绘制 3D 线段

            Args:
                start (Tuple[float, float, float]): 线段起始位置
                end (Tuple[float, float, float]): 线段终止位置
            """
            # 将三维坐标转换为三个向量, 分别表示:
            # xs: 线段在 x 轴的起始和终止
            # ys: 线段在 y 轴的起始和终止
            # zs: 线段在 z 轴的起始和终止
            xs, ys, zs = ((start[i], end[i]) for i in range(0, 3))
            # 绘制线段
            ax.plot(xs, ys, zs, color="k", linestyle=":")

        # 绘制 x 轴坐标轴
        draw_line((-5, 0, 0), (5, 0, 0))
        # 绘制 y 轴坐标轴
        draw_line((0, -5, 0), (0, 5, 0))
        # 绘制 z 轴坐标轴
        draw_line((0, 0, -5), (0, 0, 5))

    return ax


def get_axis3d(name: str = "3d") -> Axes3D:
    # 获取 Figure 对象
    fig = plt.gcf()

    # 获取该 Figure 对象中所有的坐标对象
    for ax in fig.get_axes():
        # 判断坐标的名称是否符合
        if ax.name == name:
            # 返回
            return ax

    raise ValueError(f'invalid axis name "{name}"')
