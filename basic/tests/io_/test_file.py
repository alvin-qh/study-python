"""`open(file_name, open_mode[, buffering, encoding) -> file`

该函数用于打开一个文件, 参数为:
    - `file_name` 参数用于指定文件的路径和名称
    - `open_mode` 参数是一个字符串，表示打开文件的方式，所有的方式如下
        - `"r"` 以只读方式打开文件 (默认)
        - `"w"` 以读写方式打开文件, 且会清空文件原有内容
        - `"x"` 以独占方式打开文件, 若文件已存在则失败
        - `"a"` 以读写方式打开文件, 在原有内容后追加
        - `"b"` 以二进制方式打开文件
        - `"t"` 以文本方式打开文件 (默认)
        - `"+"` 以更新方式打开文件 (可读写)

对于 Python3 来说，"binary mode" 和 "text mode" 的区别如下：
    - 在读取文件时对换行符号的处理上，"text mode" 会处理换行符
    - "text mode" 不支持文件指针的 "相对位置" 操作

`file::write(str/bytes) -> int`, 写入指定字符串 (或字节串)
`file::read(length) -> str/bytes`, 读取指定数量的字符 (或字节)，返回字符串或字节集合
"""

import linecache
import os
import sys
import tempfile
import zipfile

# 操作的文件名
FILENAME = "file_test.txt"


def teardown_function() -> None:
    """每个测试结束后, 删除测试文件"""

    if os.path.exists(FILENAME):
        os.remove(FILENAME)


def test_open_file_as_text_mode() -> None:
    """测试以默认的文本方式打开文件"""

    # 以读写方式打开文件
    with open(FILENAME, "w", encoding="gbk") as fp:
        # 判断打开文件的文件名
        assert fp.name == FILENAME
        # 判断打开的文件是否可写
        assert fp.writable() is True

        # 写入文件
        n = fp.write("Hello World\n")
        # 写入后文件长度
        assert n == 12

        # 写入多行内容
        fp.writelines(["a\n", "b\n", "c\n", "d\n"])
        # 查看文件指针位置
        assert fp.tell() == 20

    # 获取文件大小
    n = os.path.getsize(FILENAME)
    assert n == 20

    # 以只读方式打开文件
    with open(FILENAME, "r", encoding="gbk") as fp:
        # 判断打开文件的文件名
        assert fp.name == FILENAME
        # 判断打开的文件是否可写
        assert fp.writable() is False

        # 从文件开头处读取文件 11 个字节
        r = fp.read(11)
        assert r == "Hello World"

        # seek(offset, whence) 方法用于移动文件指针
        # 对于文本方式打开的文件, 只能使用 offset 参数

        # tell 方法获取当前文件指针
        # seek 方法移动文件指针, 文件指针向后移动 1 字节
        n = fp.seek(fp.tell() + 1)
        assert n == 12

        # 从当前位置再读区 1 字节
        r = fp.read(1)
        assert r == "a"

        # 文件指针向后移动 1 字节
        n = fp.seek(fp.tell() + 1)
        assert n == 14

        # 从当前位置读取剩余部分
        r = fp.read()
        assert r == "b\nc\nd\n"


def test_open_file_as_binary_mode() -> None:
    """测试以二进制方式打开文件"""

    with open(FILENAME, "wb") as fp:
        # 判断打开文件的文件名
        assert fp.name == FILENAME
        # 判断打开的文件是否可写
        assert fp.writable() is True

        n = fp.write("Hello World\n".encode())
        assert n == 12

        # 写入多行内容
        fp.writelines(s.encode() for s in ["a\n", "b\n", "c\n", "d\n"])
        # 查看文件指针位置
        assert fp.tell() == 20

    # 获取文件大小
    n = os.path.getsize(FILENAME)
    assert n == 20

    # 以只读方式打开文件
    with open(FILENAME, "rb") as fp:
        # 判断打开文件的文件名
        assert fp.name == FILENAME
        # 判断打开的文件是否可写
        assert fp.writable() is False

        r = [s.decode() for s in fp.readlines()]
        assert r == [
            "Hello World\n",
            "a\n",
            "b\n",
            "c\n",
            "d\n",
        ]

        # seek(offset, whence) 方法用于移动文件指针
        # 对于二进制方式打开的文件, 可以使用 offset 参数和 whence 参数
        # whence 参数取值为 os.SEEK_SET (0), os.SEEK_CUR (1) 和 os.SEEK_END (2)

        # 从文件起始位置移动指针 12 字节
        n = fp.seek(12, os.SEEK_SET)
        assert n == 12

        # 从文件指针位置读取剩余内容
        r = [s.decode() for s in fp.readlines()]
        assert r == ["a\n", "b\n", "c\n", "d\n"]


def test_line_cache() -> None:
    """测试文件行缓存

    按文件名按行对文件内容进行缓存, 并在读取的时候从缓存中进行

    仅对于需要频繁读取的文件操作需要
    """
    # 产生 5 行数据并写入文件
    lines = ["{}\n".format(n) for n in range(1, 6)]
    with open(FILENAME, "w", encoding="utf8") as fp:
        fp.writelines(lines)

    # 从 cache 中读取第 1 行数据
    line = linecache.getline(FILENAME, 1)
    assert line == "1\n"

    # 从 cache 中读取所有行数据
    lines = linecache.getlines(FILENAME)
    assert lines == ["1\n", "2\n", "3\n", "4\n", "5\n"]

    # 清空 cache 内容
    linecache.clearcache()


def test_temp_file() -> None:
    """测试操作临时文件"""

    # 创建临时文件
    h, fn = tempfile.mkstemp(".zip")
    # 关闭文件句柄
    os.close(h)

    assert os.path.splitext(fn)[1] == ".zip"

    # 定义一段 python 代码
    code = """
def func():
    return "test"
"""

    # 将 python 代码压缩后写入文件
    with zipfile.ZipFile(fn, "w") as zf:
        zf.writestr("tmp/test_temp.py", code, zipfile.ZIP_DEFLATED)

    try:
        # 把临时文件插入系统搜索路径中
        sys.path.insert(0, fn)

        # 导入压缩文件中的 tmp/test_temp 模块
        module = __import__("tmp/test_temp")
        # 执行模块中定义的函数
        assert module.func() == "test"
    finally:
        # 取消文件连接, 此时临时文件会自动删除
        os.unlink(fn)
        assert os.path.exists(fn) is False
