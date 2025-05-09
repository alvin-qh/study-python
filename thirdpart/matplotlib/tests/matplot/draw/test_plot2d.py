import matplotlib.pyplot as plt
import numpy as np

from matplot import render_axis


def test_draw_line() -> None:
    """测试在坐标系中绘制一条直线"""
    # 设置要绘制线段的 x 坐标轴和 y 坐标轴的坐标
    x_axis, y_axis = (0, 6), (0, 100)

    # 绘制坐标系
    render_axis(
        (-1, 7),  # x 坐标轴的范围
        (-10, 110),  # y 坐标轴的范围
        grid=(1, 20),  # 网格大小
        title="Draw line",
    )

    # 绘制直线
    # 两个端点坐标分别为 (0, 0), (6, 100)
    # 第三个参数为 fmt, 表示 r (红色), x (端点显示为叉叉), - (线段显示为实线)
    plt.plot(
        x_axis,  # x 坐标轴的坐标序列
        y_axis,  # y 坐标轴的坐标序列
        "rx-",  # 绘图格式
    )
    # 如果不使用 fmt 参数, 则需要使用 color, linestyle, linewidth 和 marker 参数
    # plt.plot(x_axis, y_axis, color="C1", linestyle="-", marker="x")

    # 显示绘图结果
    plt.show()


def test_draw_markers() -> None:
    """绘制线段端点"""
    # 设置要绘制线段的 x 坐标轴和 y 坐标轴的坐标
    x_axis, y_axis = (0, 5, 10), (0, 50, 100)

    # 绘制坐标系
    render_axis(
        (-1, 11),  # x 坐标轴的范围
        (-10, 110),  # y 坐标轴的范围
        grid=(1, 20),  # 网格大小
        title="Draw markers",
    )

    # 绘制两个点
    # 三个点坐标分别为 (0, 0), (5, 50), (10, 100)
    # 第三个参数为 fmt, 表示 r (红色), o (端点显示圆点), 不显示连线
    plt.plot(
        x_axis,  # x 坐标轴的坐标序列
        y_axis,  # y 坐标轴的坐标序列
        "ro",  # 绘图格式
    )
    # 如果不使用 fmt 参数, 则需要使用 color, linewidth 和 marker 参数
    # plt.plot(
    #     x_axis,
    #     y_axis,
    #     linewidth=0,
    #     color="r",
    #     marker="o",
    # )

    # 显示绘图结果
    plt.show()


def test_draw_line_with_markers() -> None:
    """绘制线段端点"""
    # 设置要绘制线段的 x 坐标轴和 y 坐标轴的坐标
    x_axis, y_axis = (1, 2, 6, 8), (3, 8, 1, 10)

    # 绘制坐标系
    render_axis(
        (-1, 11),  # x 坐标轴的范围
        (-1, 11),  # y 坐标轴的范围
        grid=(1, 1),  # 网格大小
        title="Draw markers",
    )

    # 绘制两个点
    # 三个点坐标分别为 (0, 0), (5, 50), (10, 100)
    # 第三个参数为 fmt, 表示 r (红色), o (端点显示圆点), 不显示连线
    plt.plot(
        x_axis,  # x 坐标轴的坐标序列
        y_axis,  # y 坐标轴的坐标序列
        "ro-",  # 绘图格式
    )
    # 如果不使用 fmt 参数, 则需要使用 color, linewidth 和 marker 参数
    # plt.plot(
    #     x_axis,
    #     y_axis,
    #     linestyle="-",
    #     color="r",
    #     marker="o",
    # )

    # 显示绘图结果
    plt.show()


def test_draw_multi_lines() -> None:
    """在一个坐标系内绘制多条线段

    `plt.plot` 函数的 `*args` 参数可以传递个坐标轴, 即:

    ```python
    plt.plot(
        第 1 组 x 坐标列表,
        第 1 组 y 坐标列表,
        第 1 组绘图样式,
        第 2 组 x 坐标列表,
        第 2 组 y 坐标列表,
        第 2 组绘图样式,
        ...
        第 n 组 x 坐标列表,
        第 n 组 y 坐标列表,
        第 n 组绘图样式,
    )
    ```

    这样即可以在一次调用中绘制多组线段
    """
    # 设置要绘制线段的 x 坐标轴和 y 坐标轴的坐标
    # 第一组线段
    x_axis1, y_axis1 = np.array([1, 2, 6, 8]), np.array([3, 8, 1, 10])
    # 第二组线段
    x_axis2, y_axis2 = x_axis1 * 2, y_axis1 * 2

    # 绘制坐标系
    render_axis(
        (-1, 20),  # x 坐标轴的范围
        (-1, 22),  # y 坐标轴的范围
        grid=(1, 1),  # 网格大小
        title="Draw markers",
    )

    # 绘制两个点
    # 三个点坐标分别为 (0, 0), (5, 50), (10, 100)
    # 第三个参数为 fmt, 表示 r (红色), o (端点显示圆点), 不显示连线
    plt.plot(
        x_axis1,  # x 坐标轴的坐标序列
        y_axis1,  # y 坐标轴的坐标序列
        "ro-",  # 绘图格式
        x_axis2,  # x 坐标轴的坐标序列
        y_axis2,  # y 坐标轴的坐标序列
        "bx--",  # 绘图格式
    )

    # 显示绘图结果
    plt.show()


def test_draw_curve() -> None:
    """绘制 4 个周期的正弦和余弦波函数图"""
    # 计算 x 轴坐标集合, 为 0 ~ 4pi, 每 0.1 为一段
    x = np.arange(0, 4 * np.pi, 0.1)
    # 根据 x 计算正弦值作为 y1 的坐标集合
    y1 = np.sin(x)
    # 根据 x 计算余弦值作为 y2 的坐标集合
    y2 = np.cos(x)

    # 绘制坐标系
    render_axis(
        (np.min(x) - 1, np.max(x) + 1),  # x 坐标轴的范围
        (np.min(y1) - 1, np.max(y1) + 1),  # y 坐标轴的范围
        grid=(1, 1),  # 网格大小
        title="Draw waves",
    )

    # 绘制图形
    plt.plot(
        x,  # 绘制 x 和 y1 组成的正弦图形
        y1,
        x,  # 绘制 x 和 y2 组成的余弦图形
        y2,
    )

    # 显示绘图结果
    plt.show()
