from types import TracebackType
from typing import Any, Callable, Optional, Type


class Context:
    """
    记录上下文的类
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        初始化上下文

        通过参数传递的 `Dict` 对象参数值存储到上下文中
        """
        self.__dict__.update(kwargs)

    def __getattr__(self, key: str) -> Any:
        """
        通过上下文的参数名获取参数值

        Args:
            key (str): 参数名

        Returns:
            Any: 参数值
        """
        return self.__dict__[key]

    def __enter__(self) -> "Context":
        """
        进入上下文作用域范围

        Returns:
            Context: 当前对象
        """
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            trace: Optional[TracebackType],
    ) -> None:
        """
        退出上下文作用域范围
        """
        self.__dict__.clear()


class FixtureName:
    """
    记录 `fixture` 名称的类
    """

    def __init__(self) -> None:
        """
        初始化
        """
        self._fixture_name = ""

    def set(self, fixture: Callable[[], Any]) -> None:
        """
        保存 `fixture` 的名称

        Args:
            fixture (FixtureCall): fixture 函数
        """
        self._fixture_name = fixture.__name__

    @property
    def value(self) -> str:
        """
        获取保存的 `fixture` 名称

        Returns:
            str: 保存的 fixture 名称
        """
        return self._fixture_name

    def clear(self) -> None:
        """
        清除保存的 `fixture` 名称
        """
        self._fixture_name = ""


class FixtureVisitorCount:
    """
    记录各 fixture 被调用的次数
    """

    def __init__(self) -> None:
        """
        初始化对象
        """
        # 为字典字段设置初始值
        self._counter = {
            "function": 0,
            "class": 0,
            "module": 0,
            "session": 0
        }

    def increase(self, scope: str) -> None:
        """
        增加调用次数

        Args:
            scope (str): 调用的 `fixture` 范围
        """
        self._counter[scope] += 1

    def __getitem__(self, scope: str) -> int:
        """
        获取指定 `scope` 的 `fixture` 调用次数

        Args:
            scope (str): `fixture` 的 `scope` 名称

        Returns:
            int: 调用次数
        """
        return self._counter[scope]
