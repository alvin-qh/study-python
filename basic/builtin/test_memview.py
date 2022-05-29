from pytest import raises


def test_memoryview() -> None:
    """
    `memoryview` 对一个 `ReadableBuffer` 对象进行包装 (`bytes`, `bytearray` 类型),
    可以对这部分内存进行直接访问
    """
    # 创建一个可读写的 memoryview 对象
    # 基于 bytearray 类型的 memoryview 可读写
    # 基于 bytes 类型的 memoryview 只读
    mv = memoryview(bytearray(b"abcdef"))
    # mv = memoryview(b"abcdef")  # 只读的 memoryview 对象

    # 整体包含了 6 个字节
    assert mv.nbytes == 6

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
