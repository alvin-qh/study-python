import io
import os

import zstandard as zstd

from utils.file_opt import delete_file_finally
from utils.generator import generate_large_data
from utils.unit import convert_unit


# 测试流式压缩和流式解压缩
# 1. 使用 `copy_stream` 方法进行流式压缩和解压缩
# 2. 使用 `ZstdCompressor` 和 `ZstdDecompressor` 对象的流式写入和流式读取功能进行压缩和解压缩


@delete_file_finally("test_compressor_copy_stream_output.zst")
def test_compressor_copy_stream() -> None:
    """测试通过 `copy_stream` 方法将流中的数据进行压缩"""
    # 生成 10MB 的数据
    raw_data = generate_large_data(1024 * 1024 * 10)
    print(
        f"Raw size: {convert_unit(len(raw_data), from_unit='B', to_unit='KB'):.2f} KB"
    )

    # 创建一个 zstandard 压缩器对象, 并设置压缩级别
    compressor = zstd.ZstdCompressor(level=10)

    # 基于待压缩数据创建一个输入流, 基于磁盘文件建立一个输出流
    # 通过 `copy_stream` 方法将输入流的内容写入输出流, 实现将输入流的原始数据压缩到压缩文件中
    with (
        io.BytesIO(raw_data) as fi,
        open("test_compressor_copy_stream_output.zst", "wb") as fo,
    ):
        # 使用压缩器对象的 `copy_stream` 方法进行压缩
        compressor.copy_stream(fi, fo, size=len(raw_data))

    # 获取压缩文件的大小
    stat = os.stat("test_compressor_copy_stream_output.zst")
    print(
        f"Compressed size: {convert_unit(stat.st_size, from_unit='B', to_unit='KB'):.2f} KB"
    )

    # 确认压缩后的文件大小小于原始数据大小
    assert stat.st_size < len(raw_data)
    print(f"Compression ratio: {stat.st_size / len(raw_data):.2f}")

    # 读取压缩文件内容, 并进行解压缩
    with open("test_compressor_copy_stream_output.zst", "rb") as f:
        decompressed_data = zstd.decompress(f.read())

    # 确认解压缩后的数据与原始数据相同
    assert decompressed_data == raw_data


@delete_file_finally("test_decompressor_copy_stream_output.zst")
def test_decompressor_copy_stream() -> None:
    """测试通过 `copy_stream` 方法将流中的数据进行解压缩"""
    # 生成 10MB 的数据
    raw_data = generate_large_data(1024 * 1024 * 10)

    # 压缩数据
    compressed_data = zstd.compress(raw_data)

    # 创建一个 zstandard 解压器对象
    decompressor = zstd.ZstdDecompressor()

    # 基于压缩数据创建一个输入流, 基于磁盘文件建立一个输出流
    # 通过 `copy_stream` 方法将输入流中的数据写入输出流, 实现将输入流中的压缩数据解压缩到文件中
    with (
        io.BytesIO(compressed_data) as fi,
        open("test_decompressor_copy_stream_output.zst", "wb") as fo,
    ):
        # 使用解压器对象的 `copy_stream` 方法进行解压缩
        decompressor.copy_stream(fi, fo)

    # 读取解压缩后的文件内容
    with open("test_decompressor_copy_stream_output.zst", "rb") as f:
        decompressed_data = f.read()

    # 确认解压缩后的数据与原始数据相同
    assert decompressed_data == raw_data


