import asyncio as aio
import time
import timeit
from threading import Thread
from typing import Any, Coroutine, Dict, List, Tuple

from io_.aio import AIOTicker, aio_worker, async_echo, async_ticker
from pytest import mark, raises


def test_async_coroutine() -> None:
    """协程的异步调用和等待

    - `async` 表示一个异步方法, 该方法返回一个 `coroutine` 对象, 表示异步调用的存根, 通过 await 关键字调用该存根,
    即可以等待对应的异步方法执行完毕, 并得到异步方法的返回值

        ```python
        async def async_func():
            pass

        c = async_func()
        result = await c
        ```

     - 以协程方式启动的异步方法必须在一个事件循环中列队等待调用,`asyncio.run()` 用于启动一个事件循环, 并执行入口函数
    """

    async def main() -> None:
        """协程入口函数

        通过 `asyncio.run(main())` 方式调用
        """
        # 执行异步函数
        r = await aio_worker(0.1)

        # 判断异步函数的返回值
        assert r == "OK"

    aio.run(main())


def test_async_task() -> None:
    """异步任务

    - 可以通过 `asyncio.create_task(coroutine)` 函数创建异步任务
    - 该函数的参数是一个 `coroutine` 对象, 返回一个 `Task` 对象
    - `Task` 对象有一些额外的属性:
        - `done()` 异步任务是否完成
        - `cancelled()` 异步任务是否被取消
        - `exception()` 异步任务抛出的异常
    """

    async def main() -> None:
        """协程入口函数"""

        # 通过异步函数创建任务对象
        task = aio.create_task(aio_worker(0.1))

        # 此时任务尚未结束和取消
        assert task.done() is False
        assert task.cancelled() is False

        # 等待任务执行完毕
        r = await task

        # 判断任务的返回值
        assert r == "OK"

        # 此时任务已经结束
        assert task.done() is True

    # 执行异步函数
    aio.run(main())


def test_coroutine_wait_timeout() -> None:
    """测试异步协程调用超时

    - 通过 `await coroutine` 表示持续等待, 直到异步函数执行完毕 (或取消, 抛出异常等)
    - 可以为异步调用限定一个执行时长, 超过指定时长仍未执行完毕, 则取消该异步调用
    - `asyncio.wait_for(coroutine, timeout)` 函数接受一个 `coroutine` 对象作为参数,返回另一个 `coroutine` 对象
    - 如果异步调用超过指定时间, 则调用会抛出 `asyncio.TimeoutError` 异常并中断此次异步调用
    """

    async def main() -> None:
        """协程入口函数"""

        # 设定协程执行 100 毫秒, 启动协程函数并等待 200 毫秒
        r = await aio.wait_for(aio_worker(0.1), timeout=0.2)
        # 此时等待成功, 协程执行完毕
        assert r == "OK"

        # 等待失败, 抛出超时异常
        with raises(aio.TimeoutError):
            # 设定协程执行 300 毫秒, 启动协程函数并等待 200 毫秒
            await aio.wait_for(aio_worker(0.3), timeout=0.2)

    aio.run(main())


def test_task_wait_timeout() -> None:
    """测试异步任务调用超时

    - 通过 `asyncio.create_task(coroutine)` 包装一个 `coroutine` 对象
    - 通过 `asyncio.wait_for(task, timeout)` 函数对任务设定超时时长, 得到一个 `coroutine` 对象

    > 注意: 一个任务即便超时, 访问任务的 `done()` 函数也会返回 `True`, 表示任务已完成. 即超时的任务仍属于已完成任务, 而不是已取消任务
    """

    async def main() -> None:
        """
        协程入口函数
        """
        # 设定任务执行 1 秒, 执行任务并等待 2 秒
        task = aio.create_task(aio_worker(0.1))
        r = await aio.wait_for(task, timeout=2)
        # 此时等待成功, 协程执行完毕
        assert r == "OK"

        task = aio.create_task(aio_worker(0.3))

        # 等待失败, 抛出超时异常
        with raises(aio.TimeoutError):
            # 设定任务执行 3 秒, 启动任务并等待 2 秒
            await aio.wait_for(task, timeout=0.2)

    aio.run(main())


