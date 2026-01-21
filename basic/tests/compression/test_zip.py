import os
import zipfile
from datetime import datetime
from os import path

from basic.compression.file_opt import delete_file_finally
from basic.compression.generator import generate_data


@delete_file_finally("test_zip_unzip_data.zip")
def test_zip_unzip_data() -> None:
    """测试文件的压缩和解压

    `zipfile` 包下 `ZipFile` 类对象表示一个压缩文件对象
    """
    # 定义两个节点名称
    ZIP_ENTRY1 = "data1/test.dat"
    ZIP_ENTRY2 = "data2/test.dat"

    # 产生一组数据
    raw_data1 = generate_data(1024 * 1024)
    raw_data2 = generate_data(1024 * 1024)
    now = datetime.now().timetuple()[:6]

    # 创建一个可写入的压缩文件对象, 使用 DEFLATED 算法
    with zipfile.ZipFile("test_zip_unzip_data.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        # 将数据写入压缩文件的指定节点
        zf.writestr(ZIP_ENTRY1, raw_data1)

        # 通过 ZipInfo 对象写入数据
        # ZipInfo 可为压缩数据节点赋予更多的属性, 包括创建时间, 文件权限等
        zi = zipfile.ZipInfo("data2/test.dat", date_time=now)
        zi.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(zi, raw_data2)

    # 压缩后文件尺寸小于原数据大小
    assert path.getsize("test_zip_unzip_data.zip") < len(raw_data1) + len(raw_data2)

    # 打开一个可读取的压缩文件对象
    with zipfile.ZipFile("test_zip_unzip_data.zip", "r") as zf:
        # 测试压缩文件是否正确
        # 测试会读取所有压缩文件并对 CRC 进行验证, 失败会返回错误的数据节点名称
        assert zf.testzip() is None

        # 通过节点名称读取内容
        assert zf.read(ZIP_ENTRY1) == raw_data1
        assert zf.read(ZIP_ENTRY2) == raw_data2

        # 获取数据节点信息
        zi = zf.getinfo(ZIP_ENTRY1)
        assert zi.filename == ZIP_ENTRY1
        assert zi.CRC == zipfile.crc32(raw_data1)  # type: ignore # 判断文件的 crc 验证码

        # 获取数据节点信息
        zi = zf.getinfo(ZIP_ENTRY2)
        assert zi.filename == ZIP_ENTRY2
        assert zi.CRC == zipfile.crc32(raw_data2)  # type: ignore # 判断文件的 crc 验证码
        # 文件时间的秒有可能有一些误差, 所以比较到分钟部分
        assert zi.date_time[:5] == now[:5]

        # 遍历读取压缩文件中的所有数据节点
        for zi, name, data in zip(
            zf.filelist, [ZIP_ENTRY1, ZIP_ENTRY2], [raw_data1, raw_data2]
        ):
            assert zi.filename == name
            assert zf.read(name) == data


@delete_file_finally("test_compress_and_decompress_files.zip")
def test_compress_and_decompress_files() -> None:
    """测试压缩文件和解压缩文件"""

    # 获取当前路径
    curdir = path.dirname(__file__)

    # 创建压缩文件对象
    with zipfile.ZipFile(
        "test_compress_and_decompress_files.zip", "w", zipfile.ZIP_DEFLATED
    ) as zf:
        # 获取当前路径下所有文件
        for name in os.listdir(curdir):
            if path.isdir(name):
                continue  # 只对文件进行压缩

            # 将文件写入压缩文件
            zf.write(os.path.join(curdir, name), name)

    # 确认压缩文件正确创建
    assert os.path.exists("test_compress_and_decompress_files.zip")

    # 打开压缩文件对象
    with zipfile.ZipFile("test_compress_and_decompress_files.zip", "r") as zf:
        # 确保压缩文件正确
        assert zf.testzip() is None

        # 创建解压缩文件夹
        os.mkdir("_unzip")

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
            zf.extract(zi, "_unzip")

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
