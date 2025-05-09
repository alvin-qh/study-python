import matplotlib.pyplot as plt


def test_draw_stack() -> None:
    """绘制堆叠图

    堆叠图类似于折线图, 一般情况下, 用 `x` 轴表示时间维度, `y` 轴表示数值变化, 堆叠指的是 `y` 坐标的值是累加的结果
    """
    # 设置标题
    plt.title("Stack Plot")

    # 设置坐标轴标签
    plt.xlabel("x")
    plt.ylabel("y")

    # 设置 x 轴坐标点位
    x = [1, 2, 3, 4, 5]

    # 设置四个指标的值, 体现在 y 轴上
    y1 = [7, 8, 6, 11, 7]
    y2 = [2, 3, 4, 3, 2]
    y3 = [7, 8, 7, 2, 2]
    y4 = [9, 4, 7, 11, 13]

    # 绘制图例
    # 对应堆叠图的每个颜色, 绘制 5 条线段, 作为图例
    for c, l in zip(["m", "c", "r", "k"], ["y1", "y2", "y3", "y4"]):
        plt.plot([], [], color=c, label=l, linewidth=5)

    # 显示图例
    plt.legend()

    # 绘制堆叠图
    plt.stackplot(
        x,  # x 坐标数值
        y1,
        y2,
        y3,
        y4,  # y 坐标数值
        colors=["m", "c", "r", "k"],  # y 坐标每个数值对应的颜色
    )

    # 显示绘图结果
    plt.show()
