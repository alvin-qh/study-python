import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style


def test_animated_plot() -> None:
    style.use("fivethirtyeight")

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    def animate(i: int) -> None:
        xs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ys = np.random.randint(0, 20, size=10)

        ax.clear()
        ax.plot(xs, ys)

    ani = animation.FuncAnimation(fig, animate, interval=500)

    plt.show()