def test_coroutine_cancel() -> None:
    """取消异步协程调用

    - 可以通过 `asyncio.shield` 方法包装一个 `coroutine` 对象, 并返回一个 `Future` 对象
    - `Future` 对象具备 `cancel` 方法, 可以在异步调用发生前取消此次调用
    - 调用一个被取消的异步调用将抛出 `asyncio.CancelledError` 异常
    """

    async def main() -> None:
        """
        协程入口函数
        """
        # 包装异步函数为 Future 对象
        future = aio.shield(aio_worker(0.1))
        # 取消异步调用
        future.cancel()

        # 抛出异常, 协程已被取消
        with raises(aio.CancelledError):
            # 在已取消的 Future 对象上进行等待
            await future

        assert future.done() is True
        assert future.cancelled() is True

    aio.run(main())


def test_task_cancel() -> None:
    """取消异步任务调用

    - 可以通过 `asyncio.create_task` 方法包装一个 `coroutine` 对象, 并返回一个 `Task` 对象
    - `Task` 对象具备 `cancel` 方法, 可以在异步调用发生前取消此次调用
    - 调用一个被取消的异步调用将抛出 `asyncio.CancelledError` 异常
    """

    async def main() -> None:
        """协程入口函数"""

        # 包装异步函数为 Task 对象
        task = aio.create_task(aio_worker(0.1))
        # 取消异步调用
        task.cancel()

        # 抛出异常, 任务已被取消
        with raises(aio.CancelledError):
            # 在已取消的 Task 对象上进行等待
            await task

        assert task.done() is True
        assert task.cancelled() is True

    aio.run(main())


def test_coroutine_exception() -> None:
    """异步调用异常

    - 在异步调用的过程中如果抛出异常, 则异步调用中断, 异常从调用方抛出
    """

    async def main() -> None:
        """协程入口函数"""

        # 判断确实抛出了指定异常
        with raises(IOError):
            # 等待一个会抛出异常的协程执行
            await aio_worker(exception=IOError)

        # 产生一个 Future 对象, 包装一个会抛出异常的协程执行
        future = aio.shield(aio_worker(exception=IOError))

        with raises(IOError):
            # 等待执行
            await future

        # 判断协程执行完毕
        assert future.done() is True
        # 判断协程确实抛出了指定异常
        assert isinstance(future.exception(), IOError)

    aio.run(main())


def test_task_exception() -> None:
    """异步任务异常

    - 在异步任务执行过程中如果抛出异常, 则任务被中断, 调用方捕获异常
    """

    async def main() -> None:
        """协程入口函数"""

        # 产生一个 Task 对象, 包装一个会抛出异常的协程执行
        task = aio.create_task(aio_worker(0.1, exception=IOError))

        with raises(Exception):
            # 等待执行
            await task

        # 判断协程执行完毕
        assert task.done() is True
        # 判断协程确实抛出了指定异常
        assert isinstance(task.exception(), IOError)

    aio.run(main())


def test_multiple_coroutines() -> None:
    """批量异步调用

    - 可以通过 `asyncio.gather(...coroutines)` 函数一次性批量执行多个异步调用, 得到一个 `_GatheringFuture` 对象, 表示该组调用的存根
    - 当多个异步调用同时进行时, `IO` 操作将会并发执行, 耗费的总时间是这些调用中 `IO` 耗时最长的那个时间
    - 另外 `asyncio.gather(...coroutines)` 函数也可用于一组 `Task` 的同时调用
    """

    async def main() -> None:
        """协程入口函数"""

        # 组织若干异步协程调用
        futures = aio.gather(
            aio_worker(0.1, id_=3),
            aio_worker(0.2, id_=2),
            aio_worker(0.3, id_=1),
        )

        # 记录开始调用时间
        start = timeit.default_timer()

        # 等待该组协程调用完毕
        rs = await futures

        # 查看整组协程返回的结果
        assert rs == [
            "OK By Task-3",
            "OK By Task-2",
            "OK By Task-1",
        ]
        # 整组协程执行时间为 300 毫秒以上, 即组内最长协程执行时间的协程
        assert timeit.default_timer() - start >= 0.3

    aio.run(main())


