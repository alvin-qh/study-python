from queue import Queue

import pytest

from basic.network import get_available_port, tcp


def test_sync_tcp() -> None:
    """测试 TCP 以同步方式进行通信"""
    port = get_available_port()

    try:
        # 实例化服务端对象
        srv = tcp.SyncServer()

        # 启动服务端侦听
        srv.listen(port)

        # 实例化客户端对象
        client = tcp.SyncClient()

        # 客户端连接服务端
        client.connect("127.0.0.1", port)

        # 客户端发送数据
        client.send(b"hello")

        # 客户端接收数据
        n, data = client.recv()

        # 确认客户端接收数据正确
        assert n == 9
        assert data[:n] == b"hello_ack"
    except Exception as e:
        pytest.fail(str(e))
    finally:
        if "client" in locals():
            client.close()

        if "srv" in locals():
            srv.close()


def test_stream_tcp() -> None:
    """测试 TCP 以同步流方式进行通信"""
    port = get_available_port()

    try:
        # 实例化服务端对象
        srv = tcp.StreamServer()
        # 启动服务端侦听
        srv.listen(port)

        # 实例化客户端对象
        client = tcp.StreamClient()
        # 客户端连接服务端
        client.connect("127.0.0.1", port)

        # 客户端发送登录请求数据包
        pack = tcp.Package(
            tcp.Header("login"),
            tcp.Body(
                tcp.LoginPayload("alvin", "123456"),
            ),
        )
        client.send(pack)
        # 客户端接收登录响应数据包
        pack = client.recv()
        assert pack.header.cmd == "login"
        assert pack.body.payload.success is True  # type: ignore
        assert pack.body.payload.err == ""  # type: ignore

        # 客户端发送退出请求包
        pack = tcp.Package(
            tcp.Header("bye"),
            tcp.Body(
                tcp.ByePayload(),
            ),
        )
        client.send(pack)
        # 客户端接收退出响应包
        pack = client.recv()
        assert pack.header.cmd == "bye"
        assert pack.body.payload.word == "bye bye"  # type: ignore
    finally:
        if "client" in locals():
            client.close()

        if "srv" in locals():
            srv.close()


@pytest.mark.asyncio
async def test_async_tcp() -> None:
    """测试基于协程的异步 UDP 服务端和和客户端"""
    port = get_available_port()

    # 保存服务端返回消息的队列
    res_que: Queue[str] = Queue()

    try:
        # 实例化服务端对象
        srv = tcp.AsyncServer()

        # 服务端绑定端口号, 开始监听
        await srv.bind(port)

        # 实例化客户端对象
        client = tcp.AsyncClient(lambda: srv.close())

        # 客户端连接到服务端
        await client.connect("127.0.0.1", port, res_que)

        # 等待服务端关闭
        await srv.wait()

        # 确认客户端收到服务端消息
        assert res_que.get() == "hello_ack"
    finally:
        if "client" in locals():
            client.close()

        if "srv" in locals():
            srv.close()
