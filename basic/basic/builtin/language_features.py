from typing import Any


def check_value_if_true(val: Any) -> str:
    """检查值是否为真

    Args:
        - `val` (`Any`): 待检查的值

    Returns:
        `str`: 如果值为真, 则返回 "True", 否则返回 "False"
    """
    # 检查值是否为真, 如果值表示真, 则返回 "True", 否则返回 "False"
    if val:
        return "True"
    else:
        return "False"
