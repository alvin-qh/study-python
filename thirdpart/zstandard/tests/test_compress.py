import zstandard as zstd
from utils import generate_large_string, convert_unit


def test_compress_string() -> None:
    """测试使用 zstandard 库压缩生成的字符串"""
    # 生成一个大字符串并转换为字节
    raw_data = generate_large_string(1000000).encode("utf-8")
    print(
        f"Raw size: {convert_unit(len(raw_data), from_unit='B', to_unit='KB'):.2f} KB"
    )

    # 创建一个 zstandard 压缩器对象, 并设置压缩级别
    comp = zstd.ZstdCompressor(level=10)

    # 压缩数据, 并获取压缩后的字节数据
    comp_data = comp.compress(raw_data)
    print(
        f"Compressed size: {convert_unit(len(comp_data), from_unit='B', to_unit='KB'):.2f} KB"
    )

    # 确认压缩后的数据小于原始数据
    assert len(comp_data) < len(raw_data)

    # 创建一个 zstandard 解压器对象
    de_comp = zstd.ZstdDecompressor()

    # 解压缩数据, 并获取解压后的字节数据
    de_comp_data = de_comp.decompress(comp_data)

    # 确认解压缩后的数据与原始数据相同
    assert de_comp_data == raw_data
