import re
from typing import Any


def test_match_pattern() -> None:
    """`re` 包的 `match` 函数用于通过一个模式对字符串进行匹配

    `match(pattern, str, flags=0) -> bool` 函数通过 `pattern` 模式字符串对 `str` 进行匹配.其中 `flags` 参数取值如下:

    - `re.A` (或 `re.ASCII`): 令 `\\w`, `\\W`, `\\b`, `\\B` 模式只对 ASCII 字符有效
    - `re.DEBUG`: 显示调试日志
    - `re.I` (或 `re.IGNORECASE`): 匹配时忽略大小写
    - `re.L` (或 `re.LOCALE`): 令 `\\w`, `\\W`, `\\b`, `\\B` 模式以及忽略大小写标记通过本地语言进行处理
    - `re.M` (或 `re.MULTILINE`): 允许处理多行文本
    - `re.S` (或 `re.DOTALL`): 令 `.` 模式匹配所有字符, 包括换行符; 否则 `.` 模式不匹配换行符. 对应的内联标记为 (`?s`).
    - `re.X` (或 `re.VERBOSE`): 该模式下可以支持可读性更好的正则表达式, 即允许模块化和添加注释
    """
    # 定义电话号码的模式
    pattern = (
        r"^\(?(0\d{2})[\)\-\s]?(\d{8})$"  # 3 + 8 固话
        r"|^\(?(0\d{3})[\)\-\s]?(\d{7,8})$"  # 4 + 7 / 4 + 8 固话
        r"|(^1\d{10})$"  # 11 位手机号码, 1 开头
    )

    # 判断 3 + 8 模式的固话号码匹配清空
    r = re.match(pattern, "(029)85556666")
    assert r  # 不为 None 表示匹配成功
    assert r.group(1) == "029"  # 获取第 1 个分组, 为 3 + 8 模式的区号 (3 部分)
    assert r.group(2) == "85556666"  # 获取第 2 个分组, 为 3 + 8 模式的电话号 (8 部分)

    # 同上
    r = re.match(pattern, "029-85556666")
    assert r
    assert r.group(1) == "029"
    assert r.group(2) == "85556666"

    # 同上
    r = re.match(pattern, "029 85556666")
    assert r
    assert r.group(1) == "029"
    assert r.group(2) == "85556666"

    # 判断 4 + 7 模式的固话号码匹配清空
    r = re.match(pattern, "(0917)8556666")
    assert r  # 不为 None 表示匹配成功
    assert r.group(3) == "0917"  # 获取第 3 个分组, 为 4 + 7 模式的区号 (4 部分)
    assert r.group(4) == "8556666"  # 获取第 4 个分组, 为 4 + 7 模式的电话号 (7 部分)

    # 同上
    r = re.match(pattern, "0917-8556666")
    assert r
    assert r.group(3) == "0917"
    assert r.group(4) == "8556666"

    # 同上
    r = re.match(pattern, "0917 8556666")
    assert r
    assert r.group(3) == "0917"
    assert r.group(4) == "8556666"

    # 判断 11 模式的手机号码匹配清空
    r = re.match(pattern, "13991300001")
    assert r  # 不为 None 表示匹配成功
    assert r.group(5) == "13991300001"  # 获取第 5 个分组, 为手机号模式的电话号 (11 部分)

    # 匹配一个错误模式
    r = re.match(pattern, "029-8555666")
    assert not r  # 为 None 表示匹配失败


def test_find_all_matched_part() -> None:
    """查找所有和模式匹配的部分, 返回这些匹配结果组成的集合

    - `findall` 函数返回所有匹配的结果组成的集合
    - `finditer` 函数返回所有匹配结果 Match 对象的迭代器
    """
    r: Any

    # 查找数字
    pattern = r"\d+"

    # 查找数字, 每 3 个数字中间的空格会造成模式中断
    # 最终结果为 3 项, 每项 3 个数字
    r = re.findall(pattern, "123 456 789")
    assert r == ["123", "456", "789"]

    # 查找逻辑同上, 返回 Match 对象的迭代器
    r = re.finditer(pattern, "123 456 789")
    # 通过每个 Match 对象获取匹配结果
    assert [m.group() for m in r] == ["123", "456", "789"]


def test_split() -> None:
    """通过正则表达式切分一个字符串, 返回切分结果的列表集合对象"""

    # 用于切分字符串的正则表达式
    pattern = r"\s+"

    # 通过正则表达式对字符串进行切分
    r = re.split(pattern, "abc    def ghi\tjkl")
    # 验证切分结果
    assert r == ["abc", "def", "ghi", "jkl"]

    # 对切分结果的数量进行限制, maxsplit=2 表示最大返回 3 个结果
    r = re.split(pattern, "abc    def ghi\tjkl", maxsplit=2)
    # 验证切分结果, 最后一部分因为限制未进行切分
    assert r == ["abc", "def", "ghi\tjkl"]


