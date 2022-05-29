def test_ascii_convert() -> None:
    """
    测试将字符和 ASCII 码之间的互相转换
    """
    # 字符转为 ASCII 码
    assert ord("A") == 65
    # ASCII 码转为字符
    assert chr(97) == "a"

    # 将字符串内容转为 ASCII 编码表示

    # ASCII 字符转为 ASCII 编码表示
    assert ascii("AB") == "'AB'"
    # UNICODE 字符转为 ASCII 编码表示
    assert ascii("测试") == "'\\u6d4b\\u8bd5'"
