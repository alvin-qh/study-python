from datetime import datetime
import math


def test_match_case_statement_basic() -> None:
    """测试 match case 语句

    match case 语句在 Python 3.10 中被引入，用于解决 Python 缺少其它语言中 switch case 语句的问题

    Python 引入的 match case 语句，可以替代 switch case 语句，实现更简洁的代码, 且具备匹配模式, 可以完成更复杂的逻辑判断

    本例演示了 match case 语句的基本用法, 对指定值进行匹配判断, 并执行对应的逻辑分支
    """
    res = ""

    x = 1

    # 匹配 x 的值, 对应执行不同分支
    match x:
        case 0:
            res = "x is zero"
        case 1:
            res = "x is one"
        case _:  # 当之前所有分支都未被匹配时, 执行此分支
            res = "x is more than one"

    assert res == "x is one"


def test_match_case_statement_to_match_list() -> None:
    """测试 match case 语句

    本例测试 match case 语句，对列表数据进行匹配判断, 并执行对应的逻辑分支

    原则上, 对集合的匹配仍是等值匹配, 但 Python 为集合匹配增加了一个元素捕捉功能, 可以匹配集合中的部分元素, 匹配成功则捕获剩余元素
    """
    res = ""

    x = [1, 2, 5]
    match x:
        case [1, 2, 3]:
            res = "x is [1, 2, 3]"
        case [1, 2, 4]:
            res = "x is [1, 2, 4]"
        case [1, 2, *rest]:  # 匹配集合中前两个元素为 1, 2, 剩余元素捕获在变量 rest 中
            res = f"x is [1, 2, {rest}]"

    assert res == "x is [1, 2, [5]]"


def test_match_case_statement_with_variable() -> None:
    """测试 match case 语句

    本例测试 match case 语句，对指定值进行匹配判断, 并执行对应的逻辑分支, 且匹配成功时, 可以获取匹配成功的值

    在 case 语句中, 可以定义变量来捕获 match 语句中指定的值, 并在 case 语句中定义条件判断, 来判断变量的值是否满足要求,
    这种方式使得匹配逻辑更加灵活
    """
    res = ""

    x = 1
    match x:
        case 0:
            res = "x is zero"
        case 1:
            res = "x is one"
        case val if val > 1:  # 通过 `val` 变量捕获 x 变量的值, 并且通过 `if` 语句进行匹配
            res = "x is more than one"
        case val if val < 0:
            res = "x is less than zero"

    assert res == "x is one"


def test_match_case_statement_with_unpack_variable() -> None:
    """测试 match case 语句

    本例测试在 case 中捕获变量时, 对被捕获的变量进行 unpack 操作, 之后对 unpack 的变量进行各种匹配操作
    """
    res = ""

    point = (1, 2)

    match point:
        case (0, 0):
            res = "origin"
        case (x, y) if x > y:
            res = "x is more than y"
        case (x, y) if x < y:
            res = "x is less than y"
        case _:
            res = "x and y are equal"

    assert res == "x is less than y"


def test_f_string_with_variable() -> None:
    """测试 f-string 增强项

    本例中测试在 f-string 中使用变量, 获取变量的值并拼接字符串, 该语法有利于在调试过程中快速输出变量值
    """
    a = 100
    b = 200

    # 获取变量值并拼接字符串
    s = f"{a =}, {b =}, {a + b =}"
    assert s == "a=100, b='OK'"


def test_f_string_with_complex_expressions() -> None:
    """测试 f-string 增强项

    本例中测试在 f-string 中使用复杂表达式, 可以简化代码结构
    """
    radius = 3

    # 在 f-string 中使用复杂表达式, 输出圆面积
    s = f"S = {math.pi * radius ** 2:.2f}"
    assert s == "S = 28.27"


def test_use_quotes_in_expression_in_f_string() -> None:
    """测试 f-string 增强项

    本例中测试在 f-string 的表达式中使用引号, 包括访问字典属性, 对象属性访问以及使用字符串常量等
    """
    attrs = {
        "name": "Alvin",
        "age": 43,
        "gender": "M",
    }

    s = (
        f"{"Mr." if attrs["gender"] == "M" else "Mis."}"  # 在 f-string 表达式中使用字符串常量并访对象属性
        f" {attrs["name"]} is {attrs["age"]} years old"  # 在 f-string 表达式中使用对象属性访问
    )
    assert s == "Mr. Alvin is 43 years old"


