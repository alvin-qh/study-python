import io

import zstandard as zstd

from utils import convert_unit, generate_large_data

# 测试使用 zstandard 库对数据进行压缩
# 1. 创建 `ZstdCompressor` 压缩器对象和 `ZstdDecompressor` 解压器对象
# 2. 使用 `.compress` 和 `.decompress` 方法对数据进行压缩和解压缩
# 3. 使用 `.compressobj` 和 `.decompressobj` 方法进行增量压缩和增量解压缩


def test_compress_data() -> None:
    """测试使用 zstandard 库压缩和解压缩数据

    通过 zstandard 库的 `ZstdCompressor` 和 `ZstdDecompressor` 类对数据进行压缩和解压缩
    """
    # 生成 10MB 的数据
    raw_data = generate_large_data(1024 * 1024 * 10)
    print(f"Raw size: {convert_unit(len(raw_data), from_unit='B', to_unit='KB'):.2f} KB")

    # 创建一个 zstandard 压缩器对象, 并设置压缩级别
    compressor = zstd.ZstdCompressor(level=10)

    # 压缩数据, 并获取压缩后的字节数据
    compressed_data = compressor.compress(raw_data)
    print(f"Compressed size: {convert_unit(len(compressed_data), from_unit='B', to_unit='KB'):.2f} KB")

    # 确认压缩后的数据小于原始数据
    assert len(compressed_data) < len(raw_data)
    print(f"Compression ratio: {len(compressed_data) / len(raw_data):.2f}")

    # 创建一个 zstandard 解压器对象
    decompressor = zstd.ZstdDecompressor()

    # 解压缩数据, 并获取解压后的字节数据
    decompressed_data = decompressor.decompress(compressed_data)

    # 确认解压缩后的数据与原始数据相同
    assert decompressed_data == raw_data


def test_compress_object() -> None:
    """测试增量压缩和增量解压缩功能

    所谓增量压缩, 即在压缩过程中, 可以分多次将数据传入压缩器对象进行压缩, 每次传入一部分数据, 最终通过 flush 方法获取剩余的压缩数据

    所谓增量解压缩, 即在解压缩过程中, 可以分多次将数据传入解压器对象进行解压缩, 每次传入一部分数据, 最终通过 flush 方法获取剩余的解压数据

    增量压缩和解压缩并不是常用功能 (不推荐使用), 因为其压缩比相较于一次性压缩要低, 如果需要进行流式压缩和解压缩, 推荐使用流式读写功能
    """
    # 创建一个 zstandard 压缩器对象
    compressor = zstd.ZstdCompressor()

    # 创建一个增量压缩对象
    c_obj = compressor.compressobj()

    # 保存每次压缩原始数据的集合
    raw_data_list: list[bytes] = []

    # 保存每次压缩后数据的集合
    compressed_chunks: list[bytes] = []

    # 生成 10 个 1MB 的数据块, 并依次进行压缩
    for _ in range(10):
        # 生成 1MB 的数据块, 并将其保存到集合中
        raw_data = generate_large_data(1024 * 1024)
        raw_data_list.append(raw_data)

        # 对数据块进行压缩, 并将压缩后的数据保存到集合中
        compressed_data = c_obj.compress(raw_data)
        compressed_chunks.append(compressed_data)

    # 保存压缩器对象中剩余的压缩数据
    compressed_chunks.append(c_obj.flush())

    # 拼接所有原始数据块和压缩数据块, 得到最终的原始数据和压缩数据
    raw_data = b"".join(raw_data_list)
    compressed_data = b"".join(compressed_chunks)

    # 输出压缩前后的数据大小和压缩率
    print(f"Raw size: {convert_unit(len(raw_data), from_unit='B', to_unit='KB'):.2f} KB")
    print(f"Compressed size: {convert_unit(len(compressed_data), from_unit='B', to_unit='KB'):.2f} KB")
    print(f"Compression ratio: {len(compressed_data) / len(raw_data):.2f}")

    # 创建一个 zstandard 解压器对象
    decompressor = zstd.ZstdDecompressor()

    # 创建一个增量解压缩对象
    d_obj = decompressor.decompressobj()

    # 依次对每个压缩数据块进行解压缩, 并将解压缩后的数据保存到集合中
    decompressed_chunks = [d_obj.decompress(chunk) for chunk in compressed_chunks]

    # 保存解压器对象中剩余的解压数据
    decompressed_chunks.append(d_obj.flush())

    # 拼接所有解压数据块, 得到最终的解压数据
    decompressed_data = b"".join(decompressed_chunks)

    # 确认解压缩后的数据与原始数据相同
    assert raw_data == decompressed_data


def test_compress_in_chunk() -> None:
    raw_data = generate_large_data(1024 * 1024 * 10)
    print(f"Raw size: {convert_unit(len(raw_data), from_unit='B', to_unit='KB'):.2f} KB")

    chunk_size = 32768

    compressor = zstd.ZstdCompressor()

    chunker = compressor.chunker(chunk_size=chunk_size)

    compressed_chunks: list[bytes] = []

    with io.BytesIO(raw_data) as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break

            for chunk_data in chunker.compress(chunk):
                compressed_chunks.append(chunk_data)

        for chunk_data in chunker.finish():  # type: ignore
            compressed_chunks.append(chunk_data)

    for i in range(len(compressed_chunks) - 1):
        assert len(compressed_chunks[i]) == chunk_size

    print(
        f"Number of compressed chunks: {len(compressed_chunks)}, "
        f"each chunk size: {chunk_size} B, "
        f"last chunk size: {len(compressed_chunks[-1])} B"
    )

    compressed_data = b"".join(compressed_chunks)
    print(f"Compressed size: {convert_unit(len(compressed_data), from_unit='B', to_unit='KB'):.2f} KB")

    print(f"Compression ratio: {len(compressed_data) / len(raw_data):.2f}")

    decompress = zstd.ZstdDecompressor(max_window_size=chunk_size)
    assert decompress.decompress(compressed_data) == raw_data
