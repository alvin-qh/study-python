import numpy as np


def arange_by_shape(start: int, shape: tuple[int, ...], step: int = 1) -> np.ndarray:
    return np.arange(start, start + np.prod(shape) * step, step).reshape(shape)
