from typing import Callable


def test_function_like() -> None:
    """
    测试 Python 中的仿函数 (`Callable` 类型)
    """

    def do(cb: Callable, a: int, b: int) -> int:
        """
        定义一个测试函数

        Args:
            cb (Callable): 一个可调用类型
            a (int): 供可调用类型调用的第一个参数
            b (int): 供可调用类型调用的第二个参数

        Returns:
            int: 返回可调用类型的返回值
        """
        # 这里必须使用一个 int() 运算符, 对类型进行转换或对象进行 __int__ 方法调用
        return int(cb(a, b))

    # 通过一个 lambda 表达式调用 do 函数
    # lambda 表达式相当于一个单行函数
    r = do(lambda x, y: x + y, 10, 20)
    assert r == 30

    class CallableClass:
        """
        定义一个可调用类型
        """

        def __init__(self, base: int) -> None:
            self._base = base

        def __call__(self, a: int, b: int) -> int:
            """
            供可调用类型对象进行仿函数调用的方法

            Args:
                a (int): 参数1
                b (int): 参数2

            Returns:
                int: 两个参数的计算结果
            """
            return a + b + self._base

    # 一个类, 如果具备 __call__ 方法, 则其对象可以仿照函数调用语法进行调用
    callable_obj = CallableClass(10)
    r = do(callable_obj, 1, 2)
    assert r == 13

    class CallClass:
        """
        定义一个具备构造器的类
        """

        def __init__(self, a: int, b: int) -> None:
            """
            具备两个参数的构造器

            Args:
                a (int): 参数1
                b (int): 参数2
            """
            # 计算两个参数的和
            self._r = a + b

        def __int__(self) -> int:
            """
            支持通过 int(obj) 将当前对象转为 int 类型

            Returns:
                int: 两个参数运算的结果
            """
            return self._r

    # 将一个类作为参数传递, 在 do 函数内部会以函数调用形式
    # 使用这个类, 相当于调用类的构造器方法, 得到类对象.
    # 通过 __int__ 方法, 类对象会转为 int 类型, 得到结果
    call_obj = do(CallClass, 1, 2)
    assert call_obj == 3