def test_multiple_tasks() -> None:
    """批量执行异步任务

    - `Task` 对象也可以通过 `asyncio.gather(...coroutines)` 进行批量调用
    """

    async def main() -> None:
        """协程入口函数"""

        # 组织若干异步协程任务调用
        tasks = aio.gather(
            aio.create_task(aio_worker(0.1, id_=3)),
            aio.create_task(aio_worker(0.2, id_=2)),
            aio.create_task(aio_worker(0.3, id_=1)),
        )

        # 记录开始调用时间
        start = timeit.default_timer()

        # 等待该组协程任务调用完毕
        rs = await tasks

        # 查看整组协程任务返回的结果
        assert rs == [
            "OK By Task-3",
            "OK By Task-2",
            "OK By Task-1",
        ]
        # 整组协程执行时间为 300 毫秒以上, 即组内最长协程任务执行时间的协程
        assert timeit.default_timer() - start >= 0.3

    aio.run(main())


def test_async_callback() -> None:
    """异步回调

    - 当一个异步调用 (或任务) 结束后, 可以回调指定的函数, 通知调用方并传递执行结果
    - 对于异步调用, 回调是通过 `Future` 对象完成的

        ```python
        future = asyncio.ensure_future(coroutine)
        ```

     - 对于异步任务, `Task` 对象本身就具备设置回调的能力
     - 通过回调手段, 可以无需 `await` 操作, 防止对调用方的阻塞
    """

    # 保存回调结果的列表
    # 列表每一项保存: (任务名称, 任务执行结果, 执行任务的事件循环对象)
    callbacks: List[Tuple[str, str, aio.AbstractEventLoop]] = []

    def callback(task: aio.Task) -> None:
        """异步任务结束后回调的函数

        Args:
            - `task` (`asyncio.Task`): 执行协程的异步任务对象
        """
        # 将任务名称, 协程执行结果以及协程所在的事件循环对象存入列表中
        callbacks.append((task.get_name(), task.result(), task.get_loop()))

    async def main() -> None:
        """协程入口函数"""

        # 对 Coroutine 执行后进行回调

        # 将协程对象包装为 Future 对象
        future = aio.ensure_future(aio_worker(0.1, id_=1))
        # 设置任务名称
        future.set_name("Task-1")
        # 设置结束后的回调函数
        future.add_done_callback(callback)

        # 等待协程执行完毕
        await future

        # 验证回调函数确实被执行
        assert callbacks[0][0] == "Task-1"
        assert callbacks[0][1] == "OK By Task-1"
        assert callbacks[0][2] == aio.get_running_loop()

        # 对 Task 执行后进行回调

        # 将协程对象包装为 Task 对象
        task = aio.create_task(aio_worker(0.1, id_=2))
        # 设置任务名称
        task.set_name("Task-2")
        # 设置结束后的回调函数
        task.add_done_callback(callback)

        # 等待协程执行完毕
        await task

        # 验证回调函数确实被执行
        assert callbacks[1][0] == "Task-2"
        assert callbacks[1][1] == "OK By Task-2"
        assert callbacks[1][2] == aio.get_running_loop()

    aio.run(main())


