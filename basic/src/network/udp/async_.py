import asyncio as aio
import logging
from queue import Queue
import socket as so
from typing import Optional, Tuple, cast

from ..common import format_addr

log = logging.getLogger()


class ServerProtocol(aio.DatagramProtocol):
    """服务端协议类"""

    def __init__(self, on_con_lost: aio.Future[bool]) -> None:
        """初始化服务端协议类

        Args:
            `on_con_lost` (`aio.Future[bool]`): 当连接关闭时, 通知服务端结束的异步量
        """
        self._on_con_lost = on_con_lost

    def connection_made(self, transport: aio.BaseTransport) -> None:
        """当连接创建后回调

        Args:
            `transport` (`aio.BaseTransport`): 数据传输对象, 本例中应为 `aio.DatagramTransport` 类型对象
        """
        self._transport = cast(aio.DatagramTransport, transport)
        log.info("[SERVER] UDP server bound")

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        """当数据接收完毕后回调

        Args:
            `data` (`bytes`): 接收到的数据
            `addr` (`Tuple[str, int]`): 客户端地址
        """
        # 将接收到的数据增加后缀后发送回客户端
        msg = data.decode()
        log.info(f"[SERVER] Data {msg!r} received from {format_addr(addr)!r}")

        msg = f"{msg}_ack"
        self._transport.sendto(msg.encode(), addr)
        log.info(f"[SERVER] Data {msg!r} send to {format_addr(addr)!r}")

        # 发送完毕后, 关闭服务端
        self._transport.abort()

    def connection_lost(self, exc: Optional[Exception] = None) -> None:
        """当链接关闭时回调

        Args:
            `exc` (`Optional[Exception]`, optional): 导致连接关闭的异常. Defaults to `None`.
        """
        self._on_con_lost.set_result(True)
        log.info("[SERVER] Connection closed")


class AsyncServer:
    """异步 UDP 服务端类"""

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

        self._transport: Optional[aio.DatagramTransport] = None

        # 创建连接关闭后的异步通知量
        self._on_con_lost = self._loop.create_future()

    async def bind(self, port: int, host: str = "0.0.0.0") -> None:
        """将服务端和一个端口号绑定

        Args:
            `port` (`int`): 端口号
            `host` (`str`, optional): 绑定地址. Defaults to "0.0.0.0".
        """
        # 事件循环对象的 `create_datagram_endpoint` 方法用于创建一个基于 UDP 协议的服务端网络节点
        # 所有网络事件 (客户端连接, 数据接收完毕), 都会通过 `ServerProtocol` 类对象的对应方法进行处理
        transport, _ = await self._loop.create_datagram_endpoint(
            lambda: ServerProtocol(self._on_con_lost),
            local_addr=(host, port),
        )
        self._transport = transport

    def close(self) -> None:
        """关闭服务端连接"""
        if self._transport:
            self._transport.close()
            self._transport = None

    async def wait(self) -> None:
        """等待服务端结束"""
        await self._on_con_lost


class ClientProtocol(aio.BaseProtocol):
    """UDP 客户端协议类"""

    def __init__(
        self,
        addr: Tuple[str, int],
        res_que: Queue[str],
        on_con_lost: aio.Future[bool],
    ) -> None:
        """初始化客户端协议对象

        Args:
            `addr` (`addr`): 服务端地址
            `res_que` (`Queue[str]`): 服务端返回的消息队列
            `on_con_lost` (`aio.Future[bool]`): 当连接关闭时, 通知服务端结束的异步量
        """
        self._addr = addr
        self._res_que = res_que
        self._on_con_lost = on_con_lost
        self._transport: Optional[aio.DatagramTransport] = None

    def connection_made(self, transport: aio.BaseTransport) -> None:
        """当连接到服务端后回调

        Args:
            `transport` (`aio.BaseTransport`): 数据传输对象, 本例中应为 `aio.DatagramTransport` 类型对象
        """
        self._transport = cast(aio.DatagramTransport, transport)

        # 本例中, 连接服务端时省略了 `remote_addr` 参数, 故在此发送数据时, 需要指定服务端地址
        data = b"hello"
        self._transport.sendto(data, self._addr)
        log.info(f"[CLIENT] Data {data!r} send to {format_addr(self._addr)!r}")

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        """当从服务器接收到消息后回调

        Args:
            `data` (`bytes`): 接收到的消息
            `addr` (`Tuple[str, int]`): 服务端地址
        """
        msg = data.decode()
        log.info(f"[CLIENT] Data {msg!r} receive from: {format_addr(addr)!r}")

        self._res_que.put(msg)
        if self._transport:
            self._transport.close()

    def connection_lost(self, exc: Optional[Exception] = None) -> None:
        """当客户端连接被关闭后回调

        Args:
            `exc` (`Optional[Exception]`, optional): 导致客户端连接关闭的异常. Defaults to `None`.
        """
        self._on_con_lost.set_result(True)
        log.info("[CLIENT] Connection closed")


class AsyncClient:
    """异步 UDP 客户端类"""

    def __init__(self, loop: Optional[aio.AbstractEventLoop] = None) -> None:
        """初始化异步 UDP 客户端对象实例

        Args:
            `loop` (`Optional[aio.AbstractEventLoop]`, optional): 异步事件循环对象. Defaults to `None`.
        """
        if loop is not None:
            self._loop = loop
        else:
            # 如果参数未传递事件循环对象, 则获取当前协程的事件循环对象
            self._loop = aio.get_running_loop()

        self._transport: Optional[aio.DatagramTransport] = None

    async def connect(
        self, host: str, port: int, msg: str, res_que: Queue[str]
    ) -> None:
        """连接到服务端

        Args:
            `host` (`str`): 服务端地址
            `port` (`int`): 服务端端口号
            `msg` (`str`): 发送给服务端的第一条消息
            `res_que` (`Queue[str]`): 保存服务端返回消息的队列
        """
        on_con_lost = self._loop.create_future()

        # 事件循环对象的 `create_datagram_endpoint` 方法用于创建一个基于 UDP 协议的客户端网络节点
        # 所有网络事件 (网络连接, 数据接收完毕), 都会通过 `ClientProtocol` 类对象的对应方法进行处理
        #
        # `remote_addr` 参数表示服务端地址
        # 如果 `remote_addr` 参数被省略, 则表示客户端可以向任意服务端发送数据, 此时 `family` 参数必须为 `so.SOCK_DGRAM`, 且
        # 发送时必须指定目标地址
        # 反之, 可以省略 `family` 参数, 且发送时无需指定目标地址
        transport, _ = await self._loop.create_datagram_endpoint(
            lambda: ClientProtocol((host, port), res_que, on_con_lost),
            family=so.SOCK_DGRAM,
            proto=so.IPPROTO_UDP,
            # remote_addr=(host, port),
        )
        self._transport = transport

    def close(self) -> None:
        """关闭连接"""
        if self._transport:
            self._transport.close()
            self._transport = None
