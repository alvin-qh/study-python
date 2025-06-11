import matplotlib.pyplot as plt
import numpy as np

from matplot import render_axis


def test_draw_splashes() -> None:
    """测试绘制散点图

    1. 通过一组圆心值绘制实心圆圈
    2. 通过 `c` (`color`) 参数指定颜色
    """
    # 绘制坐标系和网格
    render_axis(
        (0, 20),  # x 坐标轴的范围
        (70, 120),  # y 坐标轴的范围
        grid=(5, 10),  # 网格大小
        axis=False,
    )

    # 第 1 组圆心的 x 轴坐标集合
    x = np.array([5, 7, 8, 7, 2, 17, 2, 9, 4, 11, 12, 9, 6])
    # 第 1 组圆心的 y 轴坐标集合
    y = np.array([99, 86, 87, 88, 111, 86, 103, 87, 94, 78, 77, 85, 86])

    # 绘制第 1 组点
    plt.scatter(x, y, c="hotpink", marker="o")

    # 第 2 组圆心的 x 轴坐标集合
    x = np.array([2, 2, 8, 1, 15, 8, 12, 9, 7, 3, 11, 4, 7, 14, 12])
    # 第 2 组圆心的 y 轴坐标集合
    y = np.array([100, 105, 84, 105, 90, 99, 90, 95, 94, 100, 79, 112, 91, 80, 85])
    # 绘制第 2 组点
    plt.scatter(x, y, c="#88c999", marker="x")

    # 显示画布
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

    # 绘制坐标系和网格
    render_axis(
        (-0.1, 1.1),  # x 坐标轴的范围
        (-0.1, 1.1),  # y 坐标轴的范围
        grid=(0.1, 0.1),  # 网格大小
        axis=False,
    )

    # 产生 50 个颜色值
    c = np.random.rand(N)

    # 产生 50 个随机半径 (0 ~ 15) 并计算对应的面积
    area = np.pi * (15 * np.random.rand(N)) ** 2

    plt.scatter(
        x,  # 点在 x 轴的坐标集
        y,  # 点在 y 轴的坐标集
        s=area,  # 对应的圆面积
        c=c,  # 对应的颜色, 这里设为调色板的颜色编号, 0~100 之间
        cmap="afmhot_r",  # 设置调色板, 之后可以通过 0~100 的数值代表调色板的颜色
        alpha=0.5,
    )

    plt.colorbar()  # 显示调色板, 即各数字对应的颜色
    plt.show()
