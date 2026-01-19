# zstandard

## 1. 概述

本项目是一个 [zstandard](https://facebook.github.io/zstd/) 压缩算法的 Python 绑定库学习和测试项目

zstandard（简称 Zstd）是由 Facebook 开源的无损数据压缩算法，以其高压缩比和快速压缩/解压缩速度而著称

## 2. zstandard 库使用说明

### 2.1. 安装

```bash
pip install zstandard
```

或

```bash
pdm add zstandard
```

### 2.2. 核心组件

zstandard Python 库提供以下核心组件：

| 组件                          | 说明                           |
| ----------------------------- | ------------------------------ |
| `ZstdCompressor`              | 压缩器对象，支持多种压缩模式   |
| `ZstdDecompressor`            | 解压器对象，支持多种解压缩模式 |
| `compress()` / `decompress()` | 一次性压缩/解压缩快捷函数      |
| `open()`                      | 文件句柄封装，支持读写压缩文件 |

### 2.3. 压缩级别

zstandard 支持 1-22 级的压缩级别, 默认为 3:

- **级别 1-3**: 快速压缩，适合实时处理场景
- **级别 4-9**: 平衡压缩比和处理速度
- **级别 10+**: 高压缩比，适合离线处理场景

## 3. 使用范例

### 3.1. 一次性压缩/解压缩

适用于小数据量的简单压缩场景:

```python
import zstandard as zstd

# 原始数据
raw_data = b"Hello, zstandard!"

# 一次性压缩
compressed_data = zstd.compress(raw_data, level=10)

# 一次性解压缩
decompressed_data = zstd.decompress(compressed_data)

# 验证结果
assert decompressed_data == raw_data
```

### 3.2. 压缩器/解压器对象

适合需要重复使用压缩/解压缩功能的场景：

```python
import zstandard as zstd

# 创建压缩器对象
compressor = zstd.ZstdCompressor(level=10)

# 压缩数据
raw_data = b"Data to compress" * 1000
compressed_data = compressor.compress(raw_data)

# 创建解压器对象
decompressor = zstd.ZstdDecompressor()

# 解压缩数据
decompressed_data = decompressor.decompress(compressed_data)

assert decompressed_data == raw_data
```

### 3.3. 文件压缩/解压缩

使用 `zstd.open` 进行文件级别的压缩操作：

```python
import zstandard as zstd

# 压缩文件
with zstd.open("data.zst", "wb", cctx=zstd.ZstdCompressor(level=15)) as f:
    f.write(b"File content to compress")

# 解压缩文件
with zstd.open("data.zst", "rb", dctx=zstd.ZstdDecompressor()) as f:
    decompressed_data = f.read()
```

### 3.4. 流式压缩/解压缩

适用于大型文件或内存敏感场景：

```python
import io
import zstandard as zstd

# 流式压缩
compressor = zstd.ZstdCompressor(level=10)
with io.BytesIO(raw_data) as fi, open("output.zst", "wb") as fo:
    compressor.copy_stream(fi, fo, size=len(raw_data))

# 流式解压缩
decompressor = zstd.ZstdDecompressor()
with open("output.zst", "rb") as fi, io.BytesIO() as fo:
    decompressor.copy_stream(fi, fo)
    decompressed_data = fo.getvalue()
```

### 3.5. 流式写入器

使用 `stream_writer` 进行增量写入压缩：

```python
import zstandard as zstd

compressor = zstd.ZstdCompressor(level=10)

with open("output.zst", "wb") as f:
    with compressor.stream_writer(f) as w:
        for chunk in data_chunks:
            w.write(chunk)
```

### 3.6. 流式读取器

使用 `stream_reader` 进行增量读取解压缩：

```python
import zstandard as zstd

decompressor = zstd.ZstdDecompressor()

with open("data.zst", "rb") as f:
    with decompressor.stream_reader(f) as reader:
        decompressed_data = reader.read()
```

### 3.7. 增量压缩/解压缩

适用于数据分块处理的场景：

```python
import zstandard as zstd

# 增量压缩
compressor = zstd.ZstdCompressor()
c_obj = compressor.compressobj()

compressed_chunks = []
for chunk in data_chunks:
    compressed_chunks.append(c_obj.compress(chunk))
compressed_chunks.append(c_obj.flush())

compressed_data = b"".join(compressed_chunks)

# 增量解压缩
decompressor = zstd.ZstdDecompressor()
d_obj = decompressor.decompressobj()

decompressed_chunks = []
for chunk in compressed_chunks:
    decompressed_chunks.append(d_obj.decompress(chunk))
decompressed_chunks.append(d_obj.flush())

decompressed_data = b"".join(decompressed_chunks)
```

## 4. 项目结构

```plaintext
zstandard/
├── README.md                 # 项目说明文档
├── pyproject.toml           # 项目配置
├── tests/                    # 测试用例
│   ├── __init__.py
│   ├── test_compress.py     # 基础压缩测试
│   ├── test_one_shot.py     # 一次性压缩测试
│   └── test_stream.py       # 流式压缩测试
└── utils/                    # 工具模块
    ├── __init__.py
    ├── unit.py              # 单位转换工具
    ├── generator.py         # 测试数据生成器
    └── file_opt.py          # 文件操作工具
```

## 5. 运行测试

```bash
# 运行所有测试
pytest
```

## 参考资料

- [Python zstandard 官方文档](https://python-zstandard.readthedocs.io/en/latest/index.html)
- [zstandard 官方文档](https://facebook.github.io/zstd/)
- [zstandard GitHub 仓库](https://github.com/facebook/zstd)

## License

MIT
