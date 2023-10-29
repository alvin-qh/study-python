import asyncio
from typing import AsyncGenerator


class AIOTicker:
    """
    从 `0` 到 `to` 每隔 `delay` 秒产生一个数字

    协程异步数字产生类型,

    Python 具备 `__iter__` 和 `__next__` 两个魔法方法, 前者用于返回一个迭代器对象, 后者用于返回每次
    迭代的结果. 具备 `__next__` 方法的类型可被看作是一个迭代器类型, 具备 `__iter__` 方法的类型可以返
    回一个迭代器对象, 可被用于 `for ... in ...` 形式的循环中.

    对于协程异步 (`asyncio`) 方式, Python 也提供了一系列魔法方法和非异步方式对应, 包括:
    - `__aiter__` 返回值为一个具备 `__anext__` 方法的对象, 表示返回一个异步迭代器对象
    - `__anext__` 异步返回下一个迭代值, 方法必须声明为 `async`, 可被用于 `async for ... in ...`
    形式的循环中
    """

    def __init__(self, delay: int, to: int) -> None:
        """
        初始化对象

        Args:
            delay (int): 每次产生数字的间隔
            to (int): 最大产生的数值上限
        """
        self._delay = delay
        self._from = 0
        self._to = to

    def __aiter__(self) -> "AIOTicker":
        """
        获取协程异步迭代器对象

        Returns:
            AIOTicker: 返回当前对象本身, 当前对象本身具备 `__anext__` 方法, 表示一个异步迭代器
        """
        return self

    async def __anext__(self) -> int:
        """
        异步返回下一个迭代值

        具备该方法的类型可作为一个 "异步迭代器" 类型, 其对象可以通过 `for ... in ...` 的语法进行迭代

        Raises:
            StopAsyncIteration: 表示迭代结束的异常

        Returns:
            int: 下一个迭代值
        """
        num = self._from
        if num >= self._to:
            raise StopAsyncIteration()

        self._from += 1
        if self._from:
            # 除第一次外, 每次迭代间隔指定时间
            await asyncio.sleep(self._delay)

        return num


async def ticker(delay: int, to: int) -> AsyncGenerator[int, None]:
    """
    异步生成器函数, 返回一个 `AsyncGenerator` 类型的对象, 表示异步生成器对象

    Args:
        delay (int): 每次迭代的间隔时间
        to (int): 最大的迭代上限值

    Returns:
        AsyncGenerator[int, None]: 异步生成器对象, 通过该生成器可以按设定产生期望的值

    Yields:
        int: 每次迭代产生的值
    """
    for i in range(to):
        yield i
        await asyncio.sleep(delay)


async def async_echo(delay: int, to: int) -> AsyncGenerator[int, int]:
    """
    返回一个可交互的 `Generator` 对象

    Args:
        delay (int): 每次迭代间隔时间
        to (int): 最大迭代值

    Returns:
        AsyncGenerator[int, int]: 异步生成器对象, 生成整数值, 可以发送整数值

    Yields:
        int: 产生一个整数值
    """
    # 生成 0 值, 读取一个值
    v = yield 0

    # 循环直到最大值
    for _ in range(to):
        # 将上次读取的值进行运算
        v *= 10
        # 生成 v 值到客户端
        yield v

        # 休眠指定的间隔时间
        await asyncio.sleep(delay)

        # 接收新值
        v = yield v
        # 如果接收到 0 值, 结束
        if v == 0:
            break
