import re
from typing import Any


def test_match_pattern() -> None:
    """
    `re` 包的 `match` 函数用于通过一个模式对字符串进行匹配

    `match(pattern, str, flags=0) -> bool` 函数通过 `pattern` 模式字符串对 `str` 进行匹配.
    其中 `flags` 参数取值如下:

    - `re.A` (或 `re.ASCII`): 令 `\\w`, `\\W`, `\\b`, `\\B` 模式只对 ASCII 字符有效
    - `re.DEBUG`: 显示调试日志
    - `re.I` (或 `re.IGNORECASE`): 匹配时忽略大小写
    - `re.L` (或 `re.LOCALE`): 令 `\\w`, `\\W`, `\\b`, `\\B` 模式以及忽略大小写标记通过
    本地语言进行处理
    - `re.M` (或 `re.MULTILINE`): 允许处理多行文本
    - `re.S` (或 `re.DOTALL`): 令 `.` 模式匹配所有字符, 包括换行符; 否则 `.` 模式不匹配换行符. 对应的内联标
    记为 (`?s`).
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
    """
    查找所有和模式匹配的部分, 返回这些匹配结果组成的集合

    `findall` 函数返回所有匹配的结果组成的集合
    `finditer` 函数返回所有匹配结果 Match 对象的迭代器
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
