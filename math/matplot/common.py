from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np

Point = Tuple[float, float]


def render_axis(xlim: Optional[Point] = None, ylim: Optional[Point] = None, grid=(1, 1), axis=True, title="") -> None:
    plt.title(title)

    if xlim:
        # 设定 x 坐标轴的数值范围
        plt.xlim(left=xlim[0], right=xlim[1])

    if ylim:
        # 设定 y 坐标轴的数值范围
        plt.ylim(bottom=ylim[0], top=ylim[1])

    # 绘制网格
    plt.grid(  # type: ignore
        True,  # 允许绘制网格线
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

    if axis:
        # 绘制原点坐标轴
        # 本例中使用自行绘制的坐标轴
        ax.axhline(linewidth=2, color="k")
        ax.axvline(linewidth=2, color="k")

    # 设置坐标轴的名称
    plt.xlabel("X")
    plt.ylabel("Y")
