from typing import Any, cast, overload


def test_override_functions() -> None:
    """定义函数重载

    Python 没有真正的函数重载概念, 也就是不能在一个作用域范围内定义多个同名函数,
    所以 Python 中仍是采用不定参数结合逻辑判断对不同输入参数进行不同处理

    Python 提供了 `@overload` 注解, 可以标识
    """

    @overload
    def add(a: int | float, b: int | float) -> int | float: ...

    @overload
    def add(a: str, b: Any) -> str: ...

    @overload
    def add[T: Any](a: list[T], b: T) -> list[Any]: ...

    @overload
    def add[T: Any](a: list[T], b: list[T]) -> list[Any]: ...

    def add(*args: Any, **kwargs: Any) -> int | float | str | list[Any]:
        result: int | float | str | list[Any]

        match args:
            case x if len(x) >= 2:
                a, b = args
            case x if len(x) == 1:
                a = args[0]

        if "a" in kwargs:
            a = kwargs["a"]

        if "b" in kwargs:
            b = kwargs["b"]

        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            result = a + b
        elif isinstance(a, str):
            result = f"{a}{b}"
        elif isinstance(a, list):
            if isinstance(b, list):
                result = a + b
            else:
                result = [*a, b]

        return result

    r: Any

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


def test_override_method() -> None:
    """测试类成员函数重载"""

    class DemoClass:
        _result: int | float | str | list[Any]

        @overload
        def __init__(self, a: int | float, b: int | float) -> None: ...

        @overload
        def __init__(self, a: str, b: Any) -> None: ...

        @overload
        def __init__[T: Any](self, a: list[T], b: T) -> None: ...

        @overload
        def __init__[T: Any](self, a: list[T], b: list[T]) -> None: ...

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            match args:
                case x if len(x) >= 2:
                    a, b = args
                case x if len(x) == 1:
                    a = args[0]

            if "a" in kwargs:
                a = kwargs["a"]

            if "b" in kwargs:
                b = kwargs["b"]

            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                self._result = a + b
            elif isinstance(a, str):
                self._result = f"{a}{b}"
            elif isinstance(a, list):
                if isinstance(b, list):
                    self._result = a + b
                else:
                    self._result = [*a, b]

        def __int__(self) -> int:
            return cast(int, self._result)

        def __float__(self) -> float:
            return cast(float, self._result)

        def __str__(self) -> str:
            return cast(str, self._result)

        def __iter__(self) -> Any:
            if isinstance(self._result, list):
                return iter(self._result)

            return iter([self._result])

    c = DemoClass(10, b=20)
    assert int(c) == 30

    c = DemoClass(0.1, 0.2)
    assert abs(float(c) - 0.3) < 0.00001

    c = DemoClass("Hello", 123)
    assert str(c) == "Hello123"

    c = DemoClass([1, 2, 3], 4)
    assert list(c) == [1, 2, 3, 4]

    c = DemoClass([1, 2, 3, 4], [5, 6])
    assert list(c) == [1, 2, 3, 4, 5, 6]
