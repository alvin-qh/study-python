import numpy as np
from matplot import render_axis
from matplotlib import pyplot as plt


def test_draw_text() -> None:
    """测试绘制文本

    具体的参数为:
    - `x`: 文本的 x 坐标
    - `y`: 文本的 y 坐标
    - `s`: 文本字符串
    - `verticalalignment`: 文本和坐标的垂直对齐方式
    - `horizontalalignment`: 文本和坐标的水平对齐方式
    - `xycoords`: 选择指定的坐标轴系统
        - `figure points`: 图左下角的点
        - `figure pixels`: 图左下角的像素
        - `figure fraction`: 图的左下部分
        - `axes points`: 坐标轴左下角的点
        - `axes pixels`: 坐标轴左下角的像素
        - `axes fraction`: 左下轴的分数
        - `data`: 使用被注释对象的坐标系统 (默认)
        - `polar(theta, r)`: 极坐标系统
    - `arrowprops`: 箭头参数, 参数类型为字典对象
        - `width`: 箭头的宽度 (以点为单位)
        - `headwidth`: 箭头底部以点为单位的宽度
        - `headlength`: 箭头的长度 (以点为单位)
        - `shrink`: 总长度的一部分, 从两端“收缩”
        - `facecolor`: 箭头颜色
    - `bbox`: 给标题增加外框, 常用参数如下:
        - `boxstyle`: 方框外形
        - `facecolor`: (简写 `fc`) 背景颜色
        - `edgecolor`: (简写 `ec`) 边框线条颜色
        - `edgewidth`: 边框线条大小
    """
    # 绘制坐标系和网格
    render_axis(
        (-20, 20),  # x 坐标轴的范围
        (-120, 120),  # y 坐标轴的范围
        grid=(5, 20),  # 网格大小
    )

    # 第 1 组圆心的 x 轴坐标集合
    xs = np.array([5, -12, -18, 7, 2, -17, 2, -9, 4, 11, -12, -9, 6])
    # 第 1 组圆心的 y 轴坐标集合
    ys = np.array([99, -80, -87, -88, -111, 86, -103, -87, 94, -78, 77, 85, 86])

    # 绘制第 1 组点
    plt.scatter(xs, ys, color="hotpink", marker="o")

    lx = plt.xlim()
    offset = (lx[1] - lx[0]) / 60.0

    for x, y in zip(xs, ys):
        plt.text(
            x=x + offset,  # x, y 坐标值
            y=y,
            s=f"({x}, {y})",  # 要绘制的文本
            fontsize=6,  # 文本大小
            verticalalignment="center",  # 垂直对齐方式
            horizontalalignment="left",  # 水平对齐方式
            color="blue",  # 文本颜色
        )

    # 显示绘制结果
    plt.show()
