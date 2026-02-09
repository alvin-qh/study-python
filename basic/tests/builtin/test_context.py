import random
from contextlib import contextmanager
from typing import Generator

from pytest import raises

from basic.builtin import Context


def test_context_scope() -> None:
    """测试上下文范围和上下文对象"""
    # 产生一个上下文对象并调用 __enter__ 方法进入上下文范围
    # 退出上下文范围后会调用上下文对象的 __exit__ 方法
    with Context() as ctx:
        ctx.put("A", 100)
        ctx.put("B", 200)

        assert ctx.get("A") == 100
        assert ctx.get("B") == 200

    # 退出上下文范围后, 存储的 Key/Value 不可用
    with raises(KeyError):
        assert ctx.get("A")

    # 退出上下文范围后, 存储的 Key/Value 不可用
    with raises(KeyError):
        assert ctx.get("B")


def test_context_with_exception() -> None:
    """测试上下文范围内的异常抛出情况"""
    # 产生一个上下文对象并调用 __enter__ 方法进入上下文范围
    # suppress_exception 表示 __exit__ 方法返回 True, 异常不传递到上下文范围之外
    with Context(suppress_exception=True) as ctx:
        # 抛出异常
        raise ValueError("error")

    assert ctx.exception is not None

    # 确认 __exit__ 方法的异常参数值
    assert ctx.exception[0] is ValueError
    assert str(ctx.exception[1]) == "error"


class RandomNumberContext:
    def __init__(self) -> None:
        self._context_nums = [1, 2, 3, 4, 5, 6, 7]

    @contextmanager
    def context(self) -> Generator[int, None, None]:
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
        if len(self._context_nums) == 0:
            raise IndexError("random number out of range")

        # 在读取上下文前执行
        pos = random.randint(0, len(self._context_nums) - 1)

        # 返回上下文值
        yield self._context_nums[pos]

        # 在读取上下文后执行
        del self._context_nums[pos]


def test_context_from_contextmanager() -> None:
    """测试上下文管理器

    测试被 `@contextmanager` 装饰器修饰的函数作为上下文管理器使用
    """
    nums = []

    ctx = RandomNumberContext()

    while True:
        try:
            with ctx.context() as n:
                nums.append(n)
        except IndexError as e:
            assert e.args[0] == "random number out of range"
            break

    assert sorted(nums) == [1, 2, 3, 4, 5, 6, 7]
