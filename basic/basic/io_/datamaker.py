import struct


def make_bytes_data_from_nums(min_num: int = 0, max_num: int = 1000) -> bytes:
    """产生一组数据用于测试

    Returns:
        `bytes`: 产生的数据集合
    """
    data = bytearray()

    for n in range(min_num, max_num):
        data += struct.pack("i", n)

    return bytes(data)
