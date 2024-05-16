from math import sqrt

import matplotlib.pyplot as plt

from matplot import render_axis


def test_draw_arrow() -> None:
    """绘制一个箭头

    1. 箭头由两部分组成: 箭头的头部 (一个三角形) 和箭头的尾部 (一个线段)
    2. 计算箭头长度的时候, 需要注意, 整个箭头的长度需要减去头部的长度, 绘制后加上头部长度就刚刚好
    """

    # 绘制坐标系
    render_axis(
        (-1, 10),  # x 坐标轴的范围
        (-1, 10),  # y 坐标轴的范围
        grid=(2, 2),  # 网格大小
        title="Draw arrow",
    )

    # 设置箭头的起始和结尾
    tip, tail = (8, 9), (1, 2)

    # 获取 x 坐标轴的范围
    x = plt.xlim()

    # 计算箭头头部的长度, 令头部长度为 x 轴长度的 1/30
    tip_length = (x[1] - x[0]) / 30.0

    # 计算整个箭头的整个长度 (勾股定理), 该长度包含了箭头头部的长度
    length = sqrt((tip[1] - tail[1]) ** 2 + (tip[0] - tail[0]) ** 2)

    # 去除箭头头部长度, 获取箭头的实际长度
    new_length = length - tip_length

    # 计算无头长度和有头长度的比例
    k = new_length / length

    # 通过比例计算新的计算箭头头部的坐标
    new_x = (tip[0] - tail[0]) * k
    new_y = (tip[1] - tail[1]) * k

    # 获取 Axes 对象, 表示一个坐标
    gca = plt.gca()  # type: ignore

    # 绘制箭头
    gca.arrow(
        tail[0],  # 箭头的尾部的 x 坐标
        tail[1],  # 箭头的尾部的 y 坐标
        new_x,  # 箭头的头部的 x 坐标
        new_y,  # 箭头的头部的 y 坐标
        head_width=tip_length / 1.5,  # 箭头头部的宽度
        head_length=tip_length,  # 箭头的长度
        fc="b",  # 箭头头部颜色
        ec="r",  # 箭头线条额颜色
    )

    plt.show()
