from functools import partial
from typing import Callable


def test_override_function() -> None:
    """
    测试简单的函数重载

    Python 中, 任何函数都可以通过 `*args, **kwargs` 方式传参, 由解释器来分配实际的参数.

    所以, 可以根据不同的情况, 选择不同的函数, 然后通过 `*args, **kwargs` 方式统一传参调用
    """

    def run(*args: int, **kwargs: int) -> int:
        """
        根据不同的参数, 执行不同的函数

        Returns:
            int: 调用结果
        """

        def add1(x: int, y: int) -> int:
            """
            执行两个参数相加, 返回结果

            Args:
                x (int): 加数 1
                y (int): 加数 2

            Returns:
                int: 两个参数相加的结果
            """
            return x + y

        def add2(x: int, y: int, z: int) -> int:
            """
            执行三个参数相加, 返回结果

            Args:
                x (int): 加数 1
                y (int): 加数 2
                z (int): 加数 3

            Returns:
                int: 三个参数相加的结果
            """
            return x + y + z

        fn: Callable[..., int] = add2

        # 根据参数情况, 从 add1 和 add2 中选择要执行的函数
        if len(args) + len(kwargs) == 2:
            fn = add1

        # 执行选择的方法
        return fn(*args, **kwargs)

    # 验证两个参数的情况
    assert run(1, 2) == 3
    assert run(x=1, y=2) == 3

    # 验证三个参数的情况
    assert run(1, 2, 3) == 6
    assert run(z=1, x=2, y=3) == 6


def test_asterisk_arg() -> None:
    """
    测试星号参数

    星号参数不是实际的参数, 但星号参数之后的参数, 必须用命名传参的方式使用
    """

    def run(a: int, b: int, *, c: int) -> int:
        """
        计算三个参数的和

        `a` 和 `b` 参数可以使用位置传参以及命名传参的方式传参.
        `c` 参数由于在星号参数之后, 所以必须通过命名传参的方式使用
        Args:
            a (int): 加数 1
            b (int): 加数 2
            c (int): 加数 3

        Returns:
            int: 三个参数的和
        """
        return a + b + c

    # 验证传参方式
    r = run(10, 20, c=30)
    assert r == 60


def test_currying_function() -> None:
    """
    "柯里化", 即将一个函数转化为另一种形式 (例如固定某个参数的值)

    `partial` 函数有助于让一个函数的形式符合调用要求
    """

    def func(a: int, b: int) -> int:
        """
        两个参数的函数, 用于测试 "柯里化"

        Args:
            a (int): 参数 1
            b (int): 参数 2

        Returns:
            int: 两个参数的和
        """
        return a - b

    # 为 func 函数设置两个参数, 返回一个无参的函数代理
    fw = partial(func, 10, 20)
    # 调用无参的代理函数, 确认两个预设参数是否起作用
    assert fw() == -10

    # 为 func 函数设置一个参数, 返回一个单参数的函数代理
    fw = partial(func, 10)
    # 调用无参的代理函数, 确认两个预设参数是否起作用
    assert fw(20) == -10

    # 为 func 函数设置一个参数, 返回一个单参数的函数代理
    fw = partial(func, a=10)
    # 因为 a 参数已经以命名形式固定, 所以 b 参数也必须通过命名方式传递
    assert fw(b=20) == -10
