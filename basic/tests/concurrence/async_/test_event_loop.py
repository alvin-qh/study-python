import asyncio as aio
import time
import timeit
from typing import Any, Dict


def test_event_loop() -> None:
    """测试事件循环

    Python 的异步处理是通过"事件循环"实现的, 即将任务放入事件队列后, 通过事件循环执行
    """
    # 创建一个事件循环
    loop = aio.new_event_loop()
    assert loop is not None

    async def event_future() -> None:
        """定义一个异步函数"""
        assert aio.get_running_loop() is loop

    # 将异步函数调用放入时间循环, 并等待其执行结束
    loop.run_until_complete(event_future())


def test_none_async_call_in_event_loop() -> None:
    """在事件循环中调用非协程函数

    - 非协程函数也可以放入事件队列中, 但这类函数的调用是完全阻塞式的, 无法在使用 IO 的时候切换到另一个调用, 相当于同步执行了一个函数
    - 可以指定函数在事件循环中执行的时机. 包括：立即执行, 稍后执行和指定执行时间

        ```python
        event_loop.call_soon(function, args, context=None)
        event_loop.call_later(seconds, function, args, context=None)
        event_loop.call_at(when, function, args, context=None)
        ```

        注意: 由于这些方法在事件循环中中是同步执行的, 即前一个执行完毕后后一个才能执行,
        所以设定时间只能安排函数的具体执行顺序而无法准确的定义执行的时间

    - 如果事件循环中没有包含协程函数调用, 则无法使用队列的 `run_until_complete` 函数来自动化事件队列的生命周期,
    只能让队列一直存在直到显式将其结束

        ```python
        event_loop.run_forever()
        ...
        event_loop.stop()
        ```

    - 另外, `event_loop.call_soon` 函数并不能让指定的调用立即执行, 因为此时当前线程还在执行代码, 事件循环得不到执行机会,
    只有当前线程执行完指定代码后, 才有机会调度事件循环从事件队列中执行一个函数
    """

    # 记录结束任务和其结束的时间
    called_tasks: Dict[int, float] = {}

    # 记录起始时间
    start: float = 0

    def sync_func(id_: int) -> None:
        """同步方法

        该函数消息队列中被 同步 调用, 所以无法并发执行 IO 操作 (例如 sleep)
        """
        # 记录被调用的任务 id 和被调用的时间
        called_tasks[id_] = timeit.default_timer() - start

        # 用 sleep 方法阻塞当前线程, 同时阻塞协程队列
        time.sleep(0.1)

    async def main(loop: aio.AbstractEventLoop) -> None:
        # 立即执行 id=1
        loop.call_soon(sync_func, 1)

        # 立即执行 id=2
        loop.call_soon(sync_func, 2)

        # 设置 100 毫秒后执行 id=3, 由于 200 毫秒后 id=4 会执行, 耗时 100 毫秒, 所以 id=3 会在 id=4 后执行实际在 300 毫秒后执行

        loop.call_later(0.2, sync_func, 3)
        # 设置 200 毫秒后执行 id=4, 由于 id=1 和 id=2 一共会执行 200 毫秒, 所以 id=4 会在 id=2 之后被执行
        loop.call_later(0.1, sync_func, 4)

        # 获取协程执行的当前时间
        now = loop.time()

        # 指定在协程当前时间后第 300 毫秒执行 id=5, 但由于之前的操作已经耗费了 400 毫秒, 所以该函数只能在第 400 毫秒时被执行
        # 如果将参数改为 now + 0.2, 则 id=5 会先于 id=3 被执行（即在 id=4 之后）
        loop.call_at(now + 0.3, sync_func, 5)

        while len(called_tasks) < 5:
            await aio.sleep(0.5)

    # 记录程序开始时间
    start = timeit.default_timer()

    loop = aio.new_event_loop()
    try:
        loop.run_until_complete(main(loop))
    finally:
        loop.close()

    # id=1 立即执行
    assert round(called_tasks[1], 1) == 0
    # id=2 于 100 毫秒后执行 (在 id=1 执行完毕后执行)
    assert round(called_tasks[2], 1) == 0.1
    # id=3 于 300 毫秒后执行 (在 id=4 执行完毕后执行)
    assert round(called_tasks[3], 1) == 0.3
    # id=4 于 200 毫秒后执行 (在 id=2 执行完毕后执行)
    assert round(called_tasks[4], 1) == 0.2
    # id=5 于 400 毫秒后执行 (在 id=3 执行完毕后执行)
    assert round(called_tasks[5], 1) == 0.4


def test_async_lock() -> None:
    """协程锁对象 `Lock`

    - 协程的 IO 操作是异步进行的, 所以某些情况下仍需要同步对象对 IO 操作进行同步化, 以规约异步 IO 操作的顺序
    - 协程的同步对象效率很高 (线程同步对象要进入内核态，效率相对低), 并不是真正从 CPU 层进行执行同步, 只是限定了多个协程间的代码执行顺序
    - 锁是最基本的同步对象, 持有相同锁对象的协程, 同时只有一个可以执行

    锁的用法如下:

    ```python
    try:
        lock.acquire() # 抢占锁，如锁被占用则进入等待
        ...
    finally:
        lock.release() # 释放锁
    ```

    或

    ```python
    async with lock
    ```

    - `async with` 是 Python3.7 的新语法，即一个异步的 `with` 操作
    """
    # 定义协程锁
    lock = aio.Lock()

    # 生成开始时间
    start_time = timeit.default_timer()

    async def locked_job(id_: int) -> Dict[str, Any]:
        """测试协程函数

        Args:
            - `id_` (`int`): ID 标识符

        Returns:
            `Dict[str, Any]`: 返回 ID 标识符和执行时间组成的字典
        """
        # 进入锁
        async with lock:
            # 延迟 1 秒钟后退出锁
            await aio.sleep(0.1)

        return {
            "id": id_,  # ID 值
            "finish_time": round(timeit.default_timer() - start_time, 1),  # 执行时间
        }

    async def main() -> None:
        """协程入口函数"""

        # 组合两个协程函数同时执行
        r = await aio.gather(locked_job(1), locked_job(2))
        assert len(r) == 2

        # 第一个结果为 ID=1 函数返回
        assert r[0]["id"] == 1
        assert r[0]["finish_time"] == 0.1  # 整体执行 100 毫秒

        # 第二个结果为 ID=2 函数返回
        assert r[1]["id"] == 2
        assert r[1]["finish_time"] == 0.2  # 整体执行 200 毫秒

    aio.run(main())
