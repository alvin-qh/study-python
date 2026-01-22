from os import path

from compression import gzip

from pytest import mark

from basic.compression import convert_unit, generate_data

# 测试使用 `compression.gzip` 库对数据进行压缩
# 2. 通过 `gzip.compress` 和 `gzip.decompress`` 函数进行压缩和解压缩
# 3. 通过 `gzip.open` 函数以文件句柄的形式进行压缩和解压缩


def test_compress_and_decompress() -> None:
    """测试 gzip 库的一次性压缩和解压缩功能"""
    # 原始数据
    raw_data = generate_data(1024 * 1024)
    print(
        f"Raw size: {convert_unit(len(raw_data), from_unit='B', to_unit='KB'):.2f} KB"
    )

    # 使用 gzip 库的一次性压缩函数进行压缩
    compressed_data = gzip.compress(raw_data, compresslevel=9)
    print(
        f"Compressed size: {convert_unit(len(compressed_data), from_unit='B', to_unit='KB'):.2f} KB"
    )

    # 使用 gzip 库的一次性解压缩函数进行解压缩
    decompressed_data = gzip.decompress(compressed_data)

    # 确认解压缩后的数据与原始数据相同
    assert decompressed_data == raw_data


@mark.parametrize("delete_file_fixture", [{"extension": ".gz"}], indirect=True)
def test_open_compression_file(delete_file_fixture: list[str]) -> None:
    """测试 zstandard 库一次性打开文件进行压缩和解压缩功能"""

    file_name = delete_file_fixture[0]

    # 生成原始数据
    raw_data = generate_data(1024 * 1024)

    # 使用 zstandard 库创建一个压缩文件句柄, 并写入数据， 其中的 filename 和 mode 参数与 Python 内置的 open 函数类似
    # 其中 cctx 参数用于指定该文件用于压缩的压缩器对象, 除此之外, 可选的参数还包括:
    # - dctx: 用于解压缩的解压缩器对象
    # - encoding: 指定文件编码方式 (对于 mode 为文本模式时有效)
    # - errors: 指定编码错误处理方式 (对于 mode 为文本模式时有效)
    with gzip.open(file_name, "wb", compresslevel=9) as f:
        f.write(raw_data)

    # 确认压缩后的文件大小小于原始数据大小
    assert path.getsize(file_name) < len(raw_data)

    # 使用 zstandard 库创建一个压缩文件句柄, 并读取数据
    with gzip.open(file_name, "rb") as f:
        decompressed_data = f.read()

    # 确认解压缩后的数据与原始数据相同
    assert decompressed_data == raw_data
