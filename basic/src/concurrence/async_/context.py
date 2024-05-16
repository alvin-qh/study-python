from contextlib import asynccontextmanager
import random
from types import TracebackType
from typing import Any, AsyncIterator, Dict, Optional, Self, Tuple, Type


class AsyncContext:
    """异步上下文管理类

    具备 `__aenter__` 和 `__aexit__` 方法的类对象为上下文对象

    可以通过 `with` 关键字定义上下文对象的有效范围
    """

    _kv: Dict[str, Any]
    exception: Optional[Tuple[Optional[Type[Exception]], Optional[Exception]]]

    def __init__(self, suppress_exception: bool = False) -> None:
        """构造上下文对象

        Args:
            `suppress_exception` (`bool`, optional): 是否制约上下文范围内的异常. Defaults to `False`.
        """
        self._kv = {}  # 存放键值对的字典
        self._suppress_exception = suppress_exception

        self.exception = None  # 保存异常类型和异常对象的元祖

    def put(self, key: str, val: Any) -> None:
        """根据 Key 存储一个 Value

        Args:
            `key` (`str`): Key 值
            `val` (`Any`): Value 值
        """
        self._kv[key] = val

    def get(self, key: str) -> Any:
        """根据 Key 获取对应的 Value

        Args:
            `key` (`str`): Key 值

        Returns:
            `Any`: Value 值
        """
        return self._kv[key]

    async def close(self) -> None:
        """关闭上下文对象 (异步)"""
        # 清理 Key/Value 字典
        self._kv = {}

    async def __aenter__(self) -> Self:
        """进入上下文范围时执行的方法, 返回上下文对象 (异步)

        返回的上下文对象必须具备 `__exit__` 方法, 可以为其它对象,
        也可以是当前对象

        Returns:
            `Context`: 当前对象
        """
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[Exception]],
        exc_value: Optional[Exception],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        """退出上下文范围时执行的方法 (异步)

        Args:
            `exc_type` (`Optional[Type[Exception]]`): 在上下文范围中抛出异常类型, 无异常则为 `None`
            `exc_value` (`Optional[Exception]`): 在上下文范围中抛出异常对象, 无异常则为 `None`
            `exc_tb` (`Optional[TracebackType]`): 在上下文范围中抛出异常堆栈, 无异常则为 `None`

        Returns:
            `bool`: `True` 表示异常不会抛出到上下文范围之外
        """
        await self.close()
        self.exception = (exc_type, exc_value)

        return self._suppress_exception


_CONTEXT_NUMS = [1, 2, 3, 4, 5, 6, 7]


@asynccontextmanager
async def async_random_number_context() -> AsyncIterator[int]:
    """生成随机数上下文 (异步)

    被 `@asynccontextmanager` 装饰器修饰的函数可以管理异步上下文, 该方法返回 `_AsyncGeneratorContextManager[T]` 类型对象,
    (在本例中为 `_AsyncGeneratorContextManager[int]` 类型), 相当于一个实现了 `__aenter__` 以及 `__aexit__` 方法的类型实
    例, 表示一个异步环境中使用的上下文管理器对象

    `@asynccontextmanager` 装饰器可以简化异步上下文类型的定义, 而使用则完全类似普通的异步上下文类型实例, 即:

    ```python
    with async_random_number_context() as n:
        ...

    ```

    Yields:
        `int`: 随机数值
    """
    if len(_CONTEXT_NUMS) == 0:
        raise IndexError("random number out of range")

    # 在读取上下文前执行
    pos = random.randint(0, len(_CONTEXT_NUMS) - 1)

    # 返回上下文值
    yield _CONTEXT_NUMS[pos]

    # 在读取上下文后执行
    del _CONTEXT_NUMS[pos]
