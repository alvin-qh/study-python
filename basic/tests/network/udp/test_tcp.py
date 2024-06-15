from network import tcp


def test_sync_tcp() -> None:
    try:
        srv = tcp.SyncServer()
        srv.bind(28888)
        srv.start_accept()

        client = tcp.SyncClient()
        client.connect("127.0.0.1", 28888)
        client.send(b"hello")
        n, data = client.recv()
    finally:
        client.close()
        srv.close()

    assert n == 9
    assert data[:n] == b"hello_ack"


def test_stream_tcp() -> None:
    try:
        srv = tcp.StreamServer()
        srv.bind(18888)
        # srv.start_accept()

        # client = tcp.StreamClient()
        # client.connect("127.0.0.1", 28888)

        # pack = tcp.Package(
        #     tcp.Header("login"),
        #     tcp.Body(
        #         tcp.LoginPayload("alvin", "123456"),
        #     ),
        # )
        # client.send(pack)
        # pack = client.recv()
    finally:
        # client.close()
        srv.close()
