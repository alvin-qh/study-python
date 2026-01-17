import random


def generate_large_data(
    length: int,
    charset: bytes = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}|;:',.<>?/`~",
) -> bytes:
    """根据所给长度生成任意字符串

    Args:
        `length` (`int`): 期望的字节串长度

    Returns:
        `bytes`: 返回生成的字节串
    """
    return bytes([random.choice(charset) for _ in range(length)])
