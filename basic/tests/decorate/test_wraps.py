from functools import wraps
from typing import Any, Callable


def _d1(func: Callable) -> Callable:
    """
    直接在装饰器函数中定义代理函数并返回, 会导致被装饰的函数名称被返回的代理函数取代

    Args:
        func (Callable): 被装饰函数

    Returns:
        Callable: 被装饰函数的代理函数
    """
    def wrapper(*args, **kwargs) -> Any:
        return func(*args, **kwargs)

    return wrapper


def _d2(func: Callable) -> Callable:
    """
    `functools` 包下面的 `wraps` 装饰器主要作用是将被装饰函数的 `__name__` 属性传递给代理函数,
    否则一个函数一旦被修饰, 其名称就会变为返回的代理函数名称

    Args:
        func (Callable): 被装饰函数

    Returns:
        Callable: 被装饰函数的代理函数, 函数的 `__name__` 属性和被代理函数一致
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        return func(*args, **kwargs)

    return wrapper


def test_wraps_decorator() -> None:
    """
    演示 `wraps` 装饰器的使用方法和效果
    """

    @_d1
    def d1_demo() -> None:
        pass

    @_d2
    def d2_demo() -> None:
        pass

    # d1_demo 函数的名称已经变为 @_d1 返回的代理函数名称
    assert d1_demo.__name__ == "wrapper"

    # d2_demo 函数的名称为 @_d2 返回的代理函数名称
    # 但这个函数的名称通过 wraps 装饰器处理后已经和被代理函数一致
    assert d2_demo.__name__ == "d2_demo"
