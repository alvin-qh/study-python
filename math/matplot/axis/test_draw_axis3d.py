from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np


def test_axis_grid() -> None:
    grid = (1, 1, 1)

    fig = plt.gcf()  # type: ignore

    ax = fig.add_subplot(111, projection="3d")
    ax.view_init(elev=None, azim=None)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    ax.set_zlim(-5, 5)

    x, y, z = plt.xlim(), plt.ylim(), ax.get_zlim()

    plt.xticks(np.arange(x[0], x[1], grid[0]))
    plt.yticks(np.arange(y[0], y[1], grid[1]))
    ax.set_zticks(np.arange(z[0], z[1], grid[2]))

    ax.scatter([0], [0], [0], color="k", marker="x")

    def draw_line(
        start: Tuple[float, float, float],
        end: Tuple[float, float, float],
    ) -> None:
        xs, ys, zs = [(start[i], end[i]) for i in range(0, 3)]
        ax.plot(xs, ys, zs, color="k", linestyle=":")

    draw_line((-5, 0, 0), (5, 0, 0))
    draw_line((0, -5, 0), (0, 5, 0))
    draw_line((0, 0, -5), (0, 0, 5))

    draw_line((-5, 0, 5), (-5, 0, -5))
    draw_line((-5, 0, 5), (5, 5, 0))
    draw_line((5, 5, 0), (5, 5, 0))

    plt.show()
