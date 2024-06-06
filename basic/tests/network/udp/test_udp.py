import pytest
from network import udp


def test_sync_udp() -> None:
    srv = udp.SyncServer()
    srv.bind(18888)
    data = srv.recv()


@pytest.mark.asyncio
async def test_async_udp() -> None:
    srv = udp.AsyncServer()
    await srv.bind(18888)

    client = udp.AsyncClient()
    await client.connect("127.0.0.1", 18888, "hello")

    await srv.wait()
    srv.close()
