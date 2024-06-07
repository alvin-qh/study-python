import logging
import pickle
import socket as so
from typing import IO, Optional, Tuple, cast

from ..common import format_addr
import threading

from .proto import (
    Body,
    ByeAckPayload,
    ByePayload,
    Header,
    LoginAckPayload,
    LoginPayload,
    Package,
)

log = logging.getLogger()


class _Tcp:
    """客户端和服务端的父类"""

    def __init__(self) -> None:
        """实例化对象"""
        # 创建 socket 对象, 使用 TCP 协议
        self._so = so.socket(so.AF_INET, so.SOCK_STREAM)

    def close(self) -> None:
        """关闭连接"""
        if self._so:
            self._so.close()


class StreamServer(_Tcp):
    """TCP 服务端"""

    def __init__(self) -> None:
        """初始化对象"""
        self._so = so.socket(so.AF_INET, so.SOCK_STREAM)
        self._accept_td: Optional[threading.Thread] = None

    def bind(self, port: int, addr: str = "") -> None:
        """服务端绑定本地端口

        Args:
            `port` (`int`): 本地端口号
            `addr` (`str`, optional): 要绑定的本机地址. Defaults to "".
        """
        # 绑定本地端口
        local_addr = (addr, port)
        self._so.bind(local_addr)
        log.info(f"[SERVER] Bind to {format_addr(local_addr)!r}")

    def _handle_recv(self, client_so: so.socket, client_addr: Tuple[str, int]) -> None:
        """处理数据接收"""
        with client_so:
            with client_so.makefile("rb") as f:
                while True:
                    try:
                        # 接收客户端数据
                        pack = cast(Package, pickle.load(f))
                        log.info(
                            f"[SERVER] Receive {pack!r} from {format_addr(client_addr)!r}"
                        )

                        match pack.header.cmd:
                            case "login":
                                self._handle_login(f, client_addr, pack)
                            case "bye":
                                self._handle_bye(f, client_addr, pack)
                            case _:
                                log.info(
                                    f"[SERVER] Unrecognized cmd: {pack.header.cmd}"
                                )
                                break
                    except Exception:
                        log.info("[SERVER] Stop listening")
                        break

    def _handle_login(
        self, f: IO[bytes], client_addr: Tuple[str, int], pack: Package
    ) -> None:
        """处理登录"""
        p = cast(LoginPayload, pack.body.payload)
        log.info(
            f"[SERVER] User {p.username!r} with password {p.password!r} from {format_addr(client_addr)!r}"
        )

        pack = Package(
            Header(cmd="login"),
            Body(LoginAckPayload(True, "")),
        )
        pickle.dump(pack, f)

    def _handle_bye(
        self, f: IO[bytes], client_addr: Tuple[str, int], pack: Package
    ) -> None:
        """处理退出"""
        p = cast(ByePayload, pack.body.payload)
        log.info(f"[SERVER] Bye word {p.word!r} from {format_addr(client_addr)!r}")

        pack = Package(
            Header(cmd="bye"),
            Body(ByeAckPayload()),
        )
        pickle.dump(pack, f)

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


class StreamClient(_Tcp):
    """TCP 客户端"""

    def __init__(self) -> None:
        self._so = so.socket(so.AF_INET, so.SOCK_STREAM)
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

    def recv(self) -> Package:
        """接收数据

        Returns:
            `Tuple[int, bytes]`: 接收数据的结果, 为一个三元组, 分别为 `(数据长度, 远端地址, 数据内容)`
        """
        with self._so.makefile("rb") as f:
            return cast(Package, pickle.load(f))

    def send(self, pack: Package) -> None:
        """发送数据

        Args:
            `data` (`bytes`): 被发送的数据
            `addr` (`Tuple[str, int]`): 远端地址

        Returns:
            `int`: 发送数据的长度
        """
        with self._so.makefile("wb") as f:
            pickle.dump(pack, f)
