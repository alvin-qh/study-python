from typing import Any, Dict
import eventlet
from loguru import logger

import socketio

client_mgr = socketio.RedisManager(
    url="redis://localhost:6739/0",
    channel="socketio",
    write_only=False,
    logger=logger,
)

# 创建服务端对象
sio = socketio.Server(
    client_manager=client_mgr,
    logger=logger,
    always_connect=True,
)

# 创建 WSGI 服务对象
app = socketio.WSGIApp(
    sio,
    socketio_path="_sio",
)


@sio.event
def connect(sid: str, environ: Dict[str, Any]):
    """
    处理连接成功的事件

    Args:
        sid (str): 客户端 id
        environ (Dict[str, Any]): 连接上下文
    """
    logger.info("Client '{}' connected", sid)


@sio.event
def my_message(sid, data):
    print("message ", data)


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 5600)), app)
