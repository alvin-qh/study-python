import asyncio as aio
import timeit
from typing import Any, Dict

import pytest


@pytest.mark.asyncio
async def test_condition_lock() -> None:
    """带状态的协程锁

    - `Condition lock` 相当于一个带状态的锁
    - 对于有多个协程在锁对象上进行等待的情况, `Condition lock` 允许设定解锁多少个协程
    - 通知指定数量的协程: `condition.notify(count)`
    - 通知所有协程: `condition.notify_all()`

    - 在协程上进行等待:

        ```python
        await cond.acquire()
        try:
            pass
        finally:
            cond.release()
        ```

        或

        ```python
        async with cond:
            pass
        ```
    """
    # 生成锁对象
    cond = aio.Condition()

    # 生成开始时间
    start_time = timeit.default_timer()

    async def cond_job(id_: int) -> Dict[str, Any]:
        """测试带状态的协程锁对象

        Args:
            - `id_` (`int`): ID 标识符

        Returns:
            `Dict[str, Any]`: 返回 ID 标识符和执行时间组成的字典
        """
        # 进入锁
        async with cond:
            # 等待锁通知
            await cond.wait()

        return {
            "id": id_,  # ID 值
            "finish_time": round(timeit.default_timer() - start_time, 1),  # 执行时间
        }

    group = aio.gather(
        cond_job(1),
        cond_job(2),
        cond_job(3),
    )

    # 等待 1 秒后
    await aio.sleep(0.2)

    # 通知 2 个锁
    async with cond:
        cond.notify(2)

    # 再等待 2 秒后
    await aio.sleep(0.2)

    # 通知所有锁
    async with cond:
        cond.notify_all()

    # 等待所有协程结束
    r = await group

    # 第一个结果为 ID=1 函数返回, 为第一次通知解锁
    assert r[0]["id"] == 1
    assert r[0]["finish_time"] == 0.2  # 整体执行 2 秒

    # 第二个结果为 ID=2 函数返回, 为第一次通知解锁
    assert r[1]["id"] == 2
    assert r[1]["finish_time"] == 0.2  # 整体执行 2 秒

    # 第三个结果为 ID=3 函数返回, 为第二次通知解锁
    assert r[2]["id"] == 3
    assert r[2]["finish_time"] == 0.4  # 整体执行 4 秒


@pytest.mark.asyncio
async def test_semaphore() -> None:
    """信号量

    - 信号量可以指定一个数量, 表示多少个信号可以使用, 每个协程可以占用一个信号并在稍后释放它, 当所有的信号被占用后，后续的协程会进入等待,
    直到之后有一个信号被释放
    - 占用信号: `semaphore.acquire()`
    - 释放信号: `semaphore.release()`
    - 检测是否可以占用信号: `semaphore.locked()`
    - 仍可以用 `async with` 方式来简化信号量的使用:

        ```python
        semaphore.acquire()
        try:
            pass
        finally:
            semaphore.release()
        ```

        或

        ```python
        async with semaphore:
            pass
        ```
    """
    # 生成信号量对象, 具备两个信号
    sem = aio.Semaphore(2)

    # 生成开始时间
    start_time = timeit.default_timer()

    async def sem_job(id_: int) -> Dict[str, Any]:
        """测试信号量对象

        Args:
            - `id_` (`int`): ID 标识符

        Returns:
            `Dict[str, Any]`: 返回 ID 标识符和执行时间组成的字典
        """
        # 进入信号量
        async with sem:
            # 协程等待 2 秒钟后退出信号量
            await aio.sleep(0.2)

        return {
            "id": id_,  # ID 值
            "finish_time": round(timeit.default_timer() - start_time, 1),  # 执行时间
        }

    r = await aio.gather(
        sem_job(1),
        sem_job(2),
        sem_job(3),
    )

    # 第一个结果为 ID=1 函数返回, 对应前两个信号
    assert r[0]["id"] == 1
    assert r[0]["finish_time"] == 0.2  # 整体执行 2 秒

    # 第二个结果为 ID=2 函数返回, 对应前两个信号
    assert r[1]["id"] == 2
    assert r[1]["finish_time"] == 0.2  # 整体执行 4 秒

    # 第三个结果为 ID=3 函数返回, 对应后两个信号
    assert r[2]["id"] == 3
    assert r[2]["finish_time"] == 0.4  # 整体执行 2 秒
