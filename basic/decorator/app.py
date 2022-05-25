from typing import Any, Callable, Dict, TypeVar

F = TypeVar("F", bound=Callable)


class App:
    """
    定义一个包含装饰器方法的类

    类中的装饰器方法可以通过 `@类对象.方法` 来使用
    """

    _func_map: Dict[str, Callable]

    def __init__(self) -> None:
        self._func_map = {}

    def register(self, url: str) -> Callable:
        """
        该方法返回一个装饰器函数, 用于为某个 URL 注册执行函数

        Args:
            url (str): 用于注册执行函数的 URL

        Returns:
            Callable: 执行函数
        """

        def wrapper(func: F) -> F:
            """
            装饰器方法, 将传入的执行函数进行注册

            Args:
                func (F): 执行函数

            Returns:
                F: 执行函数, 和参数 func 相同
            """
            # 通过定义的 URL 对执行函数进行注册
            self._func_map[url] = func
            return func

        return wrapper

    def execute(self, url: str) -> Any:
        """
        根据给定的 URL 获取执行函数并执行

        Args:
            url (str): URL

        Raises:
            KeyError: URL 未注册执行函数

        Returns:
            Any: 执行函数
        """
        # 根据 URL 获取执行函数
        func = self._func_map.get(url)
        if not func:
            raise KeyError(f"\"{url}\" not register")

        # 执行该函数并返回结果
        return func()
