from typing import Any, overload


def test_function_overload() -> None:
    """定义函数重载

    Python 没有真正的函数重载概念, 也就是不能在一个作用域范围内定义多个同名函数,
    所以 Python 中仍是采用不定参数结合逻辑判断对不同输入参数的情况, 在函数内部进行不同处理

    Python 提供了 `@overload` 注解, 可以标识一个函数为函数重载, 其使用形式如下:

    - 先定义一个可传递多种类型参数的函数, 并完成该函数的函数体, 作为实际被调用的函数
    - 基于上面定义的函数, 通过 `@overload` 装饰器, 为函数定义不同的函数签名 (即函数体为 `pass` 或 `...`)
    - 在调用时该函数时, 参数列表可匹配任一标记了 `@overload` 装饰器的函数签名

    注意:

    - 如果要使用 `@overload` 装饰器, 则必须要定义一个可以满足所有参数传递的函数, 并为该函数至少配置两个标记了 `@overload`
    装饰器的函数签名;
    - 标记 `@overload` 装饰器的函数签名, 必须要声明在实际函数之前;

    注意: `@overload` 注解只能用于函数定义, 不能用于函数实现, 也就是说, 被 `@overload`
    装饰器标记的函数并不能真正执行, 只是代表一个函数签名的表示, 告诉调用方该函数调用时可以传递的参数和返回值
    """

    # 为 `add` 函数定义具备两个数值类型参数的重载, 该函数返回一个数值类型值
    @overload
    def add(a: int | float, b: int | float) -> int | float: ...

    # 为 `add` 函数定义第一个参数为 str 类型的重载, 该函数返回一个 str 类型值
    @overload
    def add(a: str, b: Any) -> str: ...

    # 为 `add` 函数定义第一个参数为 list 类型参数的重载, 该函数返回一个 list 类型值
    @overload
    def add[T: Any](a: list[T], b: T) -> list[Any]: ...

    # 为 `add` 函数定义两个参数为 list 类型参数的重载, 该函数返回一个 list 类型值
    @overload
    def add[T: Any](a: list[T], b: list[T]) -> list[Any]: ...

    def add(*args: Any, **kwargs: Any) -> int | float | str | list[Any]:
        """定义满足上述重载函数签名的真实可调用函数

        该函数的参数列表以及函数实现必须覆盖上述所有标记了 `@overload` 装饰器的函数签名要求
        """
        # 定义函数返回值
        result: int | float | str | list[Any]

        # 匹配函数参数列表, 获取参数 a 和 b 的值

        # 尝试从 args 参数中获取参数 a 和 b 的值
        match args:
            case x if len(x) >= 2:
                a, b = args
            case x if len(x) == 1:
                a = args[0]

        # 尝试从 kwargs 参数中获取参数 a 和 b 的值
        if "a" in kwargs:
            a = kwargs["a"]

        if "b" in kwargs:
            b = kwargs["b"]

        # 确认参数 a 和 b 必须存在
        if "a" not in locals() or "b" not in locals():
            raise ValueError("arguments a and b must be specified")

        # 根据参数类型不同, 对参数 a 和 b 进行计算
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            result = a + b
        elif isinstance(a, str):
            result = f"{a}{b}"
        elif isinstance(a, list):
            if isinstance(b, list):
                result = a + b
            else:
                result = [*a, b]
        else:
            raise ValueError("invalid arguments type")

        return result

    r: Any

    # 测试按照不同的函数重载形式调用 add 函数

    r = add(1, 2)
    assert r == 3

    r = add(0.1, 0.2)
    assert abs(r - 0.3) < 0.00001

    r = add("Hello", 123)
    assert r == "Hello123"

    r = add([1, 2, 3, 4], 5)
    assert r == [1, 2, 3, 4, 5]

    r = add([1, 2, 3, 4], [5, 6])
    assert r == [1, 2, 3, 4, 5, 6]

    r = add(a=100, b=200)
    assert r == 300

    r = add("Hello", b="World")
    assert r == "HelloWorld"
