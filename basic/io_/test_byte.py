import binascii

from io_.crc64 import crc64_long


def test_bytes_and_bytearray() -> None:
    """
    bytes 对象表示一个无法修改的字节串
    bytearray 表示一个可以修改的字节串
    """
    # 定义一个 bytes 类型的串
    bs = b"Hello Python"
    assert isinstance(bs, bytes)
    # 字节串转为字符串
    assert bs.hex() == "48656c6c6f20507974686f6e"

    # 定义一个 bytearray 类型的串
    ba = bytearray(bs)
    assert isinstance(ba, bytearray)
    # 字节串转为字符串
    assert ba.hex() == "48656c6c6f20507974686f6e"

    # 两个串内容相同
    assert bs == ba

    # 字符串转为字节串
    bs = bytes.fromhex("48656c6c6f20507974686f6e")
    ba = bytearray.fromhex("48656c6c6f20507974686f6e")
    assert bs == ba

    # bytearray 可以修改
    ba = bytearray()
    for n in range(ord("A"), ord("A") + 6):
        ba.append(n)

    assert ba == b"ABCDEF"


def test_encode_and_decode() -> None:
    """
    测试字符串的编码和解码
    """

    s = "大家好"

    # 字符串编码
    bs = bytes(s, "utf8")
    assert bs == s.encode("utf8")

    # 字符串编码
    ba = bytearray(s, "utf8")
    assert bs == ba

    # 字符串解码
    assert bs.decode("utf8") == "大家好"
    assert ba.decode("utf8") == "大家好"


def test_crc_32() -> None:
    """
    测试生成 crc32 校验码
    """

    # 生成 10 字节数据
    data = bytearray(range(1, 10))
    # 生成校验码
    crc = binascii.crc32(data) & 0xffffffff
    # 确认校验码
    assert crc == 1089448862

    # 修改 1 字节数据
    data[3] = 11
    # 生成校验码
    crc = binascii.crc32(data) & 0xffffffff
    # 生成不同的校验码
    assert crc == 2981697867


def test_crc_64() -> None:
    """
    测试生成 crc64 校验码
    """

    # 生成 10 字节数据
    data = bytearray(range(1, 10))
    # 生成校验码
    crc = crc64_long(data)
    # 确认校验码
    assert crc == 10283202504587125611

    # 修改 1 字节数据
    data[3] = 11
    # 生成校验码
    crc = crc64_long(data)
    # 生成不同的校验码
    assert crc == 10283202694909961067
