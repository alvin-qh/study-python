import asyncio as aio
from typing import Optional, Tuple, cast


class UDPProtocol(aio.DatagramProtocol):
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

    async def bind(self, port: int, addr: str = "") -> None:
        transport, _ = await self._loop.create_datagram_endpoint(
            lambda: UDPProtocol(), local_addr=(addr, port)
        )
        self._transport = transport

    def close(self) -> None:
        if self._transport:
            self._transport.close()
            self._transport = None

    async def wait(self) -> None:
        async with self._exit_cond:
            await self._exit_cond.wait()
