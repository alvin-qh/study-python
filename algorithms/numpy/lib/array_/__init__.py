import numpy as np


def arange_by_shape(shape: tuple[int, ...], start: int, step: int = 1) -> np.ndarray:
    return np.arange(start, start + np.prod(shape) * step, step).reshape(shape)
