from typing import Literal


Unit = Literal["B", "KB", "MB", "GB", "TB"]


def convert_unit(size: int, from_unit: Unit = "B", to_unit: Unit = "KB") -> float:
    """在不同单位间转换数据大小

    Args:
        `size` (`int`): 原始数据大小
        `from_unit` (`str`, optional): 原始数据单位. Defaults to "B".
        `to_unit` (`str`, optional): 目标数据单位. Defaults to "KB".

    Returns:
        `float`: 转换后的数据大小
    """
    unit_map = {
        "B": 1,
        "KB": 1024,
        "MB": 1024**2,
        "GB": 1024**3,
        "TB": 1024**4,
    }

    if from_unit not in unit_map or to_unit not in unit_map:
        raise ValueError("Unsupported unit. Supported units are B, KB, MB, GB, TB.")

    size_in_bytes = size * unit_map[from_unit]
    converted_size = size_in_bytes / unit_map[to_unit]

    return converted_size
