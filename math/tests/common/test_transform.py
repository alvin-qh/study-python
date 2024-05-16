from typing import Callable

from common.transform import compose, curry2, rotate2d
from common.vector import to_radian


def test_compose() -> None:
    """测试 compose 函数, 组合多个函数一起执行"""

    def prepend(s: str) -> Callable[[str], str]:
        """指定一个字符串并返回一个函数, 该函数可以在指定字符串之前增加一个字符

        Args:
            `s` (`str`): 指定的字符串

        Returns:
            `Callable[[str], str]`: 返回在指定字符串增加字符的函数
        """
        return lambda input: s + input

    # 逆向执行三个 prepend 函数, 为指定的字符串添加三个字符
    fn = compose(
        prepend("P"),  # 在原字符串前添加 P 字符
        prepend("y"),  # 在原字符串前添加 y 字符
        prepend("t"),  # 在原字符串前添加 t 字符
    )

    # 确认结果正确
    assert fn("hon") == "Python"


def test_curry2() -> None:
    """测试函数柯里化

    将一个两个参数的函数包装为一个函数, 该函数接受第一个参数, 并返回另一个函数, 后者接收第二个参数, 返回原函数的执行结果
    """

    def add(x: int, y: int) -> int:
        return x + y

    # 返回第一个函数
    fn = curry2(add)
    # 执行第一个函数和第一个函数返回的函数
    assert fn(100)(200) == 300


def test_rotate2d() -> None:
    """测试将一个二维向量旋转指定弧度"""
    v = (20, 30)
    degree = to_radian(30)

    assert rotate2d(degree, v) == (2.3205080756887755, 35.98076211353316)
