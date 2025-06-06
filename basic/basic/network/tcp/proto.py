from abc import ABC


class Payload(ABC):
    """数据载荷类型"""

    def __repr__(self) -> str:
        """将数据载荷格式化为字符串"""
        return ""


class Header:
    """数据包头类型

    数据包头包含 `cmd` 属性作为包的类别标识
    """

    def __init__(self, cmd: str) -> None:
        self._cmd = cmd

    @property
    def cmd(self) -> str:
        return self._cmd

    def __repr__(self) -> str:
        return f"{{ cmd={self._cmd!r} }}"


class Body:
    """数据包体类型

    数据包体包含 payload 属性作为实际数据载荷
    """

    def __init__(self, payload: Payload) -> None:
        self._payload = payload

    @property
    def payload(self) -> Payload:
        return self._payload

    def __repr__(self) -> str:
        return f"{{ payload={self._payload!r} }}"


class Package:
    """定义一个数据包类型

    数据包包含 `header` 作为数据包头, `body` 作为数据包体
    """

    def __init__(self, header: Header, body: Body) -> None:
        self._header = header
        self._body = body

    @property
    def header(self) -> Header:
        return self._header

    @property
    def body(self) -> Body:
        return self._body

    def __repr__(self) -> str:
        return f"{{ header={self.header!r}, body={self.body!r} }}"


class LoginPayload(Payload):
    """登录请求数据包的数据载荷类型"""

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f"{{ username={self.username!r}, password={self.password!r} }}"


class LoginAckPayload(Payload):
    """登录响应数据包的数据载荷类型"""

    def __init__(self, success: bool, err: str) -> None:
        self.success = success
        self.err = err

    def __repr__(self) -> str:
        return f"{{ success={self.success!r}, err={self.err!r} }}"


class ByePayload(Payload):
    """离开请求数据包的数据载荷类型"""

    def __init__(self, word: str = "goodbye") -> None:
        self.word = word

    def __repr__(self) -> str:
        return f"{{ word={self.word!r} }}"


class ByeAckPayload(Payload):
    """离开响应数据包的数据载荷类型"""

    def __init__(self, word: str = "bye bye") -> None:
        self.word = word

    def __repr__(self) -> str:
        return f"{{ word={self.word!r} }}"
