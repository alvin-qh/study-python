from typing import Literal, TypeAlias, Union

Status: TypeAlias = Union[
    Literal["ready"],
    Literal["started"],
    Literal["finished"],
]


class Step:
    """
    步骤记录类
    """
    _state: Status

    def __init__(self) -> None:
        """
        初始化, 表示未开始
        """
        self._state = "ready"

    def start(self) -> None:
        """
        初始化, 表示执行中
        """
        self._state = "started"

    def finish(self) -> None:
        """
        初始化, 表示已结束
        """
        self._state = "finished"

    @property
    def state(self) -> Status:
        """
        获取状态

        Returns:
            str: 状态值
        """
        return self._state


class Counter:
    """
    计数器类
    """

    def __init__(self) -> None:
        """
        初始化计数器
        """
        self._value = 0

    def increase(self) -> None:
        """
        增加计数
        """
        self._value += 1

    @property
    def value(self) -> int:
        """
        获取计数值

        Returns:
            int: 计数值
        """
        return self._value
