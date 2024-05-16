import asyncio as aio
from typing import Optional, Type


async def async_worker(
    wait_time: float = 1.0,
    exception: Optional[Type[Exception]] = None,
    id_: Optional[int] = None,
) -> str:
    """异步协程入口函数

    Args:
        - `wait_time` (`float`, optional): 等待时间. Defaults to `1.0`.
        - `raises` (`Type[Exception]`, optional): 要抛出的异常, None 表示不抛出. Defaults to `None`.
        - `id_` (`int`, optional): 任务 ID. Defaults to `None`.

    Returns:
        `str`: 返回结果字符串
    """
    if exception:
        # 如果 raises 不为 None, 则抛出异常
        raise exception
    else:
        # 异步等待
        await aio.sleep(wait_time)

    if id_ is None:
        return "OK"

    return f"OK By Task-{id_}"
