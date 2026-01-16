import zstandard as zstd
from utils import generate_large_string


def test_compress_string() -> None:
    raw_data = generate_large_string(1000000).encode("utf-8")

    comp = zstd.ZstdCompressor(level=10)

    comp_data = comp.compress(raw_data)
    assert len(comp_data) < len(raw_data)
