import matplotlib.pyplot as plt


def test_draw_bar() -> None:
    """绘制基本柱状图

    柱状图由两组数据组成:
    - x 坐标为柱状图的类别, 由字符串集合组成
    - y 坐标为柱状图每个列表的数值, 由数值集合组成
    - x, y 集合的元素个数必须相同
    """
    # 设置 x 坐标轴, 类别集合
    x = ["Runoob-1", "Runoob-2", "Runoob-3", "C-RUNOOB"]
    # 设置 y 坐标轴, 数值集合
    y = [12, 22, 6, 18]

    # 绘制柱状图
    plt.bar(x, y)  # type:ignore

    # 显示绘图结果
    plt.show()


def test_draw_barh() -> None:
    """绘制纵向排列的柱状图

    纵向排列的柱状图将 x 轴和 y 轴互换, 从而绘制从上到下依次排列的柱状图
    """
    x = ["Runoob-1", "Runoob-2", "Runoob-3", "C-RUNOOB"]
    y = [12, 22, 6, 18]

    # barh 绘制纵向排列的柱状图. x, y 坐标不变
    plt.barh(x, y)  # type:ignore
    plt.show()


def test_draw_bar_with_colors() -> None:
    """给柱状图加上颜色

    1. 可以通过一组表示颜色 (明明颜色, RGB 色值) 的集合来为柱状图每个数值上色
    2. 如果颜色的个数可以小于柱状图数值个数, 此时设置的颜色会被循环重复使用
    """
    x = ["Runoob-1", "Runoob-2", "Runoob-3", "C-RUNOOB"]
    y = [12, 22, 6, 18]

    # 表示每个数值颜色的集合
    colors = ["#4CAF50", "r", "m", "#556B2F"]

    # 绘制柱状图, 加上颜色
    plt.bar(x, y, color=colors)  # type: ignore
    plt.show()


def test_draw_bar_with_width() -> None:
    """指定柱状图每个柱的宽度"""
    x = ["Runoob-1", "Runoob-2", "Runoob-3", "C-RUNOOB"]
    y = [12, 22, 6, 18]

    # 绘制柱状图, 设置每个柱的宽度
    plt.bar(x, y, width=0.1)  # type: ignore
    plt.show()


def test_draw_barh_with_height() -> None:
    """指定柱状图每个柱的高度

    如果柱状图是纵向绘制的, 即通过 `barh` 函数绘图, 则需要设置的是高度
    """
    x = ["Runoob-1", "Runoob-2", "Runoob-3", "C-RUNOOB"]
    y = [12, 22, 6, 18]

    # 绘制纵向柱状图, 设置每个柱的高度
    plt.barh(x, y, height=0.1)  # type: ignore
    plt.show()
