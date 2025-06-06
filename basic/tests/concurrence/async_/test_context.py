import asyncio as aio
from contextvars import ContextVar

import pytest

from basic.concurrence.async_.context import AsyncContext, async_random_number_context


@pytest.mark.asyncio
async def test_async_context_var_with_concurrency() -> None:
    """在并发调用中测试上下文对象

    通过 `ContextVar` 可以定义一个上下文对象, 该对象可以在同一个线程上下文进行传递

    在并发调用中, `ContextVar` 实例在每个异步任务中会被"复制"一次, 表现的结果就是:
    1. 每个并发并发任务 (协程并发或线程并发) 持有自己的上下文实例;
    2. 并发任务中持有的上下文实例是外部的一个副本, 继承外部设置的值;
    3. 并发协程之间持有的上下文实例是从一个上下文复制得到, 所以实例并不相同, 共享数据, 且对数据修改相互隔离;
    4. 子任务持有父任务上下文的副本, 所以子任务和父任务的实例并不相同, 共享数据, 且对数据修改相互隔离;
    5. 上下文实例使用"写时拷贝"策略, 所以如果不对上下文实例进行写操作, 上下文实例不会对数据进行复制;
    """
    ctx: ContextVar[str] = ContextVar("test")
    ctx.set("default")

    async def task_parent(value: str) -> None:
        """外部任务

        该任务继承"根"上下文实例, 并为其设置新值

        Args:
            `value` (`str`): 要设置给上下文实例的值
        """
        # 这里取到的上下文值是从"根"上下文复制得到
        assert ctx.get() == "default"
        # 这里设置的上下文值不会影响"根"上下文实例
        ctx.set(f"{value} from parent")

        # 并发执行两个 `task_child1` 和 `task_child1` 任务, 并设置相同的上下文值
        await aio.gather(
            task_child1(value),
            task_child2(value),
        )

        # 并发执行完毕后, 上下文实例的值依然是在本函数中设置的值
        # 即 `task_child1` 和 `task_child2` 任务的执行并无法改变根上下文实例的值, 只是改变了其副本的值
        assert ctx.get() == f"{value} from parent"

    async def task_child1(value: str) -> None:
        """内部任务

        该任务继承从 `task_parent` 设置的上下文实例, 并对其进行修改

        Args:
            `value` (`str`): 要设置给上下文实例的值
        """
        # 这里取到的上下文值是从外部上下文复制得到
        assert ctx.get() == f"{value} from parent"
        # 这里设置的上下文值不会影响外部上下文实例
        ctx.set(f"{value} from child1")

        # 并发执行的 `task_child2` 任务, 对当前任务的上下文不会有任何影响
        await aio.sleep(0.5)
        assert ctx.get() == f"{value} from child1"

    async def task_child2(value: str) -> None:
        """内部任务

        该任务继承从 `task_parent` 设置的上下文实例, 并对其进行修改

        Args:
            `value` (`str`): 要设置给上下文实例的值
        """
        # 这里取到的上下文值是从外部上下文复制得到
        assert ctx.get() == f"{value} from parent"
        # 这里设置的上下文值不会影响外部上下文实例
        ctx.set(f"{value} from child2")

        # 并发执行的 `task_child1` 任务, 对当前任务的上下文不会有任何影响
        await aio.sleep(0.5)
        assert ctx.get() == f"{value} from child2"

    # 并发执行两个 `task_parent` 任务, 并设置不同的上下文值
    await aio.gather(
        task_parent("1"),
        task_parent("2"),
    )

    # 并发执行完毕后, 上下文实例的值依然是 "default"
    # 即 `task_parent` 任务的执行并无法改变根上下文实例的值, 只是改变了其副本的值
    assert ctx.get() == "default"


@pytest.mark.asyncio
async def test_async_context_var_without_concurrency() -> None:
    """在非并发调用中测试上下文对象

    如果协程方法并不是并发执行, 仅是通过 `await` 对其执行结果进行等待 (即协程函数仍是顺序执行), 则不会对上下文进行复制, 此时
    调用链上所有的函数访问的都是同一个上下文实例
    """
    ctx: ContextVar[str] = ContextVar("test")
    ctx.set("default")

    async def task_parent(value: str) -> None:
        """外部任务

        该任务中使用的上下文实例和"根"上下文实例相同, 所以对上下文的修改是全局的

        Args:
            `value` (`str`): 要设置给上下文实例的值
        """
        assert ctx.get() == "default"
        ctx.set(f"{value} from parent")

        # 等待 `task_child1` 和 `task_child1` 函数依次调用完成
        await task_child1(value)
        await task_child2(value)

    async def task_child1(value: str) -> None:
        """内部任务 1

        该任务继承 `task_parent` 的上下文实例, 并为其设置新值

        Args:
            `value` (`str`): 要设置给上下文实例的值
        """
        # 这里获取到的值是在 `task_parent` 中设置的
        assert ctx.get() == f"{value} from parent"
        # 这里设置的值将会被后续的函数读取, 即 `task_child2` 函数
        ctx.set(f"{value} from child1")

    async def task_child2(value: str) -> None:
        """内部任务 2

        该任务继承 `task_parent` 的上下文实例, 并为其设置新值

        Args:
            `value` (`str`): 要设置给上下文实例的值
        """
        # 因为本函数在 `task_child1` 函数之后执行, 所以这里的值是在 `task_child1` 中设置的
        assert ctx.get() == f"{value} from child1"
        # 这里设置的值将是上下文实例最后最终呈现的值
        ctx.set(f"{value} from child2")

    # 等待 `task_parent` 函数依次调用完成
    await task_parent("1")
    # "根"上下文已被修改, 说明 `task_parent` 函数内部改变了"根"上下文实例
    assert ctx.get() == "1 from child2"


