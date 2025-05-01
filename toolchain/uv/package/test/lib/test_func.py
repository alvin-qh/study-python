from lib.func import add


def test_add() -> None:
    """测试 `lib.func.add` 函数"""
    assert add(1, 2) == 3
    assert round(add(1.1, 2.2), 2) == 3.30
    assert add("a", "b") == "ab"
