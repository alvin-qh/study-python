from lib import add


def test_str_add() -> None:
    """测试 `add` 方法用于字符串连接"""
    assert add("a", "b") == "ab"


def test_int_add() -> None:
    """测试 `add` 方法用于整数相加"""
    assert add(1, 2) == 3


def test_float_add() -> None:
    """测试 `add` 方法用于浮点数相加"""
    assert round(add(1.1, 2.2), 1) == 3.3
