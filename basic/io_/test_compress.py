import gzip
import os
import shutil
import struct
import zipfile
from datetime import datetime


def make_data() -> bytes:
    """
    产生一组数据用于测试

    Returns:
        bytes: 产生的数据集合
    """
    data = bytearray()

    # 遍历 1000 个整数
    for n in range(0, 1000):
        # 将整数逐个写入 byte 集合
        data += struct.pack("i", n)

    return bytes(data)


# 压缩文件名
ZIP_FILE = "demo.zip"

# 压缩文件内的存储节点名
ZIP_ENTRY1 = "data1/test.dat"
ZIP_ENTRY2 = "data2/test.dat"

# 解压文件的文件夹
UNZIP_TARGET_PATH = "_unzip"


def teardown_function() -> None:
    """
    每个测试结束后执行
    """
    # 删除测试文件
    if os.path.exists(ZIP_FILE):
        os.remove(ZIP_FILE)

    # 删除解压文件家
    if os.path.exists(UNZIP_TARGET_PATH):
        shutil.rmtree(UNZIP_TARGET_PATH)


def test_zip_unzip_data() -> None:
    """
    `zipfile` 包下 `ZipFile` 类对象表示一个压缩文件对象
    """
    # 产生一组数据
    data = make_data()
    now = datetime.now().timetuple()[:6]

    # 创建一个可写入的压缩文件对象, 使用 DEFLATED 算法
    with zipfile.ZipFile(ZIP_FILE, "w", zipfile.ZIP_DEFLATED) as zf:
        # 将数据写入压缩文件的指定节点
        zf.writestr(ZIP_ENTRY1, data)

        # 通过 ZipInfo 对象写入数据
        # ZipInfo 可为压缩数据节点赋予更多的属性, 包括创建时间, 文件权限等
        zi = zipfile.ZipInfo(ZIP_ENTRY2, date_time=now)
        zi.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(zi, data)

    # 确保压缩文件已产生
    assert os.path.exists(ZIP_FILE)

    # 压缩后为原尺寸的 1/2
    assert os.path.getsize(ZIP_FILE) < len(data)

    # 打开一个可读取的压缩文件对象
    with zipfile.ZipFile(ZIP_FILE, "r") as zf:
        # 测试压缩文件是否正确
        # 测试会读取所有压缩文件并对 CRC 进行验证, 失败会返回错误的数据节点名称
        assert zf.testzip() is None

        # 通过节点名称读取内容
        assert zf.read(ZIP_ENTRY1) == data
        assert zf.read(ZIP_ENTRY2) == data

        # 获取数据节点信息
        zi = zf.getinfo(ZIP_ENTRY1)
        assert zi.filename == ZIP_ENTRY1
        assert zi.CRC == zipfile.crc32(data)  # type: ignore # 判断文件的 crc 验证码

        # 获取数据节点信息
        zi = zf.getinfo(ZIP_ENTRY2)
        assert zi.filename == ZIP_ENTRY2
        assert zi.CRC == zipfile.crc32(data)  # type: ignore # 判断文件的 crc 验证码
        # 文件时间的秒有可能有一些误差, 所以比较到分钟部分
        assert zi.date_time[:5] == now[:5]

        # 遍历读取压缩文件中的所有数据节点
        for zi, name in zip(zf.filelist, [ZIP_ENTRY1, ZIP_ENTRY2]):
            assert zi.filename == name
            assert zf.read(zi) == data


def compare_file(file_a: str, file_b: str) -> bool:
    """
    比较两个文件是否相同

    Args:
        file_a (str): 第一个文件名
        file_b (str): 第二个文件名

    Returns:
        bool: 是否相同
    """
    with open(file_a, "rb") as fa:
        with open(file_b, "rb") as fb:
            return fa.read() == fb.read()


def test_compress_and_decompress_files() -> None:
    """
    测试压缩文件和解压缩文件
    """

    # 获取当前路径
    curdir = os.path.dirname(__file__)

    # 创建压缩文件对象
    with zipfile.ZipFile(ZIP_FILE, "w", zipfile.ZIP_DEFLATED) as zf:
        # 获取当前路径下所有文件
        for name in os.listdir(curdir):
            if os.path.isdir(name):
                continue  # 只对文件进行压缩

            # 将文件写入压缩文件
            zf.write(os.path.join(curdir, name), name)

    # 确认压缩文件正确创建
    assert os.path.exists(ZIP_FILE)

    # 打开压缩文件对象
    with zipfile.ZipFile(ZIP_FILE, "r") as zf:
        # 确保压缩文件正确
        assert zf.testzip() is None

        # 创建解压缩文件夹
        os.mkdir(UNZIP_TARGET_PATH)

        # 遍历压缩文件中的所有数据节点
        for zi in zf.filelist:
            # 通过数据节点名称生成目标文件名称
            src_file = os.path.join(curdir, zi.filename)
            # 确认对应的源文件存在
            assert os.path.exists(src_file)

            # 打开源文件
            with open(src_file, "rb") as pf:
                # 确保源文件内容和目标文件内容相同
                assert pf.read() == zf.read(zi)

            # 将数据节点解压缩到指定文件中
            zf.extract(zi, UNZIP_TARGET_PATH)

        # 遍历当前目录下的文件
        for name in os.listdir(curdir):
            # 生成压缩前源文件名
            src_file = os.path.join(curdir, name)
            # 生成解压缩后目标文件名
            target_file = os.path.join(UNZIP_TARGET_PATH, name)

            # 判断源文件是否是文件
            if os.path.isfile(src_file):
                # 确保源文件和目标文件内容一致
                assert compare_file(src_file, target_file)

        shutil.rmtree(UNZIP_TARGET_PATH)

        # 创建解压缩目标路径
        os.mkdir(UNZIP_TARGET_PATH)

        # 将压缩文件所有数据节点以文件形式写入目标路径
        zf.extractall(UNZIP_TARGET_PATH)

        # 验证所有文件都已解压成功
        for name in os.listdir(curdir):
            if os.path.isfile(name):
                assert compare_file(
                    os.path.join(curdir, name),
                    os.path.join(UNZIP_TARGET_PATH, name),
                )


def test_gzip() -> None:
    """
    测试 GZip
    """
    # 产生一组数据
    data = make_data()

    # 压缩数据, 获取被压缩数据
    z_data = gzip.compress(data)

    # 确保返回的数据已被压缩
    assert z_data != data
    assert len(z_data) < len(data)

    # 解压缩数据, 确保和源数据一致
    assert gzip.decompress(z_data) == data

    # 打开压缩文件对象用于存储数据
    with gzip.open(ZIP_FILE, "wb") as zf:
        # 将数据写入压缩文件, 确保全部数据被压缩
        assert zf.write(data) == len(data)

    # 打开压缩文件对象用于读取数据
    with gzip.open(ZIP_FILE, "rb") as zf:
        # 确保读取的数据和源数据一致
        assert zf.read() == data
