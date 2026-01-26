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
        case val if (
            val > 1
        ):  # 通过 `val` 变量捕获 x 变量的值, 并且通过 `if` 语句进行匹配
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
