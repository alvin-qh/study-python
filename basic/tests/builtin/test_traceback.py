import sys
from inspect import getframeinfo, stack
from traceback import format_exception, format_stack


def raise_exception() -> None:
    """抛出 `RuntimeError` 异常"""
    raise RuntimeError("This is an exception", 100)


def assert_str_contains(src: str, *contains: str) -> None:
    """断言所给的字符串是否被 `str` 参数字符串包含

    Args:
        `src` (`str`): 原字符串
        `contains` (`tuple[str])`): 可能被包含在 `src` 字符串的字符串集合
    """
    for s in contains:
        assert s in src, f"'{s}' not in '{src}'"


def test_get_trace_back_from_exception() -> None:
    try:
        raise_exception()
    except RuntimeError as e:
        assert e.args[0] == "This is an exception"
        assert e.args[1] == 100
        assert str(e) == "('This is an exception', 100)"

        # 为异常增加附加信息
        e.add_note("???")

        # `traceback.format_exception` 返回数组, 每一项为堆栈的一帧信息
        print("".join(format_exception(e)))

        # `sys.exc_info` 函数返回当前的异常信息和堆栈信息
        # `traceback.format_exc` 函数返回当前异常的字符串信息
        # `traceback.format_tb` 函数用于将堆栈对象 (`TracebackType` 类型) 格式化为字符串
        exp_type, exp, tb = sys.exc_info()
        assert exp_type is RuntimeError
        assert exp is e
        print("".join(format_exception(e)))

        # 获取异常对象的堆栈信息, 和当前异常的堆栈信息一致
        assert e.__traceback__ == tb

    # `traceback.format_stack` 返回当前调用堆栈的数组, 每一项为堆栈的一帧信息
    print("".join(format_stack()))

    """对应的, 还有如下函数可以直接在控制台输出异常或堆栈信息
    - `traceback.print_tb()`
    - `traceback.print_exception()`
    - `traceback.print_exc()`
    - `traceback.print_last()`
    - `traceback.print_stack()`
    """


def debug_info(message: str) -> str:
    """获取调用方的信息

    通过 `inspect.stack` 函数可以获取当前调用的堆栈信息数组, 取第 2 项 即调用当前函数的堆栈帧
    堆栈帧是一个 7 元组, 内容为 `(<frame object>, filename, lineno, function, code_context, index, positions)`, 而
    `<frame object>` 则是一个 6 元组, 包含 `(filename, lineno, function, code_context, index, positions)`

    `inspect.getframeinfo` 函数可以将 <frame object> 转化为 `Traceback` 类型对象, 可以获取堆栈帧的各项信息
    """
    caller = getframeinfo(stack()[1][0])
    return f"{caller.filename}:{caller.lineno} - {message}"


def test_debug_info() -> None:
    print(debug_info("Test debug info"))
