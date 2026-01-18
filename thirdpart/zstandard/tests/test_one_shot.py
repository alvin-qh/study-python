import os

import zstandard as zstd

from utils.file_opt import delete_file_finally
from utils.generator import generate_large_data
from utils.unit import convert_unit

# zstandard 提供了三个快捷函数, 可以以最简单的代码进行压缩和解压缩, 对于简单的使用场景非常方便 (例如压缩数据量较小)


def test_one_shot_compress_decompress() -> None:
    """测试 zstandard 库的一次性压缩和解压缩功能"""
    # 原始数据
    raw_data = generate_large_data(1024 * 1024)
    print(
        f"Raw size: {convert_unit(len(raw_data), from_unit='B', to_unit='KB'):.2f} KB"
    )

    # 使用 zstandard 库的一次性压缩函数进行压缩
    compressed_data = zstd.compress(raw_data, level=10)
    print(
        f"Compressed size: {convert_unit(len(compressed_data), from_unit='B', to_unit='KB'):.2f} KB"
    )

    # 使用 zstandard 库的一次性解压缩函数进行解压缩
    decompressed_data = zstd.decompress(compressed_data)

    # 确认解压缩后的数据与原始数据相同
    assert decompressed_data == raw_data


@delete_file_finally("test_one_shot_open_file.zst")
def test_one_shot_open_file() -> None:
    """测试 zstandard 库一次性打开文件进行压缩和解压缩功能"""

    # 生成原始数据
    raw_data = generate_large_data(1024 * 1024)

    # 使用 zstandard 库创建一个压缩文件句柄, 并写入数据， 其中的 filename 和 mode 参数与 Python 内置的 open 函数类似
    # 其中 cctx 参数用于指定该文件用于压缩的压缩器对象, 除此之外, 可选的参数还包括:
    # - dctx: 用于解压缩的解压缩器对象
    # - encoding: 指定文件编码方式 (对于 mode 为文本模式时有效)
    # - errors: 指定编码错误处理方式 (对于 mode 为文本模式时有效)
    with zstd.open(
        "test_one_shot_open_file.zst", "wb", cctx=zstd.ZstdCompressor(level=15)
    ) as f:
        f.write(raw_data)

    # 确认压缩后的文件大小小于原始数据大小
    stat = os.stat("test_one_shot_open_file.zst")
    assert stat.st_size < len(raw_data)

    # 使用 zstandard 库创建一个压缩文件句柄, 并读取数据
    with zstd.open(
        "test_one_shot_open_file.zst", "rb", dctx=zstd.ZstdDecompressor()
    ) as f:
        decompressed_data = f.read()

    # 确认解压缩后的数据与原始数据相同
    assert decompressed_data == raw_data
