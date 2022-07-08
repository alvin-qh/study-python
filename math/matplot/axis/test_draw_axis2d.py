import matplotlib.pyplot as plt
import numpy as np


def test_axis_grid() -> None:
    """
    绘制坐标系

    绘制一个坐标系, 设定 `x`, `y` 坐标轴的单位长度, 并在原点绘制坐标轴
    """
    # 设定网格的大小
    grid = (1, 1)

    # 设定图形标题
    plt.title("Draw axis with grid")

    # 设定 x 坐标轴的数值范围
    plt.xlim(left=-10, right=10)
    # 设定 y 坐标轴的数值范围
    plt.ylim(bottom=-5, top=5)
    # 绘制网格
    plt.grid(  # type: ignore
        True,  # 允许绘制网格线
        which="major",  # 表示对那一类网格线进行设置, 可选值有 "major", "minor" 和 "both"
        axis="both",  # 表示对那个坐标方向的网格线进行设置, 可选值为 "x", "y" 和 "both"
        color="y",  # 网格线的颜色,
                    # 可选值为"b", "m", "g", "y", "r", "k", "w", "c" 以及 "#rrggbb"
        linestyle=":",  # 网格线条样式,
                        # 包括: "‐" (实线), "‐‐" (破折线), "‐." (点划线), ":" (虚线)
        linewidth=0.5,  # 网格线宽度
    )

    # 获取坐标线对象
    # 图形的坐标线分别为 "top", "left", "bottom", "right" 四条
    ax = plt.gca()  # type: ignore

    # 设置坐标轴单位刻度
    x, y = plt.xlim(), plt.ylim()
    # 按照 x 轴的范围, 以 grid 中横坐标单位长度绘制刻度
    ax.set_xticks(np.arange(x[0], x[1], grid[0]))
    # 按照 y 轴的范围, 以 grid 中纵坐标单位长度绘制刻度
    ax.set_yticks(np.arange(y[0], y[1], grid[1]))
    # 显示刻度
    ax.set_axisbelow(True)

    # 绘制原点坐标轴
    # 本例中使用自行绘制的坐标轴
    ax.axhline(linewidth=2, color="k")
    ax.axvline(linewidth=2, color="k")

    # 设置坐标轴的名称
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.show()


def test_axis_movement() -> None:
    """
    绘制坐标系

    绘制一个坐标系, 设定 `x`, `y` 坐标轴的单位长度.
    将位于 "left" 和 "bottom" 位置的坐标轴移动到原点中心位置.
    去除位于 "right" 和 "top" 的坐标轴
    """
    # 设定网格的大小
    grid = (1, 1)

    # 设定图形标题
    plt.title("Draw axis with grid")

    # 设定 x 坐标轴的数值范围
    plt.xlim(left=-10, right=10)
    # 设定 y 坐标轴的数值范围
    plt.ylim(bottom=-5, top=15)
    # 绘制网格
    plt.grid(  # type:ignore
        True,  # 允许绘制网格线
        which="major",  # 表示对那一类网格线进行设置, 可选值有 "major", "minor" 和 "both"
        axis="both",  # 表示对那个坐标方向的网格线进行设置, 可选值为 "x", "y" 和 "both"
        color="k",  # 网格线的颜色,
                    # 可选值为"b", "m", "g", "y", "r", "k", "w", "c" 以及 "#rrggbb"
        linestyle=":",  # 网格线条样式,
                        # 包括: "‐" (实线), "‐‐" (破折线), "‐." (点划线), ":" (虚线)
        linewidth=0.5,  # 网格线宽度
    )

    # 获取坐标线对象
    # 图形的坐标线分别为 "top", "left", "bottom", "right" 四条
    ax = plt.gca()  # type: ignore

    # 设置坐标轴单位刻度
    x, y = plt.xlim(), plt.ylim()
    # 按照 x 轴的范围, 以 grid 中横坐标单位长度绘制刻度
    ax.set_xticks(np.arange(x[0], x[1], grid[0]))
    # 按照 y 轴的范围, 以 grid 中纵坐标单位长度绘制刻度
    ax.set_yticks(np.arange(y[0], y[1], grid[1]))
    # 显示刻度
    ax.set_axisbelow(True)

    # 设置横坐标轴刻度数字显示的位置
    ax.xaxis.set_ticks_position("bottom")
    # 设置底部横坐标轴的位置到原点位置
    ax.spines["bottom"].set_position(("data", 0))

    # 设置纵坐标轴刻度数字显示的位置
    ax.yaxis.set_ticks_position("left")
    # 设置左边纵坐标轴的位置到原点位置
    ax.spines["left"].set_position(("data", 0))

    # 删除顶部和右边的两条坐标轴
    ax.spines["top"].set_color("none")
    ax.spines["right"].set_color("none")

    plt.show()
