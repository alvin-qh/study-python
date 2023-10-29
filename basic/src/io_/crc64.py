from typing import List, Tuple


def init_crc64_tables(
    crc_table_h: List[int],
    crc_table_l: List[int],
    poly64_rev_h: int,
    bit_toggle: int,
) -> None:
    """
    生成 crc64 计算辅助表, 该表分为 高位表 和 低位表

    Args:
        crc_table_h (List[int]): 保存计算表高位数据
        crc_table_l (List[int]): 保存计算表低位数据
        poly64_rev_h (int): 生成多项式 (假设低 `32` 位为 `0`)
        bit_toggle (int): 掩码
    """
    for i in range(256):
        part_l = i
        part_h = 0

        for _ in range(8):
            r_flag = part_l & 1
            part_l >>= 1

            if part_h & 1:
                part_l ^= bit_toggle

            part_h >>= 1
            if r_flag:
                part_h ^= poly64_rev_h

        crc_table_h[i] = part_h
        crc_table_l[i] = part_l


CRC64_TABLE_H = [0] * 256
CRC64_TABLE_L = [0] * 256

init_crc64_tables(
    crc_table_h=CRC64_TABLE_H,
    crc_table_l=CRC64_TABLE_L,
    poly64_rev_h=0xd8000000,
    bit_toggle=1 << 31,
)


def crc64(data: bytes | bytearray, crc_h: int = 0, crc_l: int = 0) -> Tuple[int, int]:
    """
    计算 crc64

    Args:
        data (bytes | bytearray): 用来计算 CRC 的数据
        crc_h (int, optional): 高位初始值. Defaults to `0`.
        crc_l (int, optional): 低位初始值. Defaults to `0`.

    Returns:
        Tuple[int, int]: 返回 crc64 结果的高低位
    """

    if isinstance(data, bytearray):
        data = bytes(data)

    for b in str(data):
        shr = (crc_h & 0xFF) << 24
        temp_h = crc_h >> 8
        temp_l = (crc_l >> 8) | shr
        table_index = (crc_l ^ ord(b)) & 0xFF
        crc_h = temp_h ^ CRC64_TABLE_H[table_index]
        crc_l = temp_l ^ CRC64_TABLE_L[table_index]

    return crc_h, crc_l


def crc64_long(data: bytes | bytearray, crc_val: int = 0) -> int:
    """
    计算 CRC64 值, 并返回 `long` 类型结果

    Args:
        data (bytes | bytearray): 用来计算 CRC64 的数据
        crc_val (int, optional): CRC64 初始值. Defaults to `0`.

    Returns:
        int: crc64 值
    """
    crc_h, crc_l = crc64(
        data,
        (crc_val & 0xFFFFFFFF00000000) >> 32,
        crc_val & 0x00000000FFFFFFFF,
    )
    return int(crc_h) << 32 | crc_l
