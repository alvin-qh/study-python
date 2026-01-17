import os
import io
import zstandard as zstd

from utils.file_opt import delete_file_finally
from utils.generator import generate_large_data
from utils.unit import convert_unit


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