def test_event_loop() -> None:
    """事件循环

    - 更底层的协程操作可以直接通过 Event loop 即事件循环来完成
    - 可以在任意线程创建一个线程相关的事件循环:

        ```python
        event_loop = asyncio.new_event_loop()
        ```

    - 可以获取当前事件循环对象

        ```python
        event_loop = asyncio.get_event_loop()
        ```

    - 可以将一个 `coroutines` 对象提交到指定的事件队列中, 并得到一个 `Future` 对象
    - 可以为 `Future` 对象绑定回调函数, 在异步调用结束后获取通知, 通知中包含异步调用的结果
    - 可以对 `Future` 对象进行 `await` 操作, 等待异步调用完成, 返回结果
    """

    # 保存回调结果的列表
    # 列表每一项保存: (任务名称, 任务执行结果, 执行任务的事件循环对象)
    callbacks: List[Tuple[str, str, aio.AbstractEventLoop]] = []

    def callback(task: aio.Task) -> None:
        """异步任务结束后回调的函数

        Args:
            - `task` (`asyncio.Task`): 执行协程的异步任务对象
        """
        # 将任务名称, 协程执行结果以及协程所在的事件循环对象存入列表中
        callbacks.append((task.get_name(), task.result(), task.get_loop()))

    # 创建一个新的事件循环对象
    loop = aio.new_event_loop()

    async def main() -> None:
        """协程入口函数"""

        # 获取当前协程所在的事件循环
        assert loop == aio.get_running_loop()

        # 启动协程
        future = aio.ensure_future(aio_worker(0.1))
        # 为协程任务设置名称
        future.set_name("Task-1")
        # 为协程结束设置回调函数
        future.add_done_callback(callback)

        # 等待协程执行完毕
        await future

        # 确认回调函数确实执行
        assert callbacks[0][0] == "Task-1"
        assert callbacks[0][1] == "OK"
        assert callbacks[0][2] == loop  # 协程执行的事件循环既是创建的事件循环

    loop.run_until_complete(main())


def test_event_loop_on_other_thread() -> None:
    """
    在另一个线程中创建事件循环

    - 事件循环总是和一个线程相关, 所以可以在任意线程上创建事件循环
    - 如果一个线程没有绑定正在运行的事件循环, 则可以为该线程创建一个新的事件循环

    ```python
    event_loop = asyncio.new_event_loop()
    ```

    - 可以为事件循环载入一个 `coroutines` 对象作为主函数, 并在主函数结束后结束事件循环

    ```python
    event_loop.run_until_complete(coroutines)
    ```
    """

    # 创建一个新的事件循环对象
    loop = aio.new_event_loop()

    async def main() -> None:
        """协程入口函数"""

        # 确认当前协程所在的事件循环为新建的事件循环对象
        assert loop == aio.get_event_loop()

        # 执行协程函数, 确认返回值
        assert await aio_worker(0.1) == "OK"

    def thread_run() -> None:
        """线程入口函数

        在该函数内创建事件循环并异步执行 `main` 协程函数
        """
        # 在新建的协程对象上异步执行函数
        loop.run_until_complete(main())

    # 创建线程对象
    thread = Thread(target=thread_run)
    # 启动线程
    thread.start()
    # 等待线程函数执行结束
    thread.join()


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

    def is_finished() -> None:
        """判断程序是否可以结束"""

        # 判断字典是否包含了 5 项内容
        while len(called_tasks) < 5:
            # 数量不足, 当前协程等待 100 毫秒后返回 False
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

    loop = aio.get_event_loop()
    loop.run_until_complete(main(loop))
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


def test_async_event() -> None:
    """协程事件对象 `Event`

    - 协程事件对象用于在一个协程函数调用中通知持有相同事件对象的另一些协程, 让其可继续运行
    - 事件对象有两个状态
        - `set`: 已通知状态，此时所有在事件对象上的等待 (`wait` 操作) 将结束, 操作得以继续执行
        - `unset`: 未通知状态，此时所有在事件对象上的等待 (`wait` 操作) 将继续
    - `is_set`: 事件是否已通知
    """
    # 协程事件对象
    event = aio.Event()

    # 生成开始时间
    start_time = timeit.default_timer()

    async def event_job(id_: int) -> Dict[str, Any]:
        """测试协程事件对象

        Args:
            - `id_` (`int`): ID 标识符

        Returns:
            `Dict[str, Any]`: 返回 ID 标识符和执行时间组成的字典
        """
        # 等待事件通知
        await event.wait()

        return {
            "id": id_,  # ID 值
            "finish_time": round(timeit.default_timer() - start_time, 1),  # 执行时间
        }

    async def main() -> None:
        """
        协程入口函数
        """
        # 同时启动两个协程函数
        group = aio.gather(event_job(1), event_job(2))

        # 延迟 200 毫秒后
        await aio.sleep(0.2)
        # 发起事件通知
        event.set()

        # 等待所有协程结束
        r = await group

        # 第一个结果为 ID=1 函数返回
        assert r[0]["id"] == 1
        assert r[0]["finish_time"] == 0.2  # 整体执行 200 毫秒

        # 第二个结果为 ID=2 函数返回
        assert r[1]["id"] == 2
        assert r[1]["finish_time"] == 0.2  # 整体执行 200 毫秒

    aio.run(main())


