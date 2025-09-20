import numpy as np


def arange_by_shape(shape: tuple[int, ...], start: int, step: int = 1) -> np.ndarray:
    """根据给定的形状创建一个等差数组

    该函数首先根据起始值和步长生成一个足够长的等差数列, 然后将其重新塑形为指定的形状

    Args:
        `shape` (`tuple[int, ...]`): 指定输出数组的形状
        `start` (`int`): 等差数列的起始值。
        `step` (`int`, optional): 等差数列的步长, 默认为 `1`

    Returns:
        `np.ndarray`: 按照指定形状reshape后的等差数组。
    """
    return np.arange(start, start + np.prod(shape) * step, step).reshape(shape)
