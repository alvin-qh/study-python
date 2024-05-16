import matplotlib.pyplot as plt
import numpy as np

from matplot import render_axis3d, get_axis3d


def test_draw_splashes() -> None:
    """测试绘制散点图

    1. 通过一组圆心值绘制实心圆圈
    2. 通过 `c` (`color`) 参数指定颜色
    """
    # 绘制坐标系和网格
    render_axis3d(
        (-10, 10),  # x 坐标轴的范围
        (-10, 10),  # y 坐标轴的范围
        (-10, 10),  # z 坐标轴的范围
        grid=(2, 2, 2),  # 网格大小
        axis=False,
    )

    ax = get_axis3d()

    # 定义点在三个坐标轴上的坐标向量
    x1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y1 = [5, 6, 7, 8, 2, 5, 6, 3, 7, 2]
    z1 = [1, 2, 6, 3, 2, 7, 3, 3, 7, 2]

    # 绘制散点图
    ax.scatter(x1, y1, z1, c="g", marker="o")

    # 定义点在三个坐标轴上的坐标向量
    x2 = [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10]
    y2 = [-5, -6, -7, -8, -2, -5, -6, -3, -7, -2]
    z2 = [1, 2, 6, 3, 2, 7, 3, 3, 7, 2]

    # 绘制散点图
    ax.scatter(x2, y2, z2, c="r", marker="x")

    plt.show()


def test_draw_bubbles() -> None:
    """绘制泡泡图

    1. 通过 `s` (`size`) 参数指定绘制图形的半径
    2. 通过调色板设置颜色, `c` (`color`) 参数指定 `0~100` 的数值, 通过 `cmap` 参数指定调色板
    """
    N = 50

    # 产生 50 个坐标
    x = np.random.rand(N)  # x 坐标轴上 50 个随机值
    y = np.random.rand(N)  # y 坐标轴上 50 个随机值
    z = np.random.rand(N)  # z 坐标轴上 50 个随机值

    # 绘制坐标系和网格
    render_axis3d(
        (-0.1, 1.1),  # x 坐标轴的范围
        (-0.1, 1.1),  # y 坐标轴的范围
        (-0.1, 1.1),  # z 坐标轴的范围
        grid=(0.1, 0.1, 0.1),  # type: ignore  # 网格大小
        axis=False,
    )

    ax = get_axis3d()

    # 产生 50 个颜色值
    c = np.random.rand(N)

    # 产生 50 个随机半径 (0 ~ 15) 并计算对应的大小
    area = np.pi * (15 * np.random.rand(N)) ** 2

    ax.scatter(
        x,  # 点在 x 轴的坐标集
        y,  # 点在 y 轴的坐标集
        z,  # 点在 z 轴的坐标集
        s=area,  # 对应的圆大小, 默认 20
        c=c,  # type: ignore # 对应的颜色, 这里设为调色板的颜色编号, 0~100 之间
        cmap="afmhot_r",  # 设置调色板, 之后可以通过 0~100 的数值代表调色板的颜色
    )

    # plt.colorbar()  # type: ignore # 显示调色板, 即各数字对应的颜色
    plt.show()
