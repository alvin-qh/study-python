import logging
import socket as so
from typing import Optional, Tuple

from ..common import format_addr
import threading

log = logging.getLogger()


class _Tcp:
    """客户端和服务端的父类"""

    def __init__(self) -> None:
        """实例化对象"""
        # 创建 socket 对象, 使用 TCP 协议
        self._so = so.socket(so.AF_INET, so.SOCK_STREAM)


_suffix = b"_ack"


class SyncServer(_Tcp):
    """TCP 服务端"""

    def __init__(self) -> None:
        """初始化对象"""
        super().__init__()
        self._accept_td: Optional[threading.Thread] = None

    def bind(self, port: int, addr: str = "") -> None:
        """服务端绑定本地端口

        Args:
            `port` (`int`): 本地端口号
            `addr` (`str`, optional): 要绑定的本机地址. Defaults to "".
        """
        # 绑定本地端口
        self._so.bind((addr, port))
        log.info(f"[SERVER] Bind to {format_addr((addr, port))!r}")

    def _handle_recv(self, client_so: so.socket, client_addr: Tuple[str, int]) -> None:
        """处理数据接收"""
        buf = bytearray(1024)

        with client_so:
            while True:
                # 接收客户端数据
                n = client_so.recv_into(buf, len(buf))
                if n == 0:
                    # 接收数据长度为 0, 表示服务端连接已断开
                    log.info(
                        f"[SERVER] Connection closed from {format_addr(client_addr)!r}"
                    )
                    break

                log.info(
                    f"[SERVER] Received {buf[:n]!r} from {format_addr(client_addr)!r}"
                )

                # 给接收数据增加后缀后发送回客户端
                buf[n:] = _suffix
                n = client_so.send(buf[: n + len(_suffix)])
                log.info(
                    f"[SERVER] Send {buf[: n + len(_suffix)]!r} to {format_addr(client_addr)!r}"
                )

    def _handle_accept(self) -> None:
        """处理 Accept"""
        with self._so:
            while True:
                try:
                    # 接受客户端连接
                    client_so, client_addr = self._so.accept()
                    log.info(
                        f"[SERVER] Accept connection from {format_addr(client_addr)!r}"
                    )

                    # 启动线程接受客户端发送数据
                    threading.Thread(
                        target=self._handle_recv, args=(client_so, client_addr)
                    ).start()
                except Exception:
                    log.info("[SERVER] Stop listening")
                    break

    def start_accept(self, backlog: int = 1) -> None:
        """接收客户端连接"""
        # 在本地端口启动监听, 并设置监听队列的长度
        self._so.listen(backlog)

        # 启动线程用于接受客户端连接
        self._accept_td = threading.Thread(target=self._handle_accept)
        self._accept_td.start()

    def close(self) -> None:
        """关闭连接"""
        # 关闭服务端监听
        self._so.shutdown(so.SHUT_RDWR)

        # 等待服务端 accept 线程结束
        if self._accept_td:
            self._accept_td.join()
            self._accept_td = None


class SyncClient(_Tcp):
    """TCP 客户端"""

    def __init__(self) -> None:
        super().__init__()
        self._buf = bytearray(0)
        self._addr = ("", 0)

    def connect(self, host: str, port: int) -> None:
        """连接到远程服务端

        Args:
            `addr` (`tuple[str, int]`): 远程服务端地址
        """
        addr = (host, port)

        self._so.connect_ex(addr)

        self._addr = addr
        self._buf = bytearray(1024)

        log.info(f"[CLIENT] Connect to {format_addr(addr)!r}")

    def recv(self) -> Tuple[int, bytes]:
        """接收数据

        Returns:
            `Tuple[int, bytes]`: 接收数据的结果, 为一个三元组, 分别为 `(数据长度, 远端地址, 数据内容)`
        """
        n = self._so.recv_into(self._buf, len(self._buf))

        if n == 0:
            log.info(f"[CLIENT] Connection closed from {format_addr(self._addr)!r}")
            self.close()
        else:
            log.info(
                f"[CLIENT] Received {self._buf[:n].decode()!r} from {format_addr(self._addr)!r}"
            )

        return n, bytes(self._buf)

    def send(self, data: bytes) -> int:
        """发送数据

        Args:
            `data` (`bytes`): 被发送的数据
            `addr` (`Tuple[str, int]`): 远端地址

        Returns:
            `int`: 发送数据的长度
        """
        n = self._so.send(data)
        log.info(f"[CLIENT] Data {data[:n]!r} send to {format_addr(self._addr)!r}")
        return n

    def close(self) -> None:
        """关闭连接"""
        self._so.close()
        log.info(f"[CLIENT] Close connection to {format_addr(self._addr)!r}")
