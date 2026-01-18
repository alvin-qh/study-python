import zstandard as zstd

from utils import convert_unit, generate_large_data


def test_compress_string() -> None:
    """测试使用 zstandard 库压缩生成的字符串"""
    # 生成 10MB 的数据
    raw_data = generate_large_data(1024 * 1024 * 10)
    print(
        f"Raw size: {convert_unit(len(raw_data), from_unit='B', to_unit='KB'):.2f} KB"
    )

    # 创建一个 zstandard 压缩器对象, 并设置压缩级别
    compressor = zstd.ZstdCompressor(level=10)

    # 压缩数据, 并获取压缩后的字节数据
    compressed_data = compressor.compress(raw_data)
    print(
        f"Compressed size: {convert_unit(len(compressed_data), from_unit='B', to_unit='KB'):.2f} KB"
    )

    # 确认压缩后的数据小于原始数据
    assert len(compressed_data) < len(raw_data)
    print(f"Compression ratio: {len(compressed_data) / len(raw_data):.2f}")

    # 创建一个 zstandard 解压器对象
    decompressor = zstd.ZstdDecompressor()

    # 解压缩数据, 并获取解压后的字节数据
    decompressed_data = decompressor.decompress(compressed_data)

    # 确认解压缩后的数据与原始数据相同
    assert decompressed_data == raw_data
