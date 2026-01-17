import random
from typing import Sequence


def generate_large_string(
    length: int,
    charset: Sequence[str] = "abcdefgABCDEFG0123456789",
) -> str:
    """根据所给长度生成任意字符串

    Args:
        `length` (`int`): 期望的字符串长度

    Returns:
        `str`: 返回生成的字符串
    """
    return "".join(random.choice(charset) for _ in range(length))
