from lib.math import add


def test_math_add() -> None:
    assert add(1, 2) == 3
    assert add("1", "2") == "12"
