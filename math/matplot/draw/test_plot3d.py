import matplotlib.pyplot as plt

from ..common import get_axis3d, render_axis3d


def test_draw_line3d() -> None:
    """
    测试在坐标系中绘制一条直线
    """
    # 绘制坐标系
    render_axis3d(
        (-5, 5),  # x 坐标轴的范围
        (-5, 5),  # y 坐标轴的范围
        (-5, 5),  # y 坐标轴的范围
        grid=(1, 1, 1),  # 网格大小
    )

    # 获取名为 '3d' 的坐标对象
    ax = get_axis3d()

    # 设置线段 x, y 和 z 三个坐标轴的起始坐标
    xs = (0, 1)
    ys = (1, 4)
    zs = (0, 3)

    # 绘制线段
    ax.plot(xs, ys, zs, color="r", linestyle="-")

    # 显示绘图结果
    plt.show()
