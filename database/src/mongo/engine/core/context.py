from types import TracebackType
from typing import Any, Optional, Type, cast

from mongoengine import StringField
from werkzeug.local import Local


class TenantMixin:
    """租户接口"""

    name: str = StringField(required=True)


class Context:
    """上下文类型

    上下文对象相当于一个可以存储任意键值对的容器
    """

    def __init__(self) -> None:
        """实例化线程安全的上下文对象"""
        self.__dict__["_ctx"] = Local()

    def __getattr__(self, item: str, default: Any = None) -> Any:
        """获取当属性值

        即 `属性值 = context.<属性名称>`

        Args:
            item (str): 属性名称
            default (Any, optional): 属性默认值. Defaults to None.

        Returns:
            Any: 属性值
        """
        local: Local = self.__dict__["_ctx"]
        try:
            return local.__getattr__(item)
        except AttributeError:
            return default

    def __setattr__(self, key: str, value: Any) -> None:
        """设置属性值

        即 `context.<属性名称> = 属性值`

        Args:
            key (str): 属性名称
            value (Any): 属性值
        """
        local: Local = self.__dict__["_ctx"]
        local.__setattr__(key, value)

    def __delattr__(self, item: str) -> None:
        """删除属性值

        即 `del context.<属性名称>`

        Args:
            item (str): 属性名称
        """
        local: Local = self.__dict__["_ctx"]
        local.__delattr__(item)

    def __setitem__(self, key: str, value: Any) -> None:
        """通过下标设置属性值

        即 `context[<属性名称>] = 属性值`

        Args:
            key (str): 属性名称
            value (Any): 属性值
        """
        self.__setattr__(key, value)

    def __getitem__(self, item: str) -> Any:
        """获取当属性值

        即 `属性值 = context[<属性名称>]`

        Args:
            item (str): 属性名称

        Returns:
            Any: 属性值
        """
        return self.__getattr__(item)

    def __delitem__(self, key: str) -> None:
        """删除属性值

        即 `del context[<属性名称>]`

        Args:
            item (str): 属性名称
        """
        self.__delitem__(key)

    def delete(self, key: str) -> None:
        self.__delattr__(key)

    def clear(self) -> None:
        """删除所有属性值"""
        cast(Local, self._ctx).__release_local__()

    class _TenantContext:
        """多租户上下文"""

        def __init__(self, ctx: "Context", org: TenantMixin) -> None:
            self._ctx = ctx
            self._org = org

        def __enter__(self) -> None:
            """进入上下文作用域"""
            self._ctx["org"] = self._org

        def __exit__(
            self,
            exc_type: Optional[Type[Exception]],
            exc_value: Optional[Exception],
            exc_tb: Optional[TracebackType],
        ) -> None:
            """推出上下文作用域"""
            self._ctx.delete("org")

    def with_tenant_context(self, org: TenantMixin) -> _TenantContext:
        """获取租户上下文对象"""
        return self._TenantContext(self, org)

    def get_current_org(self) -> TenantMixin:
        """获取当前上下文租户"""
        return cast(TenantMixin, self["org"])


# 定义上下文对象
context: Context = Context()
