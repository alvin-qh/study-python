import io
import timeit
from functools import wraps
from typing import Any, Callable, Dict


class App:
    """定义一个包含装饰器方法的类

    类中的装饰器方法可以通过 `@类对象.方法` 来使用
    """

    _func_map: Dict[str, Callable[..., Any]]

    def __init__(self) -> None:
        self._func_map = {}

    def register(self, url: str) -> Callable[..., Any]:
        """该方法返回一个装饰器函数, 用于为某个 URL 注册执行函数

        Args:
            - `url` (`str`): 用于注册执行函数的 URL

        Returns:
            `Callable[..., Any]`: 执行函数
        """

        def wrapper[F: Callable[..., Any]](func: F) -> F:
            """装饰器方法, 将传入的执行函数进行注册

            Args:
                - `func` (`F`): 执行函数

            Returns:
                `F`: 执行函数, 和参数 func 相同
            """
            # 通过定义的 URL 对执行函数进行注册
            self._func_map[url] = func
            return func

        return wrapper

    def execute(self, url: str) -> Any:
        """根据给定的 URL 获取执行函数并执行

        Args:
            - `url` (`str`): URL

        Raises:
            `KeyError`: URL 未注册执行函数

        Returns:
            `Any`: 执行函数的结果
        """
        # 根据 URL 获取执行函数
        func = self._func_map.get(url)
        if not func:
            raise KeyError(f'"{url}" not register')

        # 执行该函数并返回结果
        return func()


class Logger:
    """用于记录日志的类

    该类具备一个 `__call__` 魔法函数, 其对象可以被用作仿函数, 且定义为装饰器函数
    """

    def __init__(self) -> None:
        """初始化缓冲区存放字符串"""
        self._buf = io.StringIO()

    def __call__(self, fn: Callable[..., Any]) -> Callable[..., Any]:
        """仿函数调用, 将当前对象作为一个装饰器

        该装饰器在函数调用后记录一条日志到缓冲区

        Args:
            - `fn` (`Callable[..., Any]`): 被代理函数

        Returns:
            `Callable[..., Any]`: 代理函数,
        """

        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = timeit.default_timer()
            result = fn(*args, **kwargs)

            # 记录函数调用时间
            time_cost = timeit.default_timer() - start_time

            # 记录被调用的函数名称
            self._buf.write(f"\tlog function '{fn.__name__}' is call: \n")
            self._buf.write(f"\t  function={fn.__name__}\n")

            # 记录传递的参数
            self._buf.write("\t  arguments=")
            if args:
                self._buf.write(f"{args} ")
            if kwargs:
                self._buf.write(f"{kwargs} ")
            self._buf.write("\n")

            # 记录返回值
            self._buf.write(f"\t  return={result}\n")

            # 记录调用时间
            self._buf.write(f"\t  time={time_cost:.6f} sec\n")

            return result

        return wrapper

    def reset(self) -> None:
        """重置缓存"""

        self._buf.seek(0)

    def __str__(self) -> str:
        """缓存内容转为字符串, 输出日志内容

        Returns:
            `str`: 日志内容
        """
        return self._buf.getvalue()
