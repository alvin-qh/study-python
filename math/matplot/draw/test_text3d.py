from matplotlib import pyplot as plt

from ..common import get_axis3d, render_axis3d


def test_draw_text() -> None:
    """
    测试绘制文本
    """
    # 绘制坐标系和网格
    render_axis3d(
        (-10, 10),  # x 坐标轴的范围
        (-10, 10),  # y 坐标轴的范围
        (-10, 10),  # z 坐标轴的范围
        grid=(2, 2, 2),  # 网格大小
    )

    # 获取 3d 坐标系对象
    ax = get_axis3d()

    # 要绘制的点的坐标
    x1 = [1, -2, 3, 4, 5, -6, 7, 8, -9, 10]
    y1 = [5, 6, 7, -8, 2, -5, -6, 3, 7, 2]
    z1 = [1, -2, 6, 3, 2, 7, -3, 3, -7, 2]

    # 计算 x 轴的长度
    lx = ax.get_xlim()
    # 计算文本和坐标点的偏移量
    offset = (lx[1] - lx[0]) / 60.0

    # 绘制散点图
    ax.scatter(x1, y1, z1, c="g", marker="o")

    # 遍历所有点的坐标
    for x, y, z in zip(x1, y1, z1):
        # 绘制文本
        ax.text(
            x=x + offset,  # 文本 x, y, z 坐标
            y=y + offset,
            z=z,
            s=f"({x}, {y}, {z})",  # 文本字符串
            fontsize=8,  # 文本字符大小
            zorder=1,  # z 轴的顺序
            verticalalignment="center",  # 文本和坐标的垂直对齐方式
            color="blue",  # 文本颜色
        )

    # 显示绘制结果
    plt.show()
