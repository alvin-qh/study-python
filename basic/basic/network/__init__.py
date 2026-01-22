import socket
import random


def get_available_port(min_port: int = 1024, max_port: int = 65535) -> int:
    """获取一个可用的端口

    本函数会从 `min_port` 到 `max_port` 中随机获取一个可用的端口

    Args:
        - `min_port` (`int`): 最小端口
        - `max_port` (`int`): 最大端口

    Returns:
        `int`: 可用的端口
    """
    s = socket.socket()

    while True:
        port = random.randint(min_port, max_port)
        try:
            s.bind(("", port))
            s.close()
            return port
        except Exception:
            continue