def test_condition_lock() -> None:
    """
    带状态的协程锁

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
    cond = asyncio.Condition()

    # 生成开始时间
    start_time = timeit.default_timer()

    async def cond_job(id_: int) -> Dict[str, Any]:
        """
        测试带状态的协程锁对象

        Args:
            id_ (int): ID 标识符

        Returns:
            Dict[str, Any]: 返回 ID 标识符和执行时间组成的字典
        """
        # 进入锁
        async with cond:
            # 等待锁通知
            await cond.wait()

        return {
            "id": id_,  # ID 值
            "finish_time": int(timeit.default_timer() - start_time),  # 执行时间
        }

    async def main() -> None:
        group = asyncio.gather(
            cond_job(1),
            cond_job(2),
            cond_job(3),
        )

        # 等待 1 秒后
        await asyncio.sleep(2)

        # 通知 2 个锁
        async with cond:
            cond.notify(2)

        # 再等待 2 秒后
        await asyncio.sleep(2)

        # 通知所有锁
        async with cond:
            cond.notify_all()

        # 等待所有协程结束
        r = await group

        # 第一个结果为 ID=1 函数返回, 为第一次通知解锁
        assert r[0]["id"] == 1
        assert r[0]["finish_time"] == 2  # 整体执行 2 秒

        # 第二个结果为 ID=2 函数返回, 为第一次通知解锁
        assert r[1]["id"] == 2
        assert r[1]["finish_time"] == 2  # 整体执行 2 秒

        # 第三个结果为 ID=3 函数返回, 为第二次通知解锁
        assert r[2]["id"] == 3
        assert r[2]["finish_time"] == 4  # 整体执行 4 秒

    asyncio.run(main())


def test_semaphore() -> None:
    """
    信号量

    - 信号量可以指定一个数量, 表示多少个信号可以使用, 每个协程可以占用一个信号并在稍后释放它,
    当所有的信号被占用后，后续的协程会进入等待, 直到之后有一个信号被释放
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
    sem = asyncio.Semaphore(2)

    # 生成开始时间
    start_time = timeit.default_timer()

    async def sem_job(id_: int) -> Dict[str, Any]:
        """
        测试信号量对象

        Args:
            id_ (int): ID 标识符

        Returns:
            Dict[str, Any]: 返回 ID 标识符和执行时间组成的字典
        """
        # 进入信号量
        async with sem:
            # 协程等待 2 秒钟后退出信号量
            await asyncio.sleep(2)

        return {
            "id": id_,  # ID 值
            "finish_time": int(timeit.default_timer() - start_time),  # 执行时间
        }

    async def main() -> None:
        r = await asyncio.gather(
            sem_job(1),
            sem_job(2),
            sem_job(3),
        )

        # 第一个结果为 ID=1 函数返回, 对应前两个信号
        assert r[0]["id"] == 1
        assert r[0]["finish_time"] == 2  # 整体执行 2 秒

        # 第二个结果为 ID=2 函数返回, 对应前两个信号
        assert r[1]["id"] == 2
        assert r[1]["finish_time"] == 2  # 整体执行 4 秒

        # 第三个结果为 ID=3 函数返回, 对应后两个信号
        assert r[2]["id"] == 3
        assert r[2]["finish_time"] == 4  # 整体执行 2 秒

    asyncio.run(main())


