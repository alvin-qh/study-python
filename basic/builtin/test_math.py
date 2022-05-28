def test_abs_function() -> None:
    """
    测试绝对值函数
    """
    # 测试整数的绝对值
    assert abs(-10) == 10
    # 测试浮点数的绝对值
    assert abs(-10.20) == 10.20


def test_round_function() -> None:
    """
    测试四舍五入函数
    """
    # 保留 2 位小数, 四舍五入
    assert round(123.456, 2) == 123.46


def test_divmod_function() -> None:
    """
    测试整除, 取余函数
    返回一个二元组, 第一项为两个参数的整除结果, 第二项为两个参数的余数
    """
    # 5 // 3 == 1, 整除结果
    # 5 % 3 == 2, 取余结果
    assert divmod(5, 3) == (1, 2)


def test_number_to_str() -> None:
    """
    测试数值转字符串
    """
    # 整数转 10 进制字符串
    assert str(1) == "1"
    # 整数转 2 进制字符串
    assert bin(3) == "0b11"
    # 整数转 8 进制字符串
    assert oct(10) == "0o12"
    # 整数转 16 进制字符串
    assert hex(10) == "0xa"
