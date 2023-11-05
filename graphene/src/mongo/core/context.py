from types import TracebackType
from typing import Any, Optional, Type, cast

from werkzeug.local import Local


class Tenant:
    """租户接口"""


class Context:
    """上下文类型

    上下文对象相当于一个可以存储任意键值对的容器
    """

    def __init__(self) -> None:
        """实例化线程安全的上下文对象"""
        self.__dict__["_ctx"] = Local()

    def __getattr__(self, key: str, default: Any = None) -> Any:
        """获取上下文属性值

        即 `属性值 = context.<属性名称>`

        Args:
            - `key` (`str`): 属性名称
            - `default` (`Any`, optional): 属性默认值. Defaults to `None`.

        Returns:
            Any: 属性值
        """
        local = self.__dict__["_ctx"]
        try:
            return local.__getattr__(key)
        except AttributeError:
            return default

    def __setattr__(self, key: str, value: Any) -> None:
        """设置上下文属性值

        即 `context.<属性名称> = 属性值`

        Args:
            - `key` (`str`): 属性名称
            - `value` (`Any`): 属性值
        """
        local = self.__dict__["_ctx"]
        local.__setattr__(key, value)

    def __delattr__(self, key: str) -> None:
        """删除上下文属性值

        即 `del context.<属性名称>`

        Args:
            - `key` (`str`): 属性名称
        """
        local = self.__dict__["_ctx"]
        local.__delattr__(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """通过下标设置上下文属性值

        即 `context[<属性名称>] = 属性值`

        Args:
            - `key` (`str`): 属性名称
            - `value` (`Any`): 属性值
        """
        self.__setattr__(key, value)

    def __getitem__(self, key: str) -> Any:
        """通过下标获取上下文属性值

        即 `属性值 = context[<属性名称>]`

        Args:
            - `key` (`str`): 属性名称

        Returns:
            `Any`: 属性值
        """
        return self.__getattr__(key)

    def __delitem__(self, key: str) -> None:
        """通过下标删除上下文属性值

        即 `del context[<属性名称>]`

        Args:
            - `key` (`str`): 属性名称
        """
        self.__delattr__(key)

    def delete(self, key: str) -> None:
        self.__delattr__(key)

    def clear(self) -> None:
        """删除所有属性值, 即释放本地现场变量"""
        local = cast(Local, self._ctx)
        local.__release_local__()
        self.__dict__["_ctx"] = Local()

    class TenantContext:
        """多租户上下文"""

        def __init__(self, ctx: "Context", tenant: Tenant) -> None:
            self._ctx = ctx
            self._tenant = tenant

        def __enter__(self) -> None:
            """进入上下文作用域"""
            self._ctx["_tenant"] = self._tenant

        def __exit__(
            self,
            exc_type: Optional[Type[Exception]],
            exc_value: Optional[Exception],
            exc_tb: Optional[TracebackType],
        ) -> None:
            """退出上下文作用域"""
            self._ctx.delete("_tenant")

    def with_tenant_context(self, tenant: Tenant) -> TenantContext:
        """获取租户上下文对象"""
        return self.TenantContext(self, tenant)

    def get_current_tenant(self) -> Tenant:
        """获取当前上下文租户"""
        return cast(Tenant, self["_tenant"])


# 实例化上下文对象
context: Context = Context()
