import logging
import socket as so
import sys
import threading as th
from io import BufferedRWPair

from ..common import format_addr

log = logging.getLogger()


class _StreamTcp:
    """客户端和服务端的父类"""

    @classmethod
    def _create_tcp(cls) -> so.socket:
        """创建 TCP socket

        Returns:
            `so.socket`: 设置完毕的 socket 对象
        """
        # 创建 socket 对象
        s = so.socket(so.AF_INET, so.SOCK_STREAM)

        # 设置 SO_REUSEADDR 选项, 支持地址复用
        s.setsockopt(so.SOL_SOCKET, so.SO_REUSEADDR, 1)
        return s


class StreamServer(_StreamTcp):
    """TCP 服务端"""

    def __init__(self) -> None:
        """初始化对象"""
        super().__init__()
        self._so: so.socket | None = None
        self._accept_td: th.Thread | None = None

    def listen(self, port: int, addr: str = "", backlog: int = 1) -> None:
        """接收客户端连接

        Args:
            `port` (`int`): 要监听的端口
            `addr` (`str`): 要监听的地址
            `backlog` (`int`): 监听队列的长度
        """
        # 创建服务端 socket 对象
        s = self._create_tcp()

        # 绑定本地端口号
        self._bind(s, (addr, port))

        # 在本地端口启动监听, 并设置监听队列的长度
        s.listen(backlog)

        # 启动线程用于接受客户端连接
        td = th.Thread(target=self._handle_accept, args=(s,))
        td.start()

        self._so = s
        self._accept_td = td

    def _bind(self, s: so.socket, addr: tuple[str, int]) -> None:
        """服务端绑定本地端口

        Args:
            `s` (`so.socket`): socket 对象
            `addr` (`Tuple[str, int]`): 要绑定的本地端口号和地址
        """
        # 绑定本地端口
        s.bind(addr)
        log.info(f"[SERVER] Bind to {format_addr(addr)!r}")

    def _handle_accept(self, s: so.socket) -> None:
        """Accept 线程, 用于监听服务端端口, 接受客户端连接

        Args:
            `s` (`so.socket`): 服务端 socket 对象
        """
        with s:
            while True:
                try:
                    # 接受客户端连接
                    client_so, client_addr = s.accept()
                    log.info(
                        f"[SERVER] Accept connection from {format_addr(client_addr)!r}"
                    )

                    # 启动数据收发线程, 用于处理和客户端的信息交换
                    th.Thread(
                        target=self._handle_recv, args=(client_so, client_addr)
                    ).start()
                except Exception:
                    log.info("[SERVER] Stop listening")
                    break

    def _handle_recv(self, client_so: so.socket, client_addr: tuple[str, int]) -> None:
        """客户端收发线程, 用于处理和客户端的信息交换

        Args:
            `client_so` (`so.socket`): 客户端 socket 对象
            `client_addr` (`Tuple[str, int]`): 客户端地址
        """
        # 通过客户端 socket 对象创建流对象, 并通过流对象接收和发送数据
        # 完成一次信息交换后, socket 对象和流对象都会被关闭, 从而和客户端断开连接
        with client_so, client_so.makefile("rwb") as f:
            while True:
                try:
                    # 通过流对象从客户端发送数据中读取一行数据, 并解码为字符串
                    data = f.readline()
                    msg = data.decode("utf-8")

                    log.info(
                        f"[SERVER] Receive message {msg} from {format_addr(client_addr)!r}"
                    )

                    # 向客户端发送数据
                    f.write(f"{msg.strip()}-ack\n".encode("utf-8"))
                    f.flush()
                except Exception as e:
                    log.info(f"[SERVER] Stop receiving, reason {e}")
                    break

    def close(self) -> None:
        """关闭连接"""
        # 关闭服务端监听
        if self._so:
            if sys.platform.startswith("win"):
                self._so.close()
            else:
                self._so.shutdown(so.SHUT_RDWR)
            self._so = None

        # 等待服务端 accept 线程结束
        if self._accept_td:
            self._accept_td.join()
            self._accept_td = None


class StreamClient(_StreamTcp):
    """TCP 客户端"""

    def __init__(self) -> None:
        super().__init__()

        self._so: so.socket | None = None
        self._addr = ("", 0)
        self._f: BufferedRWPair | None = None

    def connect(self, host: str, port: int) -> None:
        """连接到远程服务端

        Args:
            `host` (`str`): 远程服务端地址
            `port` (`int`): 远程服务端口号
        """
        addr = (host, port)

        # 创建客户端 socket 对象
        s = self._create_tcp()

        # 令客户端 socket 对象连接到远程服务端
        s.connect(addr)

        # 通过客户端连接 socket 创建流对象, 用于和服务端通信
        f = s.makefile("rwb")
        log.info(f"[CLIENT] Connect to {format_addr(addr)!r}")

        self._so = s
        self._f = f
        self._addr = addr

    def recv(self) -> str:
        """接收数据

        Returns:
            `str`: 接收数据的结果, 为字符串
        """
        f = self._f
        if not f:
            raise Exception("Not connected")

        # 通过流对象从服务端接收数据, 接收一行数据并解码为字符串
        data = f.readline()
        msg = data.decode("utf-8")

        log.info(f"[CLIENT] Receive message {msg} from {format_addr(self._addr)!r}")

        return msg

    def send(self, msg: str) -> None:
        """发送数据

        Args:
            `msg` (`str`): 要发送的字符串数据
        """
        f = self._f
        if not f:
            raise Exception("Not connected")

        # 通过流对象向服务端发送数据, 发送一整行字符串数据
        f.write(f"{msg}\n".encode("utf-8"))
        f.flush()

        log.info(f"[CLIENT] Message {msg} was sent")

    def close(self) -> None:
        """关闭连接"""
        if self._f:
            self._f.close()
            self._f = None

        if self._so:
            self._so.close()
            self._so = None
