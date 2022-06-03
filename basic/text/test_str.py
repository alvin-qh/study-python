def test_str_slice() -> None:
    """
    字符串切片操作
    """
    s = "一二三四五六七八九零"

    # 通过下标获取指定位置嗯字符
    assert s[2] == "三"
    # 获取一个范围的切片
    assert s[1:4] == "二三四"
    # 获取指定位置到结尾的切片
    assert s[2:] == "三四五六七八九零"
    # 获取开头到指定位置的切片
    assert s[:3] == "一二三"
    # 位置可以使用负数, 表示从字符串末尾倒数计算
    assert s[-4:] == "七八九零"
    # 设置切片的步长
    assert s[1:-1:2] == "二四六八"

    # 利用 LC 切片发获取每字符串两个字符的集合
    fivers = [s[k:k + 2] for k in range(0, len(s), 2)]
    assert fivers == ["一二", "三四", "五六", "七八", "九零"]

    cuts = [2, 5, 9]
    # 将首位, 末尾位置加上后, 产生 2 元组序列
    # 相当于 zip([0, 2, 5, 9], [2, 5, 9, 10])
    slices = list(zip([0] + cuts, cuts + [len(s)]))
    assert slices == [(0, 2), (2, 5),  (5, 9), (9, 10)]
    # 进行切片
    fivers = [s[i:j] for i, j in slices]
    assert fivers == ["一二", "三四五", "六七八九", "零"]


def test_str_multiplication() -> None:
    """
    字符串的乘法操作, 相当于将字符串内容重复多次后形成新的字符串

    cspell: disable
    """
    s = "xo"
    # 验证重复 3 次的结果
    assert s * 3 == "xoxoxo"
    # cspell: enable


def test_character_filter() -> None:
    """
    `str` 用于字符过滤判断的函数包括:
    - `isdigit` 返回字符串是否全部由数字字符组成
    - `isalpha` 返回字符串是否全部由字母 (或汉字) 字符组成
    - `isalnum` 结果相当于 `isalpha` 和 `isdigit` 两个函数的组合
    """

    # 判断字符串是否全部为数字字符
    assert "123".isdigit() is True
    assert "a23".isdigit() is False

    # 判断字符串是否全部为字母字符
    assert "123".isalpha() is False
    assert "abc".isalpha() is True

    # 判断字符串是否全部为数字+字母字符
    assert "123".isalnum() is True
    assert "abc".isalnum() is True
    assert "a1b2c3".isalnum() is True
    assert "_1c".isalnum() is False
