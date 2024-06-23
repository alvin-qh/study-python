import asyncio as aio
import logging
from queue import Queue
import socket as so
from typing import Callable, Optional, Tuple, cast

from ..common import format_addr

log = logging.getLogger()


class ServerProtocol(aio.Protocol):
    """服务端协议类"""

    _transport: aio.Transport

    def __init__(self) -> None:
        """初始化服务端协议类"""
        # 用于保存客户端连接地址
        self._addr: Tuple[str, int] = ("", 0)

    def connection_made(self, transport: aio.BaseTransport) -> None:
        """当连接创建后回调

        Args:
            `transport` (`aio.BaseTransport`): 数据传输对象, 本例中应为 `aio.Transport` 类型对象
        """
        self._transport = cast(aio.Transport, transport)
        self._addr = transport.get_extra_info("peername")
        log.info(f"[SERVER] TCP server bound, listening at {format_addr(self._addr)}")

    def data_received(self, data: bytes) -> None:
        """当数据接收完毕后回调

        Args:
            `data` (`bytes`): 接收到的数据
        """
        # 将接收到的数据解码
        msg = data.decode()
        log.info(f"[SERVER] Data {msg!r} received from {format_addr(self._addr)!r}")

        # 生成发送到客户端的数据
        msg = f"{msg}_ack"
        # 将数据发送到客户端
        self._transport.write(msg.encode())
        log.info(f"[SERVER] Data {msg!r} send to {format_addr(self._addr)!r}")

        # 发送完毕后, 关闭服务端
        self._transport.abort()

    def connection_lost(self, exc: Optional[Exception] = None) -> None:
        """当链接关闭时回调

        Args:
            `exc` (`Optional[Exception]`, optional): 导致连接关闭的异常. Defaults to `None`.
        """
        log.info("[SERVER] Connection closed")


class AsyncServer:
    """异步 TCP 服务端类"""

    def __init__(self, loop: Optional[aio.AbstractEventLoop] = None) -> None:
        """初始化服务端对象

        Args:
            `loop` (`Optional[aio.AbstractEventLoop]`, optional): 异步事件循环对象. Defaults to `None`.
        """
        if loop is not None:
            self._loop = loop
        else:
            # 如果参数未传递事件循环对象, 则获取当前协程的事件循环对象
            self._loop = aio.get_running_loop()

        # 用于保存异步服务器对象
        self._server: Optional[aio.Server] = None

    async def bind(self, port: int, host: str = "0.0.0.0") -> None:
        """将服务端和一个端口号绑定

        Args:
            `port` (`int`): 端口号
            `host` (`str`, optional): 绑定地址. Defaults to "0.0.0.0".
        """
        # 事件循环对象的 `create_server` 方法用于创建一个基于 TCP 协议的服务端网络节点
        # 所有网络事件 (客户端连接, 数据接收完毕), 都会通过 `ServerProtocol` 类对象的对应方法进行处理
        self._server = await self._loop.create_server(
            lambda: ServerProtocol(),
            host=host,
            port=port,
            family=so.AF_INET,
        )

    def close(self) -> None:
        """关闭服务端连接"""
        if self._server:
            self._server.close()
            self._server = None

    async def wait(self) -> None:
        """等待服务端结束"""
        if self._server:
            try:
                await self._server.serve_forever()
            except aio.CancelledError:
                pass


# 定义回调函数类型, 用于在客户端接受完最后一条消息后回调, 以通知工作全部完成
StopFn = Callable[[], None]


class ClientProtocol(aio.BaseProtocol):
    """TCP 客户端协议类"""

    def __init__(self, res_que: Queue[str], stop_fn: StopFn) -> None:
        """初始化客户端协议对象

        Args:
            `res_que` (`Queue[str]`): 服务端返回的消息队列
        """
        self._addr: Tuple[str, int] = ("", 0)
        self._res_que = res_que
        self._transport: Optional[aio.Transport] = None
        self._stop_fn = stop_fn

    def connection_made(self, transport: aio.BaseTransport) -> None:
        """当连接到服务端后回调

        Args:
            `transport` (`aio.BaseTransport`): 数据传输对象, 本例中应为 `aio.Transport` 类型对象
        """
        self._transport = cast(aio.Transport, transport)
        # 通过属性名 peername 获取本次链接的远程地址
        self._addr = transport.get_extra_info("peername")

        data = b"hello"

        # 向服务端发送数据
        self._transport.write(data)
        log.info(f"[CLIENT] Data {data!r} send to {format_addr(self._addr)!r}")

    def data_received(self, data: bytes) -> None:
        """当从服务器接收到消息后回调

        Args:
            `data` (`bytes`): 接收到的消息
        """
        # 处理从服务端接收的消息
        msg = data.decode()
        log.info(f"[CLIENT] Data {msg!r} receive from: {format_addr(self._addr)!r}")

        # 将消息写入队列
        self._res_que.put(msg)

        # 处理完毕, 关闭本次连接
        if self._transport:
            self._transport.close()

    def connection_lost(self, exc: Optional[Exception] = None) -> None:
        """当客户端连接被关闭后回调

        Args:
            `exc` (`Optional[Exception]`, optional): 导致客户端连接关闭的异常. Defaults to `None`.
        """
        log.info("[CLIENT] Connection closed")

        # 当客户端连接关闭后, 调用回调函数, 通知可以结束任务
        self._stop_fn()


class AsyncClient:
    """异步 TCP 客户端类"""

    def __init__(
        self, stop_fn: StopFn, loop: Optional[aio.AbstractEventLoop] = None
    ) -> None:
        """初始化异步 UDP 客户端对象实例

        Args:
            `stop_fn` (`StopFn`): 当客户端完成工作后回调的函数
            `loop` (`Optional[aio.AbstractEventLoop]`, optional): 异步事件循环对象. Defaults to `None`.
        """
        if loop is not None:
            self._loop = loop
        else:
            # 如果参数未传递事件循环对象, 则获取当前协程的事件循环对象
            self._loop = aio.get_running_loop()

        self._transport: Optional[aio.Transport] = None
        self._stop_fn = stop_fn

    async def connect(self, host: str, port: int, res_que: Queue[str]) -> None:
        """连接到服务端

        Args:
            `host` (`str`): 服务端地址
            `port` (`int`): 服务端端口号
            `res_que` (`Queue[str]`): 保存服务端返回消息的队列
        """
        # 事件循环对象的 `create_connection` 方法用于创建一个基于 TCP 协议客户端连接, 连接到服务端,
        # 所有网络事件 (网络连接, 数据接收完毕), 都会通过 `ClientProtocol` 类对象的对应方法进行处理
        transport, _ = await self._loop.create_connection(
            lambda: ClientProtocol(res_que, self._stop_fn),
            host=host,
            port=port,
            family=so.AF_INET,
        )
        self._transport = transport

    def close(self) -> None:
        """关闭连接"""
        if self._transport:
            self._transport.close()
            self._transport = None
