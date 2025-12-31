from typing import Any

import numpy as np


def aprint(propmpt: str, /, values: dict[str, Any], show_shapes: bool = True) -> None:
    """打印提示信息和字典格式的值, 对 numpy 数组和矩阵额外显示形状信息

    Args:
        `propmpt` (`str`): 要打印的提示信息
        `values` (`dict[str, Any]`): 包含要打印的键值对的字典
        `show_shapes` (`bool`, optional): 是否显示数组的形状, 默认为 `True`
    Returns:
        `None`
    """
    print(f"{propmpt}")
    prefix = "▶️"
    for key, value in values.items():
        print(f"{prefix} {key}:")
        print(f"{value}", end="")
        if isinstance(value, (np.ndarray, np.matrix)) and show_shapes:
            print(f", shape={value.shape}")
        else:
            print()
        prefix = "✅"
