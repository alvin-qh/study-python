from enum import Enum
from math import ceil, floor, sqrt
from typing import Iterable, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np

Number = Union[int, float]
Point = Tuple[Number, Number]


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


class Shape:
    def __init__(self, color: Color) -> None:
        self.color = color.value


class Polygon(Shape):
    def __init__(self, *vertices: Point, color=Color.blue, fill=None, alpha=0.4) -> None:
        super().__init__(color)

        self.vertices = vertices
        self.fill = fill
        self.alpha = alpha


class Points(Shape):
    def __init__(self, *vectors: Point, color=Color.black):
        super().__init__(color)

        self.vectors = list(vectors)


class Arrow(Shape):
    def __init__(self, tip, tail=(0, 0), color=Color.red):
        super().__init__(color)

        self.tip = tip
        self.tail = tail


class Segment(Shape):
    def __init__(self, start_point, end_point, color=Color.blue):
        super().__init__(color)

        self.start_point = start_point
        self.end_point = end_point


def extract_vectors(objects: Iterable[Shape]):
    for o in objects:
        if isinstance(o, Polygon):
            for v in o.vertices:
                yield v

        elif isinstance(o, Points):
            for v in o.vectors:
                yield v

        elif isinstance(o, Arrow):
            yield o.tip
            yield o.tail

        elif isinstance(o, Segment):
            yield o.start_point
            yield o.end_point

        else:
            raise TypeError(f"Unrecognized object: {o}")


def draw(
    *objects: Shape,
    origin=True,
    axes=True,
    grid=(1, 1),
    nice_aspect_ratio=True,
    width=6,
    save_as=None,
) -> None:
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
            for i in range(0, len(o.vertices)):
                x1, y1 = o.vertices[i]
                x2, y2 = o.vertices[(i+1) % len(o.vertices)]

                plt.plot([x1, x2], [y1, y2], color=o.color)

            if o.fill:
                xs = [v[0] for v in o.vertices]
                ys = [v[1] for v in o.vertices]
                gca.fill(xs, ys, o.fill, alpha=o.alpha)

        elif isinstance(o, Points):
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
            x1, y1 = o.start_point
            x2, y2 = o.end_point
            plt.plot([x1, x2], [y1, y2], color=o.color)

        else:
            raise TypeError(f"Unrecognized object: {o}")

    if nice_aspect_ratio:
        coords_height = (y[1] - y[0])
        coords_width = (x[1] - x[0])

        plt.gcf().set_size_inches(  # type: ignore
            width, width * coords_height / coords_width,
        )

    if save_as:
        plt.savefig(save_as)

    plt.show()
