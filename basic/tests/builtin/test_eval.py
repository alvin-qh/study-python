def test_eval_expression() -> None:
    """
    `eval` 函数用于执行一个编译后的 Python 表达式

    表达式需要先通过 `compile` 函数进行编译
    """
    # 字符串, 表示一个 Python 表达式
    expression = "1 + 1"

    # 将字符串进行编译, mode="eval" 表示编译为表达式, 通过 eval 函数执行
    # 在通过 eval 函数执行后, 返回表达式的值
    compiled = compile(expression, filename="", mode="eval")

    # 测试执行结果
    assert eval(compiled) == 2

    # 直接执行字符串表达式
    assert eval("1 + 2") == 3


def test_eval_function() -> None:
    """
    `eval` 函数用于执行一段编译后的 Python 代码

    代码需要先通过 `compile` 函数进行编译
    """
    _locals = {"x": None, "y": None}

    # 字符串, 表示一段 Python 代码
    code = "x = 1 + 1"

    # 将字符串进行编译, mode="exec" 表示编译为代码, 通过 exec 函数执行
    # 在通过 exec 函数执行后, 不返回任何结果, 但内存中会保留变量的值
    compiled = compile(code, filename="", mode="exec")

    # 执行编译的代码
    exec(compiled, None, _locals)

    # 通过 eval 执行表达式获取变量值
    assert _locals["x"] == 2

    # 直接执行字符串代码
    exec("""y = 1 + 2""", None, _locals)

    # 通过 eval 执行表达式获取变量值
    assert _locals["y"] == 3


def test_exec_function() -> None:
    """
    测试通过 `exec` 函数执行复杂 Python 代码
    """

    _locals = {"x": None, "y": None}

    code = """
x = 0
for i in range(10):
    x += 1
y = x
    """

    exec(code, None, _locals)

    assert _locals["x"] == 10
    assert _locals["y"] == 10
