import matplotlib.pyplot as plt

from ..common import render_axis


def test_draw_line() -> None:
    xp = (0, 6)
    yp = (0, 100)

    render_axis(xp, yp, grid=(1, 20))

    plt.plot(xp, yp)
    plt.show()
