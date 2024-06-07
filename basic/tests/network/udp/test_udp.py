from queue import Queue
import threading
import time
import pytest
from network import udp


def test_sync_udp() -> None:
    """测试同步 UDP 服务端客户端"""

    # 通知服务端线程退出的条件量
    exit_cond = threading.Condition()

    # 实例化服务端对象
    srv = udp.SyncServer()

    # 服务端对象绑定本地端口
    srv.bind(18888)

    def server_side() -> None:
        """服务端线程"""
        try:
            # 接收数据, 返回数据长度, 客户端地址和数据内容
            n, addr, data = srv.recv()
            assert data[:n] == b"hello"

            srv.sendto(b"hello_ack", addr)
        finally:
            # 通知主线程退出
            with exit_cond:
                exit_cond.notify()

            srv.close()

    threading.Thread(target=server_side).start()

    client = udp.SyncClient()

    def client_side() -> None:
        while client.sendto(b"hello", ("127.0.0.1", 18888)) == 0:
            time.sleep(0.1)

        n, addr, data = client.recv()
        assert data[:n] == b"hello_ack"

    threading.Thread(target=client_side).start()

    with exit_cond:
        exit_cond.wait()


@pytest.mark.asyncio
async def test_async_udp() -> None:
    """测试基于协程的异步 UDP 服务端和和客户端"""

    # 保存服务端返回消息的队列
    res_que: Queue[str] = Queue()

    try:
        # 实例化服务端对象
        srv = udp.AsyncServer()

        # 服务端绑定端口号, 开始监听
        await srv.bind(18888)

        # 实例化客户端对象
        client = udp.AsyncClient()

        # 客户端连接到服务端
        await client.connect("127.0.0.1", 18888, "hello", res_que)

        # 等待服务端关闭
        await srv.wait()
    finally:
        if client:
            client.close()

        if srv:
            srv.close()

    assert res_que.get() == "hello_ack"
