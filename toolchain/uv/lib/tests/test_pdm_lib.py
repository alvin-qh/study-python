from uv_lib import add


def test_math_add() -> None:
    """测试 `uv_lib` 模块的 `add` 函数"""
    assert add(1, 2) == 3
    assert add("1", "2") == "12"
