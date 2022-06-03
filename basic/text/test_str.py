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


def test_counter() -> None:
    """
    `count` 方法用于计算字符串中子字符串出现的次数

    cspell: disable
    """
    s = "abcdabcdabc"

    # 计算字符串中字符个数
    assert s.count("") == 12
    # 计算指定字符的个数
    assert s.count("b") == 3
    # 计算指定子字符串的个数
    assert s.count("bc") == 3
    # 查找 "bcd" 子字符串出现的次数, 并指定查找的起始位置和结束位置
    assert s.count("bcd", 2, -1) == 1

    # cspell: enable


def test_split() -> None:
    """
    字符串分割

    `split` 方法和 `splitlines` 方法可以对字符串进行不同方式的分割
    """
    s = """a b
c
d
e"""

    # 默认情况下 split 方法根据空白字符串 (" ", "\t", "\n" 等) 分割字符串
    assert s.split() == ["a", "b", "c", "d", "e"]

    # 指定以换行符分割字符串
    assert s.split("\n") == ["a b", "c", "d", "e"]

    # 指定以换行符分割字符串
    assert s.splitlines() == ["a b", "c", "d", "e"]


def test_reversed() -> None:
    """
    反转字符串

    字符串本质上是一个字符的列表集合, 所以可以通过 "切片运算" 和 "`reversed` 函数" 两种方式进行反转

    cspell: disable
    """
    s = "abc def"

    # 通过切片反转字符串
    assert s[::-1] == "fed cba"
    # 通过 reversed 函数反转字符串
    assert "".join(reversed(s)) == "fed cba"

    # 将字符串切分后诸部份反转
    r = " ".join([e[::-1] for e in s.split(" ")])
    assert r == "cba fed"

    # cspell: enable


def test_translate() -> None:
    """
    可以通过一个字符编码的字典对象, 对字符串中的指定字符进行转换

    `maketrans` 方法用于通过简单方法形成转换字典
    `translate` 方法用于执行转换
    """
    # 形成转换表
    # 将两个参数进行逐字符对应, 形成一个字典对象
    tab = str.maketrans("ABC", "abc")
    # 确认形成的转换表是正确的字典对象
    assert tab == {
        ord("A"): ord("a"),
        ord("B"): ord("b"),
        ord("C"): ord("c"),
    }

    # 对字符串进行转换
    s = "ABCDEF"
    # 确认转换结果
    assert s.translate(tab) == "abcDEF"