def test_f_string_with_comments() -> None:
    """测试 f-string 增强项

    本例中测试在 f-string 中使用注释, 可以在字符串中添加注释, 帮助阅读代码

    注意, 目前只允许在多行 f-string 中使用注释 (即通过 `f\"\"\"` 开始, 通过 `\"\"\"` 结束)
    """
    radius = 3

    # 在多行 f-string 中使用注释
    s = f"""S = {
        # 计算圆的面积
        math.pi * radius ** 2:.2f}"""

    assert s == "S = 28.27"


def test_f_string_with_multi_level_nesting() -> None:
    """测试 f-string 增强项

    本例中测试在 f-string 中使用多层嵌套, 可以简化代码结构

    所谓嵌套, 即可以在 f-string 的表达式中继续使用 f-string
    """
    name = "Alvin"
    age = 43

    detail = f"Name: {name}, Age: {age}, Detail: {f"{name} is {age} years old"}"
    assert detail == "Name: Alvin, Age: 43, Detail: Alvin is 43 years old"


def test_f_string_with_number_formats() -> None:
    """测试 f-string 增强项

    本例中测试在 f-string 中对数值进行格式化, 常用的数值格式化方式有:
    - `.<n>f`: 保留 `n` 位小数
    - `#0x`: 十六进制表示, 并增加 `0x` 前缀
    - `,`: 添加千分位分隔符
    - `b`: 二进制表示
    - `o`: 八进制表示
    - `.<n>e`: 科学计数法表示, 并保留 `n` 位小数
    - `[0]<n>`: 填充数字, 宽度为 `n`, 右侧填充空格; 宽度为 `0n“, 则右侧填充零
    """
    n = 4200

    assert f"{n:.2f}" == "4200.00"
    assert f"{n:#0x}" == "0x1068"
    assert f"{n:,}" == "4,200"
    assert f"{n:b}" == "1000001101000"
    assert f"{n:o}" == "10150"
    assert f"{n:.2e}" == "4.20e+03"
    assert f"{n:09}" == "000004200"


def test_f_string_with_alignment() -> None:
    """测试 f-string 增强项

    本例中测试在 f-string 中对字符串进行对齐, 可以通过 `<` 左对齐, `>` 右对齐, `^` 居中对齐, 默认以空格填充，
    也可以设置以 `0` 填充
    """
    name = "Alvin"

    assert f"{name:<10}" == "Alvin     "
    assert f"{name:>10}" == "     Alvin"
    assert f"{name:^10}" == "  Alvin   "

    num = 123
    assert f"{num:<010}" == "1230000000"
    assert f"{num:>010}" == "0000000123"
    assert f"{num:^010}" == "0001230000"


def test_f_string_with_datetime() -> None:
    """测试 f-string 增强项

    本例中测试在 f-string 中使用日期时间格式化, 可以将日期时间格式化为字符串, 并指定格式, 格式化的格式有:
    - `%Y`: 年
    - `%m`: 月
    - `%d`: 日
    - `%H`: 时
    - `%M`: 分
    - `%S`: 秒
    - `%z`: 时区
    - `%a`: 星期
    - `%A`: 星期
    - `%b`: 月
    - `%B`: 月

    和通过 `datetime.strftime()` 函数的作用类似
    """
    now = datetime.now()

    assert f"{now:%Y-%m-%d}" == now.strftime("%Y-%m-%d")
    assert f"{now:%H:%M:%S}" == now.strftime("%H:%M:%S")
    assert f"{now:%H:%M:%S}" == now.strftime("%H:%M:%S")


def test_f_string_with_multi_lines() -> None:
    """测试 f-string 增强项

    本例中测试在 f-string 中使用多行字符串, 可以将多行字符串格式化为字符串
    """
    name = "Alvin"
    age = 43

    s = f"""
{"Mr." if age >= 18 else "Mis."} {name}, you are welcome.
you are {age} years old.
"""
    assert s == "\nMr. Alvin, you are welcome.\nyou are 43 years old.\n"


def test_f_string_with_multi_part() -> None:
    """测试 f-string 增强项

    本例中测试在 f-string 中使用对齐, 可以将字符串格式化为字符串, 并指定对齐方式
    """
    name = "Alvin"
    age = 43

    s = f"{"Mr." if age >= 18 else "Mis."} {name}, you are welcome. " f"you are {age} years old."
    assert s == "Mr. Alvin, you are welcome. you are 43 years old."
