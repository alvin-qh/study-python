import socket as so


class SyncServer:
    def __init__(self) -> None:
        self._socket = so.socket(so.AF_INET, so.SOCK_DGRAM)
        self._buf = bytearray(1024)

    def bind(self, port: int, addr: str = "") -> None:
        self._socket.bind((addr, port))

    def recv(self) -> bytes:
        self._socket.recvfrom_into(self._buf, len(self._buf))
        return bytes(self._buf)
