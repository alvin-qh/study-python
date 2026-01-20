import random


def generate_data(
    size: int = 1024 * 1024,
    charset: bytes = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]|;:,./<>?~",
) -> bytes:
    """产生指定长度的随机字节串

    Args:
        `size` (`int`, optional): 结果字节串长度. Defaults to 1024*1024
        `charset` (`bytes`, optional): 产生随机字节串内容的字符集

    Returns:
        `bytes`: 随机字节串
    """
    return bytes(random.choice(charset) for _ in range(size))
