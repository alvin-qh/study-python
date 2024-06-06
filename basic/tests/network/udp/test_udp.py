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

    await srv.wait()
    srv.close()