@delete_file_finally("test_compressor_stream_writer_output.zst")
def test_compress_with_stream_writer() -> None:
    """测试使用 `ZstdCompressor` 对象的流式写入功能进行压缩

    通过 `ZstdCompressor` 对象的 `stream_writer` 方法创建一个写入器对象, 并通过写入器的 `write` 方法
    将数据写入文件中

    写入器对象具备 Python 标准流对象的大部分接口, 包括:
    - `flush`: 用于刷新数据
    - `close`: 用于关闭写入器
    - `truncate`: 用于截断写入器
    - `fileno`: 返回文件句柄
    - `readable`: 判断写入器是否可读
    - `readall`: 用于读取所有数据
    - `readinto`: 用于读取数据到指定缓冲区中
    - `readline`: 用于读取一行数据
    - `readlines`: 用于读取多行数据
    - `writable`: 判断写入器是否可写
    - `write`: 用于写入数据
    - `writelines`: 用于写入多行数据
    - `seekable`: 判断写入器是否可定位
    - `seek`: 用于定位写入器
    - `tell`: 用于获取当前写入器的位置

    除上述方法外, 还提供了以下方法:
    - `isatty`: 判断写入器是否为终端设备
    - `memory_size`: 返回写入器已写入的数据大小
    """
    # 创建一个 zstandard 压缩器对象, 并设置压缩级别
    compressor = zstd.ZstdCompressor(level=10)

    # 定义存储原始数据的字节集合对象
    raw_data = bytes()

    # 打开一个磁盘文件用于存储压缩后的数据
    with open("test_compressor_stream_writer_output.zst", "wb") as f:
        # 创建一个写入器, 并和文件句柄绑定
        with compressor.stream_writer(f) as w:
            # 定义一个数据块大小
            chunk_size = 1024 * 1024  # 每次写入 1MB 数据

            # 写入 10 个数据块
            for _ in range(10):
                # 生成 1MB 的数据块并写入文件
                chunk = generate_large_data(chunk_size)
                w.write(chunk)

                # 添加原始数据到集合中, 以便后续进行校验
                raw_data += chunk

            # 刷新写入器, 确保所有数据都已写入底层文件
            w.flush()

    # 获取压缩文件大小
    stat = os.stat("test_compressor_stream_writer_output.zst")
    print(
        f"Compressed size: {convert_unit(stat.st_size, from_unit='B', to_unit='KB'):.2f} KB"
    )

    # 确认压缩后的文件大小小于原始数据大小
    assert stat.st_size < 10 * chunk_size

    # 输出压缩比
    print(f"Compression ratio: {stat.st_size / (10 * chunk_size):.2f}")

    with zstd.open("test_compressor_stream_writer_output.zst", "rb") as f:
        decompressed_data = f.read()

    assert decompressed_data == raw_data


@delete_file_finally("test_decompressor_stream_reader_output.zst")
def test_decompress_with_stream_reader() -> None:
    """测试使用 `ZstdDecompressor` 对象的流式读取功能进行解压缩

    通过 `ZstdDecompressor` 对象的 `stream_reader` 方法创建一个读取器对象, 并通过读取器的 `read` 方法
    从文件中读取数据

    读取器对象具备 Python 标准流对象的大部分接口, 包括:
    - `flush`: 用于刷新数据
    - `close`: 用于关闭写入器
    - `next`: 返回下一个字节
    - `readable`: 判断读取器是否可读
    - `read`: 用于读取数据
    - `read1`: 用于读取 1 字节数据
    - `readall`: 用于读取所有数据
    - `readinto`: 用于读取数据到指定流中
    - `readinto1`: 用于读取数据 1 字节到指定流中
    - `readline`: 用于读取一行数据
    - `readlines`: 用于读取多行数据
    - `writable`: 判断写入器是否可写
    - `write`: 用于写入数据
    - `writelines`: 用于写入多行数据
    - `seekable`: 判断写入器是否可定位
    - `seek`: 用于定位写入器
    - `tell`: 用于获取当前写入器的位置

    除上述方法外, 还提供了以下方法:
    - `isatty`: 判断写入器是否为终端设备
    """
    # 生成 10MB 的原始数据
    raw_data = generate_large_data(1024 * 1024 * 10)

    # 将原始数据写入压缩文件中
    with zstd.open("test_decompressor_stream_reader_output.zst", "wb") as f:
        f.write(raw_data)

    # 创建一个 zstandard 解压缩器对象
    decompressor = zstd.ZstdDecompressor()
    with open("test_decompressor_stream_reader_output.zst", "rb") as f:
        # 创建一个读取器, 并和文件句柄绑定
        with decompressor.stream_reader(f) as reader:
            # 读取解压缩后的数据
            decompressed_data = reader.read()

    # 确认解压缩后的数据与原始数据相同
    assert decompressed_data == raw_data
