from io import BufferedRWPair
import logging
import pickle
import socket as so
from typing import Optional, Tuple, cast

from ..common import format_addr
import threading as th

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


class _StreamTcp:
    """客户端和服务端的父类"""

    @classmethod
    def _create_tcp(cls) -> so.socket:
        """创建 TCP socket"""
        s = so.socket(so.AF_INET, so.SOCK_STREAM)
        s.setsockopt(so.SOL_SOCKET, so.SO_REUSEADDR, 1)
        return s


class StreamServer(_StreamTcp):
    """TCP 服务端"""

    def __init__(self) -> None:
        """初始化对象"""
        super().__init__()
        self._so: Optional[so.socket] = None
        self._accept_td: Optional[th.Thread] = None

    def listen(self, port: int, addr: str = "", backlog: int = 1) -> None:
        """接收客户端连接"""
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

    def _bind(self, s: so.socket, addr: Tuple[str, int]) -> None:
        """服务端绑定本地端口

        Args:
            `s` (`so.socket`): socket 对象
            `addr` (`Tuple[str, int]`): 要绑定的本地端口号和地址
        """
        # 绑定本地端口
        s.bind(addr)
        log.info(f"[SERVER] Bind to {format_addr(addr)!r}")

    def _handle_accept(self, s: so.socket) -> None:
        """处理 Accept

        Args:
            `s` (`so.socket`): socket 对象
        """
        with s:
            while True:
                try:
                    # 接受客户端连接
                    client_so, client_addr = s.accept()
                    log.info(
                        f"[SERVER] Accept connection from {format_addr(client_addr)!r}"
                    )

                    # 启动线程接受客户端发送数据
                    th.Thread(
                        target=self._handle_recv, args=(client_so, client_addr)
                    ).start()
                except Exception:
                    log.info("[SERVER] Stop listening")
                    break

    def _handle_recv(self, client_so: so.socket, client_addr: Tuple[str, int]) -> None:
        """处理数据接收"""
        with client_so:
            with client_so.makefile("rwb") as f:
                while True:
                    try:
                        # 接收客户端数据
                        pack = cast(Package, pickle.load(f))
                        log.info(
                            f"[SERVER] Receive {pack!r} from {format_addr(client_addr)!r}"
                        )

                        # 根据客户端数据包头信息选择后续处理逻辑
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
                    except Exception as e:
                        log.info(f"[SERVER] Stop receiving, reason {e}")
                        break

    def _handle_login(
        self, f: BufferedRWPair, client_addr: Tuple[str, int], pack: Package
    ) -> None:
        """处理登录逻辑"""

        # 将数据包类型转为登录包类型
        p = cast(LoginPayload, pack.body.payload)
        log.info(
            f"[SERVER] User {p.username!r} with password {p.password!r} from {format_addr(client_addr)!r}"
        )

        # 生成登录确认相应包
        pack = Package(
            Header(cmd="login"),
            Body(LoginAckPayload(True, "")),
        )
        # 将登录响应包返回
        pickle.dump(pack, f)
        f.flush()

    def _handle_bye(
        self, f: BufferedRWPair, client_addr: Tuple[str, int], pack: Package
    ) -> None:
        """处理退出"""
        p = cast(ByePayload, pack.body.payload)
        log.info(f"[SERVER] Bye word {p.word!r} from {format_addr(client_addr)!r}")

        pack = Package(
            Header(cmd="bye"),
            Body(ByeAckPayload()),
        )
        pickle.dump(pack, f)
        f.flush()

    def close(self) -> None:
        """关闭连接"""
        # 关闭服务端监听
        if self._so:
            self._so.close()
            self._so = None

        # 等待服务端 accept 线程结束
        if self._accept_td:
            self._accept_td.join()
            self._accept_td = None


class StreamClient(_StreamTcp):
    """TCP 客户端"""

    def __init__(self) -> None:
        super().__init__()

        self._so: Optional[so.socket] = None
        self._addr = ("", 0)
        self._buf = bytearray(0)

        self._f: Optional[BufferedRWPair] = None

    def connect(self, host: str, port: int) -> None:
        """连接到远程服务端

        Args:
            `host` (`str`): 远程服务端地址
            `port` (`int`): 远程服务端口号
        """
        addr = (host, port)

        s = self._create_tcp()
        s.connect(addr)

        f = s.makefile("rwb")
        log.info(f"[CLIENT] Connect to {format_addr(addr)!r}")

        self._so = s
        self._f = f

        self._addr = addr
        self._buf = bytearray(1024)

    def recv(self) -> Package:
        """接收数据

        Returns:
            `Tuple[int, bytes]`: 接收数据的结果, 为一个三元组, 分别为 `(数据长度, 远端地址, 数据内容)`
        """
        f = self._f
        if not f:
            raise Exception("Not connected")

        pack = cast(Package, pickle.load(f))
        log.info(f"[CLIENT] Receive {pack!r} from {format_addr(self._addr)!r}")

        return pack

    def send(self, pack: Package) -> None:
        """发送数据

        Args:
            `pack` (`Package`): 要发送的数据包

        Returns:
            `int`: 发送数据的长度
        """
        f = self._f
        if not f:
            raise Exception("Not connected")

        pickle.dump(pack, f)
        f.flush()
        log.info(f"[CLIENT] Package {pack} was sent")

    def close(self) -> None:
        """关闭连接"""
        if self._f:
            self._f.close()
            self._f = None

        if self._so:
            self._so.close()
            self._so = None
