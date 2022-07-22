from enum import Enum
from math import ceil, floor, sqrt
from typing import Any, Generator, Iterable, List, Optional, Tuple, cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch  # type: ignore
from mpl_toolkits.mplot3d import Axes3D, proj3d  # type:ignore

from . import Number, Vector2D, Vector3D


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

    def __init__(
        self,
        *vertices: Vector2D,
        color=Color.blue,
        fill: Optional[Color] = None,
        alpha=0.4,
    ) -> None:
        """
        初始化对象

        设置多边形的各个顶点向量

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

    def __init__(self, *vectors: Vector2D, show_coord=True, color=Color.black) -> None:
        """
        初始化对象

        Args:
            vectors (Tuple[Vector2D]): 向量集合
            show_coord (bool): 是否显示坐标值
            color (Color, optional): 绘图颜色. Defaults to `Color.black`.
        """
        super().__init__(color)
        self.vectors = list(vectors)
        self.show_coord = show_coord


class Arrow(Drawable):
    """
    箭头绘图类, 绘制一个箭头图形

    给定两个向量, 绘制一个从一个向量指向另一个的箭头
    """

    def __init__(self, tip: Vector2D, tail: Vector2D = (0, 0), color=Color.red) -> None:
        """
        初始化对象, 设置箭头指向的二维向量和箭头发出的二维向量

        Args:
            tip (Vector2D): 箭头指向的向量
            tail (Vector2D, optional): 箭头发出的向量, 默认为原点. Defaults to `(0, 0)`.
            color (_type_, optional): 绘图颜色. Defaults to `Color.red`.
        """
        super().__init__(color)

        self.tip = tip
        self.tail = tail


class Segment(Drawable):
    """
    表示一个线段

    线段是由两个点组成
    """

    def __init__(self, start_point: Vector2D, end_point: Vector2D, color=Color.blue) -> None:
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
    将绘图对象展开成向量

    将向量展开为一组 `Vector2D` 对象的序列 (生成器), 用于绘图时获取每个点

    Args:
        objects (Iterable[Drawable]): 绘图对象集合

    Raises:
        TypeError: 无效的绘图类型

    Yields:
        Generator[Vector2D, None, None]: 图像中的每个点组成的序列
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
    save_as="",
) -> None:
    """
    绘制图像

    Args:
        objects (Tuple[Drawable]): 要绘制的图像对象集合
        origin (bool, optional): 是否绘制原点. Defaults to `True`.
        axes (bool, optional): 是否绘制坐标轴. Defaults to `True`.
        grid (tuple, optional): 网格的单位长度. Defaults to (1, 1).
        nice_aspect_ratio (bool, optional): 坐标系是否匹配最佳长宽比. Defaults to `True`.
        width (int, optional): 当 `nice_aspect_ratio` 参数为 `True` 时, 定义绘图宽度. Defaults to `6`.
        save_as (str, optional): 存储生成图片的文件路径. Defaults to `""`.

    Raises:
        TypeError: 错误的图形类型
    """
    xs: Iterable[Any]
    ys: Iterable[Any]

    xs, ys = zip(*list(extract_vectors(objects)))

    max_x, max_y, min_x, min_y = (
        max(0, *xs), max(0, *ys), min(0, *xs), min(0, *ys)
    )

    if grid:
        x_padding = max(ceil(0.05 * (max_x - min_x)), grid[0])
        y_padding = max(ceil(0.05 * (max_y - min_y)), grid[1])

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
        # 绘制网格
        gca.set_xticks(np.arange(x[0], x[1], grid[0]))
        gca.set_yticks(np.arange(y[0], y[1], grid[1]))
        plt.grid(  # type:ignore
            True,
            color="#aaa",
            linestyle=":",
            linewidth=0.5,
        )

        gca.set_axisbelow(True)

    if axes:
        # 绘制坐标轴
        gca.axhline(linewidth=2, color="k")
        gca.axvline(linewidth=2, color="k")

    for o in objects:
        if isinstance(o, Polygon):
            # 绘制多边形
            for i in range(0, len(o.vertices)):
                x1, y1 = o.vertices[i]
                x2, y2 = o.vertices[(i + 1) % len(o.vertices)]

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

            if o.show_coord:
                for x, y in zip(xs, ys):
                    plt.text(  # type: ignore
                        x,
                        y,
                        f"({x}, {y})",
                        fontsize=15,
                        verticalalignment="top",
                        horizontalalignment="right",
                    )

        elif isinstance(o, Arrow):
            # 绘制箭头
            tip, tail = o.tip, o.tail
            tip_length = (x[1] - x[0]) / 20.

            length = sqrt((tip[1] - tail[1]) ** 2 + (tip[0] - tail[0]) ** 2)
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


class LineStyle(Enum):
    """
    绘制线条的样式
    """
    solid = "solid"  # 实线
    dashed = "dashed"  # 点划线


class Drawable3D(Drawable):
    """
    所有 3D 绘图的超类
    """


class Points3D(Drawable3D):
    """
    在 3D 坐标系中绘制一组点
    """

    def __init__(self, *vectors: Vector3D, color=Color.black) -> None:
        """
        初始化对象, 设置三维点的坐标

        Args:
            vectors (Tuple[Vector3D]): 三维点坐标集合
            color (Color, optional): 绘图颜色. Defaults to `Color.black`.
        """
        super().__init__(color)
        self.vectors = list(vectors)


class Polygon3D(Drawable3D):
    """
    在 3D 坐标系中绘制一个多边形
    """

    def __init__(self, *vertices: Vector3D, color=Color.blue) -> None:
        """
        初始化对象, 设置三维多边形的顶点坐标

        Args:
            vertices (Tuple[Vector3D]): 三维多边形的顶点坐标
            color (Color, optional): 绘图颜色. Defaults to `Color.blue`.
        """
        super().__init__(color)
        self.vertices = vertices


class Arrow3D(Drawable3D):
    """
    在 3D 坐标系中绘制一个箭头
    """

    def __init__(self, tip: Vector3D, tail: Vector3D = (0, 0, 0), color=Color.red) -> None:
        """
        初始化对象, 设置箭头的起始和终止坐标

        Args:
            tip (Vector3D): 箭头起始坐标
            tail (Vector3D): 箭头终止坐标
            color (Color, optional): 绘图颜色. Defaults to `Color.red`.
        """
        super().__init__(color)
        self.tip = tip
        self.tail = tail


class Segment3D(Drawable3D):
    """
    在 3D 坐标系中绘制一条线段
    """

    def __init__(
        self,
        start_point: Vector3D,
        end_point: Vector3D,
        color=Color.blue,
        linestyle=LineStyle.solid,
    ) -> None:
        """
        初始化对象, 设置箭头的起始和终止坐标

        Args:
            start_point (Vector3D): 箭头起始坐标
            end_point (Vector3D): 箭头终止坐标
            color (Color, optional): 绘图颜色. Defaults to `Color.blue`.
            linestyle (LineStyle, optional): 线的样式. Defaults to `LineStyle.solid`.
        """
        super().__init__(color)
        self.start_point = start_point
        self.end_point = end_point
        self.linestyle = linestyle.value


class Box3D(Drawable3D):
    """
    在 3D 坐标系中绘制顶点和坐标轴组成的立方体

    三维空间的任意点都可以和三个坐标轴组成一个立方体
    """

    def __init__(self, *vector: Number, color=Color.gray) -> None:
        """
        初始化对象, 设置立方体在空间的点

        Args:
            vector (Tuple[Number]): 三维坐标分量, 依次为 `x`, `y` 和 `z`
            color (Color, optional): 绘图颜色. Defaults to `Color.gray`.
        """
        super().__init__(color)
        self.vector = cast(Vector3D, vector)


def extract_vectors_3D(objects: Iterable[Drawable3D]) -> Generator[Vector3D, None, None]:
    """
    将三维绘图对象展开三维向量

    将向量展开为一组 `Vector3D` 对象的序列 (生成器), 用于绘图时获取每个点

    Args:
        objects (Iterable[Drawable]): 三维绘图对象集合

    Raises:
        TypeError: 无效的绘图类型

    Yields:
        Generator[Vector3D, None, None]: 三维坐标点生成器
    """
    for o in objects:  # 遍历所有绘图对象, 逐一展开向量
        if isinstance(o, Polygon3D):
            # 针对三维多边形, 将每个顶点向量展开
            for v in o.vertices:
                yield v

        elif isinstance(o, Points3D):
            # 针对三维点集合, 将每个点向量展开
            for v in o.vectors:
                yield v

        elif isinstance(o, Arrow3D):
            # 针对三维箭头, 展开起始点坐标和终结点坐标
            yield o.tip
            yield o.tail

        elif isinstance(o, Segment3D):
            # 针对三维线段, 展开起始点坐标和终结点坐标
            yield o.start_point
            yield o.end_point

        elif isinstance(o, Box3D):
            # 针对三维立方体, 展开立方体顶点坐标
            yield o.vector

        else:
            raise TypeError(f"Unrecognized object: {o}")


class FancyArrow3D(FancyArrowPatch):
    """
    三维箭头类
    """

    def __init__(
        self,
        xs: Tuple[Number, Number],
        ys: Tuple[Number, Number],
        zs: Tuple[Number, Number],
        *args, **kwargs,
    ) -> None:
        """
        初始化对象

        Args:
            xs (Tuple[Number, Number]): 箭头在 `x` 轴的起止坐标
            ys (Tuple[Number, Number]): 箭头在 `y` 轴的起止坐标
            zs (Tuple[Number, Number]): 箭头在 `z` 轴的起止坐标

            其它附加参数, 如:
            - `mutation_scale`: 箭头的大小
            - `arrowstyle`: 箭头样式, 默认为 `-|>`
            - `color`: 箭头颜色
        """
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = (xs, ys, zs)

    def do_3d_projection(self, renderer=None) -> Number:
        """
        绘制 3D 图形
        """
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)

        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs)


def draw3d(
    *objects: Drawable3D,
    origin=True,
    axes=True,
    elev: Optional[float] = None,
    azim: Optional[float] = None,
    xlim: Optional[Tuple[Number, Number]] = None,
    ylim: Optional[Tuple[Number, Number]] = None,
    zlim: Optional[Tuple[Number, Number]] = None,
    xticks: Optional[List[Number]] = None,
    yticks: Optional[List[Number]] = None,
    zticks: Optional[List[Number]] = None,
    depthshade=False,
    save_as="",
) -> None:
    """
    绘制三维图形

    Args:
        objects (Tuple[Drawable3D]): 要绘制的三维图形.
        origin (bool, optional): 是否绘制原点. Defaults to `True`.
        axes (bool, optional): 是否绘制坐标轴. Defaults to `True`.
        elev (Optional[float], optional): 垂直方向的仰角. Defaults to `None`.
        azim (Optional[float], optional): 水平方向的方位角. Defaults to `None`.
        xlim (Optional[Tuple[Number, Number]], optional): `x` 轴的范围. Defaults to `None`.
        ylim (Optional[Tuple[Number, Number]], optional): `y` 轴的范围. Defaults to `None`.
        zlim (Optional[Tuple[Number, Number]], optional): `z` 轴的范围. Defaults to `None`.
        xticks (Optional[List[Number]], optional): `x` 轴的刻度值. Defaults to `None`.
        yticks (Optional[List[Number]], optional): `y` 轴的刻度值. Defaults to `None`.
        zticks (Optional[List[Number]], optional): `z` 轴的刻度值. Defaults to `None`.
        depthshade (bool, optional): 是否绘制深度. Defaults to `False`.
        save_as (str, optional): 存储图片的路径. Defaults to `""`.

    Raises:
        TypeError: 要绘制的三维图形不被支持
    """
    # 创建 Figure 对象
    fig = plt.figure(figsize=(6, 6))  # type: ignore

    # 创建三维坐标系
    ax: Axes3D = fig.add_subplot(111, projection="3d")

    # 初始化视图, 设置视图的仰角, 水平的方位角以及旋转轴
    ax.view_init(
        elev=elev,  # 设置垂直仰角
        azim=azim,  # 设置水平方位角
        vertical_axis="z",  # 要垂直对齐的轴, 默认为 'z' 轴
    )

    all_vectors = list(extract_vectors_3D(objects))
    if origin:
        all_vectors.append((0, 0, 0))

    xs, ys, zs = zip(*all_vectors)

    max_x, min_x = max(0, *xs), min(0, *xs)
    max_y, min_y = max(0, *ys), min(0, *ys)
    max_z, min_z = max(0, *zs), min(0, *zs)

    x_size = max_x - min_x
    y_size = max_y - min_y
    z_size = max_z - min_z

    padding_x = 0.05 * x_size if x_size else 1
    padding_y = 0.05 * y_size if y_size else 1
    padding_z = 0.05 * z_size if z_size else 1

    plot_x_range = (min(min_x - padding_x, -2), max(max_x + padding_x, 2))
    plot_y_range = (min(min_y - padding_y, -2), max(max_y + padding_y, 2))
    plot_z_range = (min(min_z - padding_z, -2), max(max_z + padding_z, 2))

    # 绘制坐标轴的标签
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    def draw_segment(
        start: Vector3D,
        end: Vector3D,
        color=Color.black.value,
        linestyle=LineStyle.solid.value,
    ) -> None:
        """
        绘制线段

        Args:
            start (Vector3D): 线段的起始三维坐标
            end (Vector3D): 线段的终止三维坐标
            color (str, optional): 线段的颜色. Defaults to `Color.black.value`.
            linestyle (str, optional): 线段样式. Defaults to `LineStyle.solid.value`.
        """
        # 将线段的起始终止坐标转为三个坐标轴的坐标值
        xs, ys, zs = [[start[i], end[i]] for i in range(0, 3)]
        # 绘制线段
        ax.plot(xs, ys, zs, color=color, linestyle=linestyle)

    # 判断是否需要绘制坐标轴
    if axes:
        # 绘制 x 坐标轴
        draw_segment(
            (plot_x_range[0], 0, 0),
            (plot_x_range[1], 0, 0),
        )

        # 绘制 y 坐标轴
        draw_segment(
            (0, plot_y_range[0], 0),
            (0, plot_y_range[1], 0),
        )

        # 绘制 z 坐标轴
        draw_segment(
            (0, 0, plot_z_range[0]),
            (0, 0, plot_z_range[1]),
        )

    # 判断是否绘制原点
    if origin:
        # 绘制原点
        ax.scatter([0], [0], [0], color="k", marker="x")

    # 绘制各个三维图形
    for o in objects:
        if isinstance(o, Points3D):
            # 绘制三维点
            xs, ys, zs = zip(*o.vectors)
            ax.scatter(xs, ys, zs, color=o.color, depthshade=depthshade)

        elif isinstance(o, Polygon3D):
            # 绘制三维多边形
            for i in range(0, len(o.vertices)):
                draw_segment(
                    o.vertices[i],
                    o.vertices[(i+1) % len(o.vertices)],
                    color=o.color,
                )

        elif isinstance(o, Arrow3D):
            # 绘制三维箭头
            xs, ys, zs = zip(o.tail, o.tip)
            a = FancyArrow3D(
                xs, ys, zs,
                mutation_scale=20,
                arrowstyle="-|>",
                color=o.color,
            )
            ax.add_artist(a)

        elif isinstance(o, Segment3D):
            # 绘制三维线段
            draw_segment(
                o.start_point,
                o.end_point,
                color=o.color,
                linestyle=o.linestyle,
            )

        elif isinstance(o, Box3D):
            # 绘制三维盒子
            x, y, z = o.vector
            kwargs = {
                "linestyle": "dashed",
                "color": o.color,
            }
            draw_segment((0, y, 0), (x, y, 0), **kwargs)
            draw_segment((0, 0, z), (0, y, z), **kwargs)
            draw_segment((0, 0, z), (x, 0, z), **kwargs)
            draw_segment((0, y, 0), (0, y, z), **kwargs)
            draw_segment((x, 0, 0), (x, y, 0), **kwargs)
            draw_segment((x, 0, 0), (x, 0, z), **kwargs)
            draw_segment((0, y, z), (x, y, z), **kwargs)
            draw_segment((x, 0, z), (x, y, z), **kwargs)
            draw_segment((x, y, 0), (x, y, z), **kwargs)

        else:
            raise TypeError(f"Unrecognized object: {o}")

    # 设置坐标轴范围
    if xlim and ylim and zlim:
        plt.xlim(*xlim)  # 设置 x 轴的范围
        plt.ylim(*ylim)  # 设置 y 轴的范围
        ax.set_zlim(*zlim)  # 设置 z 轴的范围

    # 设置坐标轴的刻度
    if xticks and yticks and zticks:
        plt.xticks(xticks)  # 设置 x 轴刻度
        plt.yticks(yticks)  # 设置 y 轴刻度
        ax.set_zticks(zticks)  # 设置 z 轴刻度

    # 是否保存图形
    if save_as:
        plt.savefig(save_as)

    # 显示图形
    plt.show()
