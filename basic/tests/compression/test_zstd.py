import os

from compression import zstd

from basic.compression import convert_unit, delete_file_finally, generate_data

# 测试使用 `compression.zstd` 库对数据进行压缩
# 1. 创建 `ZstdCompressor` 压缩器对象和 `ZstdDecompressor` 解压器对象
# 2. 通过 `zstd.compress` 和 `zstd.decompress`` 函数进行压缩和解压缩
# 3. 通过 `zstd.open` 函数以文件句柄的形式进行压缩和解压缩


def test_compress_and_decompress() -> None:
    """测试 zstd 库的一次性压缩和解压缩功能"""
    # 原始数据
    raw_data = generate_data(1024 * 1024)
    print(
        f"Raw size: {convert_unit(len(raw_data), from_unit='B', to_unit='KB'):.2f} KB"
    )

    # 使用 zstd 库的一次性压缩函数进行压缩
    compressed_data = zstd.compress(raw_data, level=10)
    print(
        f"Compressed size: {convert_unit(len(compressed_data), from_unit='B', to_unit='KB'):.2f} KB"
    )

    # 使用 zstd 库的一次性解压缩函数进行解压缩
    decompressed_data = zstd.decompress(compressed_data)

    # 确认解压缩后的数据与原始数据相同
    assert decompressed_data == raw_data


@delete_file_finally("test_one_shot_open_file.zst")
def test_open_compression_file() -> None:
    """测试 zstandard 库一次性打开文件进行压缩和解压缩功能"""

    # 生成原始数据
    raw_data = generate_data(1024 * 1024)

    # 使用 zstd 库创建一个压缩文件句柄, 并写入数据， 其中的 filename 和 mode 参数与 Python 内置的 open 函数类似
    # - encoding: 指定文件编码方式 (对于 mode 为文本模式时有效)
    # - errors: 指定编码错误处理方式 (对于 mode 为文本模式时有效)
    with zstd.open("test_one_shot_open_file.zst", "wb", level=10) as f:
        f.write(raw_data)

    # 确认压缩后的文件大小小于原始数据大小
    stat = os.stat("test_one_shot_open_file.zst")
    assert stat.st_size < len(raw_data)

    # 使用 zstd 库创建一个压缩文件句柄, 并读取数据
    with zstd.open("test_one_shot_open_file.zst", "rb") as f:
        decompressed_data = f.read()

    # 确认解压缩后的数据与原始数据相同
    assert decompressed_data == raw_data


def test_compress_data() -> None:
    """测试使用 zstd 库压缩和解压缩数据

    通过 python zstd 库的 `ZstdCompressor` 和 `ZstdDecompressor` 类对数据进行压缩和解压缩
    """
    # 生成 10MB 的数据
    raw_data = generate_data(1024 * 1024)
    print(
        f"Raw size: {convert_unit(len(raw_data), from_unit='B', to_unit='KB'):.2f} KB"
    )

    # 创建一个 zstd 压缩器对象, 并设置压缩级别
    compressor = zstd.ZstdCompressor(level=10)

    # 压缩数据, 并获取压缩后的字节数据
    compressed_data = compressor.compress(raw_data)
    print(
        f"Compressed size: {convert_unit(len(compressed_data), from_unit='B', to_unit='KB'):.2f} KB"
    )

    # 确认压缩后的数据小于原始数据
    assert len(compressed_data) < len(raw_data)
    print(f"Compression ratio: {len(compressed_data) / len(raw_data):.2f}")

    # 创建一个 zstd 解压器对象
    decompressor = zstd.ZstdDecompressor()

    # 解压缩数据, 并获取解压后的字节数据
    decompressed_data = decompressor.decompress(compressed_data)

    # 确认解压缩后的数据与原始数据相同
    assert decompressed_data == raw_data
