from network import tcp


def test_sync_tcp() -> None:
    """测试 TCP 以同步方式进行通信"""
    try:
        # 实例化服务端对象
        srv = tcp.SyncServer()
        # 启动服务端侦听
        srv.listen(28888)

        # 实例化客户端对象
        client = tcp.SyncClient()
        # 客户端连接服务端
        client.connect("127.0.0.1", 28888)
        # 客户端发送数据
        client.send(b"hello")
        # 客户端接收数据
        n, data = client.recv()

        # 确认客户端接收数据正确
        assert n == 9
        assert data[:n] == b"hello_ack"
    finally:
        if client:
            client.close()

        if srv:
            srv.close()


def test_stream_tcp() -> None:
    """测试 TCP 以同步流方式进行通信"""
    try:
        # 实例化服务端对象
        srv = tcp.StreamServer()
        # 启动服务端侦听
        srv.listen(28888)

        # 实例化客户端对象
        client = tcp.StreamClient()
        # 客户端连接服务端
        client.connect("127.0.0.1", 28888)

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

        pack = tcp.Package(
            tcp.Header("bye"),
            tcp.Body(
                tcp.ByePayload(),
            ),
        )
        client.send(pack)
        pack = client.recv()
        assert pack.header.cmd == "bye"
        assert pack.body.payload.word == "bye bye"  # type: ignore
    finally:
        if client:
            client.close()

        if srv:
            srv.close()
