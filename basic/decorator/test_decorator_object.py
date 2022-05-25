from pytest import raises

from .decorator_object import App, Logger

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


logger = Logger()


@logger
def multiply(x, y):
    return x * y


def test_logger() -> None:
    multiply(10, 20)
    assert str(logger) == """log function 'multiply' is call:
    function=multiply
      arguments=(10, 20) {}
      return=200
      time=0.000000 sec"""

    multiply(30, 40)
