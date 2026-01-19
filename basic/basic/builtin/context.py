import random
from contextlib import contextmanager
from types import TracebackType
from typing import Any, Generator, Type


class Context:
    """上下文管理类

    具备 `__enter__` 和 `__exit__` 方法的类对象为上下文对象

    可以通过 `with` 关键字定义上下文对象的有效范围
    """

    _kv: dict[str, Any]
    exception: tuple[Type[Exception] | None, Exception | None] | None

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
            Any: Value 值
        """
        return self._kv[key]

    def close(self) -> None:
        """关闭上下文对象"""
        # 清理 Key/Value 字典
        self._kv = {}

    def __enter__(self) -> "Context":
        """进入上下文范围时执行的方法, 返回上下文对象

        返回的上下文对象必须具备 `__exit__` 方法, 可以为其它对象,
        也可以是当前对象

        Returns:
            `Context`: 当前对象
        """
        return self

    def __exit__(
        self,
        exc_type: Type[Exception] | None,
        exc_value: Exception | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        """退出上下文范围时执行的方法

        Args:
            `exc_type` (`Optional[Type[Exception]]`): 在上下文范围中抛出异常类型, 无异常则为 `None`
            `exc_value` (`Optional[Exception]`): 在上下文范围中抛出异常对象, 无异常则为 `None`
            `exc_tb` (`Optional[TracebackType]`): 在上下文范围中抛出异常堆栈, 无异常则为 `None`

        Returns:
            `bool`: `True` 表示异常不会抛出到上下文范围之外
        """
        self.close()
        self.exception = (exc_type, exc_value)

        return self._suppress_exception


_CONTEXT_NUMS = [1, 2, 3, 4, 5, 6, 7]


@contextmanager
def random_number_context() -> Generator[int, None, None]:
    """生成随机数上下文

    被 `@contextmanager` 装饰器修饰的函数可以管理上下文, 该方法返回 `_GeneratorContextManager[T]` 类型对象,
    (在本例中为 `_GeneratorContextManager[int]` 类型), 相当于一个实现了 `__enter__` 以及 `__exit__` 方法
    的类型实例

    `@contextmanager` 装饰器可以简化上下文类型的定义, 而使用则完全类似普通的上下文类型实例, 即:

    ```python
    with random_number_context() as n:
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