def test_queue() -> None:
    """
    协程队列

    - 协程队列用于在协程中同步的 put 和 get 资源
    """
    # 定义队列对象, 最多可放置 5 个元素
    queue: asyncio.Queue = asyncio.Queue(5)

    async def queue_job() -> List[Coroutine]:
        """
        测试协程队列
        """
        rs = []
        # 循环直到队列被取空
        while queue.qsize():
            # 协程休眠 1 秒
            await asyncio.sleep(1)

            # 从队列中获取资源, 阻塞模式
            rs.append(await queue.get())
            # 通知队列任务完成
            # 在消费者一侧, 每次处理完一个元素, 都需要调用一次 task_done 函数, 表示处理完毕
            # 此时若另一个协程在队列上执行 join 等待, 则可以结束等待
            queue.task_done()

        return rs

    async def main() -> None:
        """
        协程入口函数
        """
        # 向队列中放入第一个元素
        # put 函数会在队列已满的时候阻塞, 直到成功存入该元素
        await queue.put(100)

        # 启动协程
        future = asyncio.ensure_future(queue_job())

        # 向队列中存入第二个元素
        await queue.put(200)
        # 向队列中存入元素且不等待, 所以无需 await
        # 如果队列已满, 则抛出异常
        queue.put_nowait(300)

        # 等待队列的当前元素处理完毕
        # 即队列的 task_done 函数执行完毕
        await queue.join()

        # 等待协程执行完毕, 确认队列内容
        assert await future == [100, 200, 300]

    asyncio.run(main())


@mark.asyncio
async def test_aio_iterator() -> None:
    """
    测试 `AIOTicker` 类型, 该类型是一个协程异步迭代器对象, 可以进行异步迭代操作

    `@mark.asyncio` 使用了 `pytest-asyncio` 插件, 可以以协程异步方式执行测试而无需编码

    参考 `conftest.py` 的 `event_loop` 函数, 提供了一个 `fixture` 用于管理协程事件队列的生命周期
    """
    # 实例化异步迭代器对象
    # 每次迭代间隔 1 秒, 最大迭代值为 5
    ticker = AIOTicker(1, 5)

    # 记录整个迭代的时间
    start = timeit.default_timer()

    # 确认第一次迭代值
    assert await ticker.__anext__() == 0
    # 确认第二次迭代值
    assert await ticker.__anext__() == 1

    vals = []
    # 通过 async for 进行异步迭代
    async for t in ticker:
        vals.append(t)

    # 判断迭代结果
    assert vals == [2, 3, 4]
    # 确认所有迭代执行的总时间
    assert 5 <= timeit.default_timer() - start <= 5.1


@mark.asyncio
async def test_aio_generator() -> None:
    """测试 `ticker` 函数

    该函数返回一个生成器 (`AsyncGenerator`) 对象, 可以作为迭代器对象使用
    """
    # 返回生成器对象
    gen = async_ticker(0.1, 5)

    # 记录整个迭代的时间
    start = timeit.default_timer()

    # 确认生成器对象第一次迭代对象
    assert await gen.__anext__() == 0
    # 确认生成器对象第二次迭代对象
    assert await gen.__anext__() == 1

    vals = []
    # 通过 async for 进行异步迭代
    async for t in gen:
        vals.append(t)

    # 判断迭代结果
    assert vals == [2, 3, 4]
    # 确认所有迭代执行的总时间
    assert 5 <= timeit.default_timer() - start <= 5.1


@mark.asyncio
async def test_async_echo() -> None:
    # 调用函数, 返回生成器对象
    g = async_echo(0.1, 5)

    # 第一个值为 0, 对应 yield 0 语句
    assert await g.__anext__() == 0

    # 设置一个值, 对应 v = yield 0, 接收一个输入, 此时 v 的值为 10
    await g.asend(10)
    # 获取下一个值为 100, 对应 v *= 10; yield v 两条语句
    assert await g.__anext__() == 100

    # 处理下一个循环
    await g.asend(20)
    assert await g.__anext__() == 200

    # 发送 0 值, 导致迭代结束
    with raises(StopAsyncIteration):
        await g.asend(0)
