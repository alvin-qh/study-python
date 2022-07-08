import asyncio
from typing import Generator

from pytest import fixture


@fixture
def event_loop(
    scope="session",
) -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    定义 pytest 的 `fixture`, 为所有使用 `AbstractEventLoop` 对象的测试中提供 `event_loop` 对象

    Args:
        scope (str, optional): 该 `fixture` 起作用的测试范围, 可以为 `function`, `class`,
        `session`. Defaults to `session`.

    Yields:
        Generator[asyncio.AbstractEventLoop, None, None]: 返回一个生成器, 生成一个
        `AbstractEventLoop` 对象
    """
    # 获取当前协程的时间循环对象
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # 透出
    yield loop

    # 获取事件循环中待运行的所有任务
    pending = asyncio.tasks.all_tasks(loop)

    # 等待所有任务执行完毕
    loop.run_until_complete(asyncio.gather(*pending))

    # 等待 1 秒保证所有任务完毕后, 再关闭事件循环
    loop.run_until_complete(asyncio.sleep(1))
    loop.close()
