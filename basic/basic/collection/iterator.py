from typing import Iterator


class Iter:
    """定义一个迭代器类

    具备 `__next__` 方法的类对象可被迭代访问, 即通过 next 函数获取序列值

    具备 `__iter__` 方法的类对象被认为是一个迭代器对象, 可以在 `for ... in ...` 循环中使用
    """

    def __init__(self, min_: int, max_: int) -> None:
        """初始化迭代器

        该迭代器表示一个 `[min, max)` 区间的递增数列

        Args:
            - `min_` (`int`): 起始值
            - `max_` (`int`): 结束值
        """
        # self._cur 保存当前迭代的值
        self._min = self._cur = min_
        self._max = max_

    def __iter__(self) -> Iterator[int]:
        """获取迭代器

        由于 `Iter` 类本身就是可迭代的, 所以该方法只是返回当前对象

        Returns:
            `Iterator[int]`: 返回一个迭代器对象
        """
        return self

    def __next__(self) -> int:
        """返回迭代对象的下一项

        具备 `__next__` 方法的类可被迭代, 即可通过 `next(...)` 函数返回迭代对象的下一项

        Raises:
            `StopIteration`: 迭代器终止

        Returns:
            `int`: 下一项值
        """
        if self._cur == self._max:
            # 抛出该异常表示迭代结束
            raise StopIteration()

        # 返回当前值
        _cur = self._cur
        # 当前值变为下一个值
        self._cur += 1
        return _cur
