def test_abs_function() -> None:
    assert abs(-10) == 10
    assert abs(-10.20) == 10.20


def test_round_function() -> None:
    assert round(123.456, 2) == 123.46
