import os
import shutil
import zipfile
from datetime import datetime
from os import path

from pytest import mark

from basic.compression.generator import generate_data


@mark.parametrize("delete_file_fixture", [{"extension": ".zip"}], indirect=True)
def test_zip_unzip_data(delete_file_fixture: list[str]) -> None:
    """测试文件的压缩和解压

    `zipfile` 包下 `ZipFile` 类对象表示一个压缩文件对象
    """
    file_name = delete_file_fixture[0]

    # 生成两个压缩节点名称和对应的数据
    # 获取节点名称集合与数据集合
    entities, raw_data = zip(
        *[(f"data{n}/test.data", generate_data(1024 * 1024)) for n in range(1, 3)]
    )

    now = datetime.now().timetuple()[:6]

    # 创建一个可写入的压缩文件对象, 使用 DEFLATED 算法
    with zipfile.ZipFile(file_name, "w", zipfile.ZIP_DEFLATED) as zf:
        # 将数据写入压缩文件的指定节点
        zf.writestr(entities[0], raw_data[0])

        # 通过 ZipInfo 对象写入数据
        # ZipInfo 可为压缩数据节点赋予更多的属性, 包括创建时间, 文件权限等
        zi = zipfile.ZipInfo(entities[1], date_time=now)
        zi.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(zi, raw_data[1])

    # 压缩后文件尺寸小于原数据大小
    assert path.getsize(file_name) < len(raw_data[0]) + len(raw_data[1])

    # 打开一个可读取的压缩文件对象
    with zipfile.ZipFile(file_name, "r") as zf:
        # 测试压缩文件是否正确
        # 测试会读取所有压缩文件并对 CRC 进行验证, 失败会返回错误的数据节点名称
        assert zf.testzip() is None

        # 通过节点名称读取内容
        assert zf.read(entities[0]) == raw_data[0]
        assert zf.read(entities[1]) == raw_data[1]

        # 获取数据节点信息
        zi = zf.getinfo(entities[0])

        assert zi.filename == entities[0]
        # 判断文件的 crc 验证码
        assert zi.CRC == zipfile.crc32(raw_data[0])  # type: ignore

        # 获取数据节点信息
        zi = zf.getinfo(entities[1])

        assert zi.filename == entities[1]
        # 判断文件的 crc 验证码
        assert zi.CRC == zipfile.crc32(raw_data[1])  # type: ignore
        # 文件时间的秒有可能有一些误差, 所以比较到分钟部分
        assert zi.date_time[:5] == now[:5]

        # 遍历读取压缩文件中的所有数据节点
        for zi, name, data in zip(zf.filelist, entities, raw_data):
            assert zi.filename == name
            assert zf.read(name) == data


@mark.parametrize("delete_file_fixture", [{"extension": ".zip"}], indirect=True)
def test_compress_and_decompress_files(delete_file_fixture: list[str]) -> None:
    """测试压缩文件和解压缩文件"""
    # 获取自动生成的压缩文件名
    file_name = delete_file_fixture[0]

    # 获取当前路径
    curdir = path.dirname(__file__)

    # 创建压缩文件对象
    with zipfile.ZipFile(file_name, "w", zipfile.ZIP_DEFLATED) as zf:
        # 获取当前路径下所有文件
        for name in os.listdir(curdir):
            # 只对文件进行压缩
            if path.isfile(name):
                # 将文件写入压缩文件
                zf.write(os.path.join(curdir, name), name)

    # 打开压缩文件对象
    with zipfile.ZipFile(file_name, "r") as zf:
        try:
            # 确保压缩文件正确
            assert zf.testzip() is None

            # 创建解压缩文件夹
            os.mkdir("_unzip")

            # 遍历压缩文件中的所有数据节点
            for zi in zf.filelist:
                # 打开压缩节点对应的源数据文件
                with open(path.join(curdir, zi.filename), "rb") as pf:
                    # 确保源文件内容和目标文件内容相同
                    assert pf.read() == zf.read(zi)

                # 将数据节点解压缩到指定文件中
                zf.extract(zi, "_unzip")
        finally:
            # 删除解压缩文件夹
            shutil.rmtree("_unzip")