def test_substring() -> None:
    """通过正则获取子字符串"""

    # 子字符串获取正则表达式
    pattern = r"\d+"

    # 要处理的原字符串
    s = "123a456b789c"

    # 通过正则处理子字符串, 并将子字符串替换为 ""
    r = re.sub(pattern, "", s)
    # 验证处理结果, 即将匹配的子字符串替换为 "" 后的结果
    assert r == "abc"

    # 过程中获取的子字符串
    # 切分为 3 部分, 每部分的内容 (原字符串的数字部分)
    subs = ["123", "456", "789"]
    index = 0

    def repl(m: re.Match) -> str:
        """过程中回调函数, 传入每次计算出的子字符串, 返回将该字符串替换为的新字符串

        Args:
            - `m` (`re.Match`): 每次切分的部分

        Returns:
            `str`: 要将切分部分替换为的字符串
        """
        nonlocal index

        # 验证切分的结果
        # span 函数获取子字符串的切片
        # group 函数返回子字符串内容
        assert s[slice(*m.span())] == m.group() == subs[index]
        index += 1

        return "X"

    # 通过正则处理子字符串, 并通过一个回调函数返回对子字符串替换的字符串
    r = re.sub(pattern, repl, "123a456b789c")
    assert r == "XaXbXc"


def test_search_and_grouping() -> None:
    """对所给的正则表达式进行完整匹配, 并获取分组结果"""

    # 正则表达式会匹配 4 个分组, 均为整数, 用 "," 分隔
    # "?P<n1>" 是分组的名称
    pattern = r"(?P<n1>\d+),(\d+),(?P<n2>\d+),(\d+)"

    # 通过正则表达式查找字符串, 获取分组结果
    rs = re.search(pattern, "10,20,30,50")
    # 验证分组结果
    assert rs
    assert rs.groups() == ("10", "20", "30", "50")

    # 通过分组 ID 获取分组结果
    assert rs.group(1) == "10"
    assert rs.group(4) == "50"

    # 通过分组名称获取分组结果
    assert rs.group("n1") == "10"
    assert rs.group("n2") == "30"

    # 获取各个分组内容在原字符串中的下标索引
    assert rs.start(1) == 0
    assert rs.end(1) == 2

    assert rs.start(2) == 3
    assert rs.end(2) == 5

    # 获取命名分组组成的字典
    assert rs.groupdict() == {"n1": "10", "n2": "30"}


def test_compile_pattern() -> None:
    """编译正则表达式

    对于需要重复使用的正则表达式, 可以将其进行编译, 加快使用效率
    """
    r: Any

    # 对正则表达式字符串进行编译
    rx = re.compile(r"\s+")

    # 通过编译后的正则表达式进行字符串匹配
    # 匹配 "\t" 字符串
    r = rx.match("\t")
    # 验证匹配成功的结果
    assert r
    assert r.group() == "\t"

    # 对正则表达式字符串进行编译
    rx = re.compile(r"(\d+)")

    # 通过编译后的正则表达式查找所有符合的子字符串
    r = rx.findall("1 2\t3  4")
    # 验证查找结果
    assert r == ["1", "2", "3", "4"]

    # 对正则表达式字符串进行编译
    rx = re.compile(r"\s+")

    # 通过编译后的正则表达式进行字符串切分
    r = rx.split("1 2\t3  4")
    # 验证切分结果
    assert r == ["1", "2", "3", "4"]

    # 通过编译后的正则表达式进行子字符串搜索和替换
    # 将正则表达式匹配出的结果替换为 "-"
    r = rx.sub("-", "1 2\t3  4")
    # 验证查找替换结果
    assert r == "1-2-3-4"

    # 对正则表达式字符串进行编译
    rx = re.compile(r"(\d+)\s*(\d+)")

    # 通过编译后的正则对字符串进行查询, 返回分组结果
    r = rx.search("1 2\t3 4")
    # 验证分组结果
    assert r.groups() == ("1", "2")


def test_escape1() -> None:
    """将正则表达式里的特殊字符进行转义

    一些特殊字符是正则表达式的保留字符, 如果要表达字符的原义则需要进行转义. 例如: 反斜杠字符, 如果要表达 "反斜杠" 字符的原义, 则需要写为 `\\`
    """
    # 对特殊字符 [, ], -, \ 进行转义
    esp = re.escape(r"[-\]")
    # 验证检验后的结果, \[, \], \-, \\
    assert esp == r"\[\-\\\]"

    # 将转义后的正则表达式字符串进行编译
    rx = re.compile(f"[{esp}]")

    # 使用转义后的正则字符串
    r = rx.findall(r"-\]a[")
    # 验证结果
    assert r == ["-", "\\", "]", "["]


def test_escape2() -> None:
    """对于用传入的字符串作为正则一部分来进行匹配时, 最优方式是对内容进行一次转义操作, 保证不会受到特殊字符的影响"""

    characters = {
        "a": "A",
        "b": "B",
        "c": "C",
    }

    # characters 字典对象作为迭代器对象, 是字典 Key 的序列
    # 对字典 Key 进行转义后, 组成一个正则表达式字符串
    pattern = "|".join(map(re.escape, characters))
    assert pattern == "a|b|c"

    # 编译正则表达式
    rx = re.compile(pattern)

    def replace(mo: re.Match) -> str:
        """对正则匹配结果进行替换的回调方法

        Args:
            - `mo` (`re.Match`): 匹配成功的 Match 对象

        Returns:
            `str`: 要替换为的字符串
        """
        return characters[mo.group(0)]

    # 通过正则表达式, 对指定的字符串进行查找, 并将查找到的子字符串进行替换
    r = rx.sub(replace, "abcde")
    # 确认替换结果
    assert r == "ABCde"
