from typing import Callable
from unittest.mock import MagicMock, patch

from pytest import raises

from .decorator_object import App, Logger, timeit

# 产生 App 类型的对象
app = App()


@app.register("/")
def main_page() -> str:
    """
    注册函数

    Returns:
        str: 返回值
    """
    return "The main page"


@app.register("/next")
def next_page():
    """
    注册函数

    Returns:
        str: 返回值
    """
    return "The next page"


def test_find_executor_by_url() -> None:
    # 确认 URL 对应的执行函数是否正确执行
    assert app.execute("/") == "The main page"
    assert app.execute("/next") == "The next page"

    # 测试未注册 URL 的情况
    with raises(KeyError) as err:
        app.execute("/unknown")

        # 确认返回的异常
        assert str(err.value) == '\'"/unknown" not register\''


# 定义日志对象
logger = Logger()


@logger  # 日志对象用作装饰器
def multiply(x: int, y: int) -> int:
    """
    乘法函数, 用于测试日志装饰器

    Args:
        x (int): 被乘数
        y (int): 乘数

    Returns:
        int: 两数相乘结果
    """
    return x * y


@patch.object(timeit, "default_timer")  # 对计时器函数进行 mock 操作
def test_logger(mocked_default_timer: MagicMock) -> None:
    # 设定计时器函数的返回值
    mocked_default_timer.return_value = 0

    # 调用目标函数
    multiply(10, 20)
    # 检测调用目标函数后的日志对象内容
    assert str(logger) == (
        "\tlog function 'multiply' is call: \n\t  function=multiply\n\t  "
        "arguments=(10, 20) \n\t  return=200\n\t  time=0.000000 sec\n"
    )

    # 再次调用目标函数
    multiply(30, 40)
    # 检测调用目标函数 2 次后的日志对象内容
    assert str(logger) == (
        "\tlog function 'multiply' is call: \n\t  function=multiply\n\t  "
        "arguments=(10, 20) \n\t  return=200\n\t  time=0.000000 sec\n"

        "\tlog function 'multiply' is call: \n\t  function=multiply\n\t  "
        "arguments=(30, 40) \n\t  return=1200\n\t  time=0.000000 sec\n"
    )
