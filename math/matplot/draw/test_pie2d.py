import matplotlib.pyplot as plt


def test_draw_pie() -> None:
    """
    绘制基本饼图
    """
    # 设置每个扇形代表的数值
    x = [35, 25, 25, 15]

    # 绘制饼图
    plt.pie(x)  # type: ignore

    # 显示图形
    plt.show()


def test_draw_pie_with_colors() -> None:
    """
    设置每个扇形的颜色
    """
    x = [35, 25, 25, 15]

    # 设置每个扇形的标签
    labels = ['A', 'B', 'C', 'D']

    # 各个扇形数值对应的颜色
    colors = ["#d5695d", "#5d8ca8", "#65a479", "#a564c9"]

    # 绘制饼图并设置颜色
    plt.pie(  # type: ignore
        x,
        labels=labels,  # 设置每个扇形的标签
        colors=colors,  # 设置每个扇形的颜色
    )
    plt.show()


def test_show_prominent_sector() -> None:
    x = [35, 25, 25, 15]

    labels = ['A', 'B', 'C', 'D']
    colors = ["#d5695d", "#5d8ca8", "#65a479", "#a564c9"]

    # 设置扇形和其它扇形的间隔, 值越大, 间隔越大
    # 第二个扇形具备间隔, 所谓第二个扇形, 即从饼图的 3 点钟方向附近逆时针数第二个扇形
    # 即标签为 B 的那个扇形
    explode = [0, 0.1, 0, 0]

    # 绘制饼图并设置颜色
    plt.pie(  # type: ignore
        x,
        labels=labels,
        colors=colors,
        explode=explode,  # 设置扇形和其它扇形的间隔
        autopct="%.2f%%",  # 设置扇形上显示数据的格式, 这里设置为百分比
    )
    plt.show()
