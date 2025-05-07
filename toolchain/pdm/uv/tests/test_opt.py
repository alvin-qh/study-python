from opt import add


def test_opt_add() -> None:
    """测试 `opt` 模块的 `add` 函数"""
    assert add(1, 2) == 3
    assert add("1", "2") == "12"
