from math import sqrt

import matplotlib.pyplot as plt

from ..common import render_axis


def test_draw_arrow() -> None:
    # 绘制坐标系
    render_axis(
        (-1, 10),  # x 坐标轴的范围
        (-1, 10),  # y 坐标轴的范围
        grid=(2, 2),  # 网格大小
        title="Draw arrow",
    )

    # 获取 x 坐标轴的
    x = plt.xlim()

    # 设置箭头的起始和结尾
    tip, tail = (8, 9), (1, 2)

    # 计算箭头头部的长度, 令头部长度为 x 轴的 1/30
    tip_length = (x[1] - x[0]) / 30.

    # 计算整个箭头的长度 (勾股定理)
    length = sqrt((tip[1] - tail[1]) ** 2 + (tip[0] - tail[0]) ** 2)

    # 计算
    new_length = length - tip_length

    new_x = (tip[0] - tail[0]) * (new_length / length)
    new_y = (tip[1] - tail[1]) * (new_length / length)

    gca = plt.gca()  # type: ignore
    gca.arrow(
        tail[0],
        tail[1],
        new_x,
        new_y,
        head_width=tip_length/1.5,
        head_length=tip_length,
        fc="b",
        ec="r",
    )

    plt.show()
