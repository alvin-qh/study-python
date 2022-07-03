from enum import Enum
from math import ceil, floor, sqrt
from typing import Any, Generator, Iterable, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np

# 表示一个数值, 可以为整数或浮点数
Number = Union[int, float]

# 表示一个点, 是数值的二元组
Vector2D = Tuple[Number, Number]


class Color(Enum):
    """
    表示颜色的枚举
    """
    blue = "C0"
    black = "k"
    red = "C3"
    green = "C2"
    purple = "C4"
    orange = "C2"
    gray = "gray"


class Drawable:
    """
    所有绘图的超类
    """

    def __init__(self, color: Color) -> None:
        """
        初始化对象, 指定绘图的颜色

        Args:
            color (Color): 颜色枚举
        """
        # 设定颜色的值
        self.color = color.value


class Polygon(Drawable):
    """
    多边形绘图类

    多边形是一组线段组成的图像, 即将一组点进行两两连接
    """

    def __init__(self, *vertices: Vector2D, color=Color.blue, fill: Optional[Color] = None, alpha=0.4) -> None:
        """


        Args:
            vertices (Tuple[Vector2D]): 顶点向量集合
            color (Color, optional): 绘图颜色. Defaults to `Color.blue`.
            fill (Optional[Color], optional): 填充颜色. Defaults to `None`.
            alpha (float, optional): 填充透明度. Defaults to `0.4`.
        """
        super().__init__(color)

        self.vertices = vertices
        self.fill = fill.value if fill else None
        self.alpha = alpha


class Points(Drawable):
    """
    二维向量集合绘图类

    表示一个向量集合, 即二维坐标上一组点的集合
    """

    def __init__(self, *vectors: Vector2D, color=Color.black):
        """
        初始化对象

        Args:
            vectors (Tuple[Vector2D]): 向量集合
            color (Color, optional): 绘图颜色. Defaults to `Color.black`.
        """
        super().__init__(color)
        self.vectors = list(vectors)


class Arrow(Drawable):
    def __init__(self, tip, tail=(0, 0), color=Color.red):
        super().__init__(color)

        self.tip = tip
        self.tail = tail


class Segment(Drawable):
    """
    表示一个线段

    线段是由两个点组成
    """

    def __init__(self, start_point: Vector2D, end_point: Vector2D, color=Color.blue):
        """
        初始化对象

        Args:
            start_point (Vector2D): 起始点向量
            end_point (Vector2D): 终结点向量
            color (Color, optional): 颜色. Defaults to `Color.blue`.
        """
        super().__init__(color)

        self.start_point = start_point
        self.end_point = end_point


def extract_vectors(objects: Iterable[Drawable]) -> Generator[Vector2D, None, None]:
    """
    展开向量

    将向量展开为一组 `Point` 对象的序列 (生成器), 用于绘图时获取每个点

    Args:
        objects (Iterable[Drawable]): 绘图对象集合

    Raises:
        TypeError: 无效的绘图类型

    Yields:
        Generator[Point, None, None]: 图像中的每个点组成的序列
    """
    # 遍历集合中的绘图对象
    for o in objects:
        # 绘制多边形
        if isinstance(o, Polygon):
            # 产生多边形每个顶点
            for v in o.vertices:
                yield v

        # 绘制点集合
        elif isinstance(o, Points):
            # 产生点集合中的每个点
            for v in o.vectors:
                yield v

        elif isinstance(o, Arrow):
            yield o.tip
            yield o.tail

        # 绘制线段
        elif isinstance(o, Segment):
            # 产生线段的第一个点
            yield o.start_point
            # 产生线段的第二个点
            yield o.end_point

        else:
            raise TypeError(f"Unrecognized object: {o}")


