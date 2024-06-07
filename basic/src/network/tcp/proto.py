from abc import ABC


class Payload(ABC):
    pass


class Header:
    def __init__(self, cmd: str) -> None:
        self._cmd = cmd

    @property
    def cmd(self) -> str:
        return self._cmd


class Body:
    def __init__(self, payload: Payload) -> None:
        self._payload = payload

    @property
    def payload(self) -> Payload:
        return self._payload


class Package:
    def __init__(self, header: Header, body: Body) -> None:
        self._header = header
        self._body = body

    @property
    def header(self) -> Header:
        return self._header

    @property
    def body(self) -> Body:
        return self._body


class LoginPayload(Payload):
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password


class LoginAckPayload(Payload):
    def __init__(self, success: bool, err: str) -> None:
        self.success = success
        self.err = err


class ByePayload(Payload):
    def __init__(self, word: str = "goodbye") -> None:
        self.word = word


class ByeAckPayload(Payload):
    def __init__(self, word: str = "bye bye") -> None:
        self.word = word
