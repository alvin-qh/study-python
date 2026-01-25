from basic.builtin.language_features import check_value_if_true


def test_if_else_statement() -> None:
    """测试 if ... else 语句"""
    # 对于布尔类型, True 表示真, False 表示假
    assert check_value_if_true(True) == "True"
    assert check_value_if_true(False) == "False"

    # 对于集合类型, 非空集合表示真, 空集合表示假
    assert check_value_if_true([1, 2, 3]) == "True"
    assert check_value_if_true([]) == "False"

    # 对于字典类型, 非空字典表示真, 空字典表示假
    assert check_value_if_true({"number": 100}) == "True"
    assert check_value_if_true({}) == "False"

    # 对于对象类型, 非空对象引用表示真, 空对象引用表示假
    assert check_value_if_true(object()) == "True"
    assert check_value_if_true(None) == "False"

    # 对于字符串类型, 非空字符串表示真, 空字符串表示假
    assert check_value_if_true("Hello") == "True"
    assert check_value_if_true("") == "False"

    # 对于数字类型, 非零数字表示真, 零数字表示假
    assert check_value_if_true(1) == "True"
    assert check_value_if_true(0) == "False"
