import io

# "流" 处理指的是处理连续数据, 包括文件流, 网络流, 管道流等
# Python 将流抽象为一个对象, 并且提供了一系列方法来操作流对象, 包括:
# - 创建流对象
# - 读取流数据: 包括 `.read`, `.readline`, `.readlines` 方法
# - 写入流数据: 包括 `.write`, `.writelines` 方法
# - 移动指针: 包括 `.seek`, `.tell` 方法
# - 关闭流对象: 包括 `.close` 方法


def test_bytes_io_stream() -> None:
    """测试内存字节流

    `io.BytesIO` 类用于在内存中创建一个字节流对象, 可以像操作文件一样操作这个字节流对象
    """
    # 创建一个内存字节流对象
    with io.BytesIO() as s:
        # 向内存字节流写入数据
        s.write(b"Hello World, ")
        s.write(b"You are awesome!")

        # 将内存字节流的指针移动到开头, 以便可以从头读取数据
        s.seek(io.SEEK_SET)

        # 读取内存字节流数据
        data = s.read()

    # 确认读取的数据正确
    assert data == b"Hello World, You are awesome!"


def test_read_bytes_by_stream() -> None:
    """测试读取字节流数据

    字节流的一个重要应用, 就是读取一块连续内存中的数据, 相比于通过集合的随机访问方式, 流访问方式速度更快, 占用内存更少
    """

    # 创建一个字节串
    data = b"Hello World,\nYou are awesome!"

    # 在字节串基础上, 创建一个字节流对象
    with io.BytesIO(data) as s:
        # 读取字节流的第一个字节
        r = s.read(1)
        assert r == b"H"

        # 再读取两个字节
        r = s.read(2)
        assert r == b"el"

        # 读取到本行末尾hang
        r = s.readline()
        assert r == b"lo World,\n"

        # 移动指针到开头
        s.seek(io.SEEK_SET)

        # 读取多行数据
        rs = s.readlines()
        assert rs == [b"Hello World,\n", b"You are awesome!"]

        # 移动指针到开头
        s.seek(io.SEEK_SET)

        # 读取流中的所有数据
        r = s.read()
        assert r == data


def test_string_io_stream() -> None:
    """测试内存字符串流

    `io.StringIO` 类用于在内存中创建一个字符串流对象, 可以像操作文件一样操作这个字符串流对象
    """
    # 创建一个内存字符串流对象
    with io.StringIO() as s:
        # 向内存字符串流写入数据
        s.write("Hello World, ")
        s.write("You are awesome!")

        # 将内存字符串流的指针移动到开头, 以便可以从头读取数据
        s.seek(0)

        # 读取内存字符串流数据
        text = s.read()

    # 确认读取的数据正确
    assert text == "Hello World, You are awesome!"


def test_read_string_by_stream() -> None:
    """测试读取字符串流数据

    字符串流和字节流一样, 也可以用来读取一块连续内存中的数据, 速度更快, 占用内存更少
    """

    # 创建一个字节串
    str = "Hello World,\nYou are awesome!"

    # 在字节串基础上, 创建一个字节流对象
    with io.StringIO(str) as s:
        # 读取字节流的第一个字符
        r = s.read(1)
        assert r == "H"

        # 再读取两个字符
        r = s.read(2)
        assert r == "el"

        # 读取到本行末尾
        r = s.readline()
        assert r == "lo World,\n"

        # 移动指针到开头
        s.seek(io.SEEK_SET)

        # 读取多行数据
        rs = s.readlines()
        assert rs == ["Hello World,\n", "You are awesome!"]

        # 移动指针到开头
        s.seek(io.SEEK_SET)

        # 读取流中的所有字符
        r = s.read()
        assert r == str
