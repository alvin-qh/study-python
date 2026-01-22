import logging
import socket as so
from typing import Tuple

from ..common import format_addr

log = logging.getLogger()


class _Udp:
    """客户端和服务端的父类"""

    # 表示服务端或客户端的标志
    __tag__ = ""

    def __init__(self) -> None:
        """实例化对象"""
        # 创建 socket 对象, 使用 UDP 协议
        self._so = so.socket(so.AF_INET, so.SOCK_DGRAM)

        # 创建数据接收缓冲区
        self._buf = bytearray(1024)

    def recv(self) -> tuple[int, tuple[str, int], bytes]:
        """接收数据

        Returns:
            `tuple[int, tuple[str, int], bytes]`: 接收数据的结果, 为一个三元组, 分别为 `(数据长度, 远端地址, 数据内容)`
        """
        # 接收数据, 并放入缓冲区中, 返回数据长度和远端地址
        n, addr = self._so.recvfrom_into(self._buf, len(self._buf))
        log.info(
            f"[{self.__tag__}] Data {self._buf[:n].decode()!r} received from {addr!r}"
        )
        return n, addr, bytes(self._buf)

    def sendto(self, data: bytes, addr: Tuple[str, int]) -> int:
        """发送数据

        Args:
            `data` (`bytes`): 被发送的数据
            `addr` (`Tuple[str, int]`): 远端地址

        Returns:
            `int`: 发送数据的长度
        """
        n = self._so.sendto(data, addr)
        log.info(f"[{self.__tag__}] Data {data.decode()!r} send to {addr!r}")
        return n

    def close(self) -> None:
        """关闭连接"""
        if self._so:
            self._so.close()


class SyncServer(_Udp):
    """UDP 服务端"""

    __tag__ = "SERVER"

    def bind(self, port: int, addr: str = "") -> None:
        """服务端绑定本地端口

        Args:
            `port` (`int`): 本地端口号
            `addr` (`str`, optional): 要绑定的本机地址. Defaults to "".
        """
        self._so.bind((addr, port))
        log.info(f"[{self.__tag__}] Bind to {format_addr((addr, port))!r}")


class SyncClient(_Udp):
    """UDP 客户端"""

    __tag__ = "CLIENT"

    def connect(self, addr: tuple[str, int]) -> None:
        """连接到远程服务端

        Args:
            `addr` (`tuple[str, int]`): 远程服务端地址
        """
        self._so.connect_ex(addr)
        log.info(f"[{self.__tag__}] Connect to {format_addr(addr)!r}")