@pytest.mark.asyncio
async def test_async_context_var_with_async_tasks() -> None:
    """通过异步任务改造 `test_async_context_var_without_concurrency` 范例

    通过 `aio.create_task(...)` 方法可以将一个异步函数放入消息队列, 使其成为并发执行的任务, 此时协程函数中对上下文的操作就会发生复制
    """
    ctx: ContextVar[str] = ContextVar("test")
    ctx.set("default")

    async def task_parent(value: str) -> None:
        """外部任务

        该任务继承"根"上下文实例, 并为其设置新值

        Args:
            `value` (`str`): 要设置给上下文实例的值
        """
        # 这里取到的上下文值是从"根"上下文复制得到
        assert ctx.get() == "default"
        # 这里设置的上下文值不会影响"根"上下文实例
        ctx.set(f"{value} from parent")

        # 并发执行两个 `task_child1` 和 `task_child1` 任务, 并设置相同的上下文值
        # 这里两个任务并不是"同时"执行, 而是按顺序执行, 但因为建立了 Task, 所以也是放入消息队列, 本质上是并发任务
        await aio.create_task(task_child1(value))
        await aio.create_task(task_child2(value))

    async def task_child1(value: str) -> None:
        """内部任务 2

        该任务继承 `task_parent` 的上下文实例, 并为其设置新值

        Args:
            `value` (`str`): 要设置给上下文实例的值
        """
        # 这里取到的上下文值是从外部上下文复制得到
        assert ctx.get() == f"{value} from parent"
        # 这里设置的上下文值不会影响外部上下文实例
        ctx.set(f"{value} from child1")

        # 并发执行的 `task_child2` 任务, 对当前任务的上下文不会有任何影响
        await aio.sleep(0.5)
        assert ctx.get() == f"{value} from child1"

    async def task_child2(value: str) -> None:
        """内部任务 2

        该任务继承 `task_parent` 的上下文实例, 并为其设置新值

        Args:
            `value` (`str`): 要设置给上下文实例的值
        """
        # 这里取到的上下文值是从外部上下文复制得到
        assert ctx.get() == f"{value} from parent"
        # 这里设置的上下文值不会影响外部上下文实例
        ctx.set(f"{value} from child2")

        # 并发执行的 `task_child2` 任务, 对当前任务的上下文不会有任何影响
        await aio.sleep(0.5)
        assert ctx.get() == f"{value} from child2"

    # 等待 `task_parent` 函数依次调用完成
    await aio.create_task(task_parent("1"))
    # "根"上下文已被修改, 说明 `task_parent` 函数内部改变了"根"上下文实例
    assert ctx.get() == "default"


@pytest.mark.asyncio
async def test_async_context_scope() -> None:
    """测试异步上下文范围和上下文对象"""
    async with AsyncContext() as ctx:
        ctx.put("A", 100)
        ctx.put("B", 200)

        assert ctx.get("A") == 100
        assert ctx.get("B") == 200

    # 退出上下文范围后, 存储的 Key/Value 不可用
    with pytest.raises(KeyError):
        assert ctx.get("A")

    # 退出上下文范围后, 存储的 Key/Value 不可用
    with pytest.raises(KeyError):
        assert ctx.get("B")


@pytest.mark.asyncio
async def test_async_context_with_exception() -> None:
    """测试上下文范围内的异常抛出情况"""
    # 产生一个上下文对象并调用 __enter__ 方法进入上下文范围
    # suppress_exception 表示 __exit__ 方法返回 True, 异常不传递到上下文范围之外
    async with AsyncContext(suppress_exception=True) as ctx:
        # 抛出异常
        raise ValueError("error")

    assert ctx.exception is not None

    # 确认 __exit__ 方法的异常参数值
    assert ctx.exception[0] is ValueError
    assert str(ctx.exception[1]) == "error"


@pytest.mark.asyncio
async def test_context_from_asynccontextmanager() -> None:
    """测试上下文管理器

    测试被 `@contextmanager` 装饰器修饰的函数作为上下文管理器使用
    """
    nums = []

    while True:
        try:
            async with async_random_number_context() as n:
                nums.append(n)
        except IndexError as e:
            assert e.args[0] == "random number out of range"
            break

    assert sorted(nums) == [1, 2, 3, 4, 5, 6, 7]
