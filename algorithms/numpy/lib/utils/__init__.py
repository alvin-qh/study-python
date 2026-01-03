from typing import Any

import numpy as np


def univariate_norm(arr: np.ndarray, mu: float, sigma: float) -> Any:
    """计算一元正态分布的概率密度函数值 (PDF)

    公式:
        f(x) = 1 / (sigma * sqrt(2*pi)) * exp(-((x-mu)**2) / (2*sigma**2))

    参数:
        `arr`: 输入数据，通常为一维 `numpy.ndarray`, 函数对数组中每个元素按元素计算 PDF (支持任意形状, 保留输入形状)
        `mu`: 均值 $\\mu$ (float), 分布中心位置
        `sigma`: 标准差 $\\sigma$ (float, 必须 > 0), 控制分布宽度 (方差为 $\\sigma^2$)

    返回:
        与 `arr` 形状相同的数组，包含对应位置的概率密度值（连续密度）。

    注意:
        - 返回的是概率密度而非区间概率; 要得到区间概率需对密度积分
        - 当 `sigma`<=0 时结果无意义或会触发除零, 应在调用前检查
        - 本函数使用 NumPy 向量化运算, 适合对数组进行高效批量计算
    """
    if sigma <= 0:
        raise ValueError("标准差 sigma 必须大于 0")

    return (
        1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-((arr - mu) ** 2) / (2 * sigma**2))
    )
