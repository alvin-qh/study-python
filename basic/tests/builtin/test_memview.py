from array import array

from pytest import raises


def test_memoryview() -> None:
    """`memoryview` 对一个 `ReadableBuffer` 对象进行包装 (`bytes`, `bytearray` 类型),
    可以对这部分内存进行直接访问 (内存视图)
    """
    # 创建一个可读写的 memoryview 对象
    # 基于 bytearray 类型的 memoryview 可读写
    # 基于 bytes 类型的 memoryview 只读
    mv = memoryview(bytearray(b"abcdef"))
    # mv = memoryview(b"abcdef")  # 只读的 memoryview 对象

    # 整体包含了 6 个字节
    assert mv.nbytes == 6
    # 每项 1 个字节
    assert mv.itemsize == 1

    # 每个字节的内容
    assert mv[0] == 97
    assert mv[1] == 98

    # tobytes 方法返回一个内存内容的字节串
    assert mv[0:4].tobytes() == b"abcd"

    # tolist 方法返回内存内容的字节列表集合
    assert mv.tolist() == [97, 98, 99, 100, 101, 102]

    # 可以对可读写的 memoryview 对象进行修改操作
    mv[-1] = ord("x")
    assert mv.tolist() == [97, 98, 99, 100, 101, 120]

    # 获取只读的 memoryview 对象
    mv_r = mv.toreadonly()
    # 只读 memoryview 内容不变
    assert mv_r == mv

    # 只读 memoryview 不支持修改
    with raises(TypeError):
        mv_r[-1] = ord("f")


def test_memoryview_cast() -> None:
    """将内存从一种视图类型转为另一种, 而无需内存复制"""
    # 创建一个整数数组并用 memoryview 对象包装
    mv_i = memoryview(array("i", range(10)))
    # 此时 memoryview 对象共 40 字节
    assert mv_i.nbytes == 40
    # 每一项 4 字节 (一个整型)
    assert mv_i.itemsize == 4
    # 内容为 10 个整数
    assert mv_i.tolist() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # 将 memoryview 对象内容转为 byte 类型
    mv_b = mv_i.cast("B")
    # 仍为 40 字节
    assert mv_b.nbytes == 40
    # 每一项 1 字节 (一个 byte)
    assert mv_b.itemsize == 1
    # 内容为 40 个 byte (10 个整数转换而来)
    assert mv_b.tolist() == [
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        2,
        0,
        0,
        0,
        3,
        0,
        0,
        0,
        4,
        0,
        0,
        0,
        5,
        0,
        0,
        0,
        6,
        0,
        0,
        0,
        7,
        0,
        0,
        0,
        8,
        0,
        0,
        0,
        9,
        0,
        0,
        0,
    ]
