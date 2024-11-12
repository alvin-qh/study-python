from queue import Queue
import threading as th
import time
import pytest
from network import udp


def test_sync_udp() -> None:
    """测试同步 UDP 服务端客户端"""

    # 通知服务端线程退出的条件量
    exit_cond = th.Condition()

    # 实例化服务端对象
    srv = udp.SyncServer()

    # 服务端对象绑定本地端口
    srv.bind(8899)

    def server_side() -> None:
        """服务端线程入口函数"""
        try:
            # 接收数据, 返回数据长度, 客户端地址和数据内容
            n, addr, data = srv.recv()
            assert data[:n] == b"hello"

            srv.sendto(b"hello_ack", addr)
        finally:
            # 通知主线程退出
            with exit_cond:
                exit_cond.notify()

            if "srv" in locals():
                srv.close()

    # 启动服务端
    th.Thread(target=server_side).start()

    client = udp.SyncClient()

    def client_side() -> None:
        """客户端线程入口函数"""
        try:
            # 发送数据到服务端
            while client.sendto(b"hello", ("127.0.0.1", 8899)) == 0:
                # 如果发送失败, 则等待一段时间后重试
                time.sleep(0.1)

            # 从服务端接收数据
            n, addr, data = client.recv()
            assert data[:n] == b"hello_ack"
        finally:
            if client:
                client.close()

    # 启动客户端线程
    th.Thread(target=client_side).start()

    # 等待服务端结束
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
        await srv.bind(8899)

        # 实例化客户端对象
        client = udp.AsyncClient()

        # 客户端连接到服务端
        await client.connect("127.0.0.1", 8899, "hello", res_que)

        # 等待服务端关闭
        await srv.wait()

        assert res_que.get() == "hello_ack"
    finally:
        if "client" in locals():
            client.close()

        if "srv" in locals():
            srv.close()
