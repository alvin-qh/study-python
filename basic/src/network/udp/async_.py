import asyncio as aio
from typing import Optional, Tuple, cast


class ServerProtocol(aio.DatagramProtocol):
    def connection_made(self, transport: aio.BaseTransport) -> None:
        self.transport = cast(aio.DatagramTransport, transport)

    def datagram_received(self, data: bytes, addr: Tuple[str | None, int]) -> None:
        message = data.decode() + "-ack"
        print(f"Received {message} from {addr}")
        self.transport.sendto(data + b"-ack", addr)


class AsyncServer:
    def __init__(self, loop: Optional[aio.AbstractEventLoop] = None) -> None:
        if loop is not None:
            self._loop = loop
        else:
            self._loop = aio.get_running_loop()

        self._transport: Optional[aio.DatagramTransport] = None
        self._exit_cond = aio.Condition()

    async def bind(self, port: int, host: str = "0.0.0.0") -> None:
        transport, _ = await self._loop.create_datagram_endpoint(
            lambda: ServerProtocol(),
            local_addr=(host, port),
        )
        self._transport = transport

    def close(self) -> None:
        if self._transport:
            self._transport.close()
            self._transport = None

    async def wait(self) -> None:
        async with self._exit_cond:
            await self._exit_cond.wait()


class ClientProtocol(aio.BaseProtocol):
    def __init__(self, message: str, on_con_lost: aio.Future[bool]) -> None:
        self._message = message
        self._on_con_lost = on_con_lost
        self._transport: Optional[aio.DatagramTransport] = None

    def connection_made(self, transport: aio.BaseTransport) -> None:
        self._transport = cast(aio.DatagramTransport, transport)
        self._transport.sendto(self._message.encode())
        print("Data sent: {!r}".format(self._message))

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        print("Received:", data.decode())

        print("Close the socket")
        if self._transport:
            self._transport.close()

    def connection_lost(self, exc: Optional[Exception] = None) -> None:
        print("The server closed the connection")
        self._on_con_lost.set_result(True)


class AsyncClient:
    def __init__(self, loop: Optional[aio.AbstractEventLoop] = None) -> None:
        if loop is not None:
            self._loop = loop
        else:
            self._loop = aio.get_running_loop()

        self._transport: Optional[aio.DatagramTransport] = None

    async def connect(self, host: str, port: int, message: str) -> None:
        on_con_lost = self._loop.create_future()

        transport, _ = await self._loop.create_datagram_endpoint(
            lambda: ClientProtocol(message, on_con_lost),
            remote_addr=(host, port),
        )
        self._transport = transport

    def close(self) -> None:
        if self._transport:
            self._transport.close()
            self._transport = None