def draw(
    *objects: Drawable,
    origin=True,
    axes=True,
    grid=(1, 1),
    nice_aspect_ratio=True,
    width=6,
    save_as=None,
) -> None:
    """
    绘制图像

    Args:
        objects (Tuple[Drawable]): 要绘制的图像对象集合
        origin (bool, optional): _description_. Defaults to `True`.
        axes (bool, optional): _description_. Defaults to `True`.
        grid (tuple, optional): _description_. Defaults to (1, 1).
        nice_aspect_ratio (bool, optional): 坐标系是否匹配最佳长宽比. Defaults to `True`.
        width (int, optional): _description_. Defaults to 6.
        save_as (_type_, optional): _description_. Defaults to None.

    Raises:
        TypeError: _description_
    """
    xs: Iterable[Any]
    ys: Iterable[Any]

    xs, ys = zip(*list(extract_vectors(objects)))

    max_x, max_y, min_x, min_y = (
        max(0, *xs), max(0, *ys), min(0, *xs), min(0, *ys)
    )

    if grid:
        x_padding = max(ceil(0.05*(max_x-min_x)), grid[0])
        y_padding = max(ceil(0.05*(max_y-min_y)), grid[1])

        plt.xlim(
            floor((min_x - x_padding) / grid[0]) * grid[0],
            ceil((max_x + x_padding) / grid[0]) * grid[0],
        )
        plt.ylim(
            floor((min_y - y_padding) / grid[1]) * grid[1],
            ceil((max_y + y_padding) / grid[1]) * grid[1],
        )

    if origin:
        plt.scatter([0], [0], color="k", marker="x")  # type: ignore

    x, y = plt.xlim(), plt.ylim()
    gca = plt.gca()  # type: ignore

    if grid:
        gca.set_xticks(np.arange(x[0], x[1], grid[0]))
        gca.set_yticks(np.arange(y[0], y[1], grid[1]))
        plt.grid(True)

        gca.set_axisbelow(True)

    if axes:
        gca.axhline(linewidth=2, color="k")
        gca.axvline(linewidth=2, color="k")

    for o in objects:
        if isinstance(o, Polygon):
            # 绘制多边形
            for i in range(0, len(o.vertices)):
                x1, y1 = o.vertices[i]
                x2, y2 = o.vertices[(i+1) % len(o.vertices)]

                plt.plot([x1, x2], [y1, y2], color=o.color)

            if o.fill:
                xs = [v[0] for v in o.vertices]
                ys = [v[1] for v in o.vertices]
                gca.fill(xs, ys, o.fill, alpha=o.alpha)

        elif isinstance(o, Points):
            # 绘制点集
            xs = [v[0] for v in o.vectors]
            ys = [v[1] for v in o.vectors]
            plt.scatter(xs, ys, color=o.color)  # type: ignore

        elif isinstance(o, Arrow):
            tip, tail = o.tip, o.tail
            tip_length = (x[1] - x[0]) / 20.

            length = sqrt((tip[1]-tail[1])**2 + (tip[0]-tail[0])**2)
            new_length = length - tip_length

            new_y = (tip[1] - tail[1]) * (new_length / length)
            new_x = (tip[0] - tail[0]) * (new_length / length)

            gca.arrow(
                tail[0],
                tail[1],
                new_x,
                new_y,
                head_width=tip_length/1.5,
                head_length=tip_length,
                fc=o.color,
                ec=o.color,
            )

        elif isinstance(o, Segment):
            # 绘制线段
            x1, y1 = o.start_point
            x2, y2 = o.end_point
            plt.plot([x1, x2], [y1, y2], color=o.color)

        else:
            raise TypeError(f"Unrecognized object: {o}")

    # 如果设置了坐标系最佳长宽比, 则根据点集进行计算
    if nice_aspect_ratio:
        # 计算坐标高度
        coords_height = y[1] - y[0]
        # 计算坐标宽度
        coords_width = x[1] - x[0]

        plt.gcf().set_size_inches(  # type: ignore
            width, width * coords_height / coords_width,
        )

    if save_as:
        plt.savefig(save_as)

    plt.show()
