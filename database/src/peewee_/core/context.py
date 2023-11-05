from types import TracebackType
from typing import Any, Optional, Type, cast

from werkzeug.local import Local


class Tenant:
    """租户接口"""

    # 获取主键
    def _get_id(self) -> int:
        """获取租户 id

        Returns:
            int: 租户 id 值
        """
        return 0


class User:
    """用户接口"""

    # 获取主键
    def _get_id(self) -> int:
        return 0


class Context:
    """记录线程本地上下文的类型"""

    def __init__(self) -> None:
        """构造器"""
        self.__dict__["_ctx"] = Local()

    def __getattr__(self, key: str, default: Any = None) -> Any:
        """获取上下文属性

        Args:
            - `key` (`str`): 属性名
            - `default` (`Any`, optional): 属性默认值. Defaults to `None`.

        Returns:
            `Any`: 属性值
        """
        local = self.__dict__["_ctx"]
        if not local:
            return default

        try:
            return local.__getattr__(key)
        except AttributeError:
            return default

    def __setattr__(self, key: str, value: Any) -> None:
        """设置上下文属性

        Args:
            - `key` (`str`): 属性名
            - `value` (`Any`): 属性值
        """
        local = self.__dict__["_ctx"]
        local.__setattr__(key, value)

    def __delattr__(self, key: str) -> None:
        """删除属性值

        Args:
            - `key` (`str`): 属性名
        """
        local = self.__dict__["_ctx"]
        local.__delattr__(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """以下标形式设置上下文属性

        Args:
            - `key` (`str`): 属性名
            - `value` (`Any`): 属性值
        """
        self.__setattr__(key, value)

    def __getitem__(self, key: str) -> Any:
        """以下标形式获取上下文属性

        Args:
            - `key` (`str`): 属性名

        Returns:
            `Any`: 属性值
        """
        return self.__getattr__(key)

    def __delitem__(self, key: str) -> None:
        """以下标形式删除上下文属性

        Args:
            - `key` (`str`): 属性值
        """
        self.__delattr__(key)

    def delete(self, key: str) -> None:
        """以函数方式删除属性值

        Args:
            - `key` (`str`): 属性名称
        """
        self.__delattr__(key)

    def clear(self) -> None:
        """清除上下文中的所有属性"""
        local: Local = self._ctx
        local.__release_local__()
        self.__dict__["_ctx"] = Local()

    class TenantContext:
        """多租户上下文类型"""

        def __init__(self, ctx: "Context", tenant: Tenant) -> None:
            self._ctx = ctx
            self._tenant = tenant

        def __enter__(self) -> None:
            """进入作用于范围, 记录租户对象"""
            self._ctx["_tenant"] = self._tenant

        def __exit__(
            self,
            exc_type: Optional[Type[Exception]],
            exc_value: Optional[Exception],
            exc_tb: Optional[TracebackType],
        ) -> None:
            """退出作用域范围, 删除租户对象"""
            self._ctx.delete("_tenant")

    class CurrentUserContext:
        """当前用户上下文类型"""

        def __init__(self, ctx: "Context", user: User) -> None:
            self._ctx = ctx
            self._user = user

        def __enter__(self) -> None:
            """进入作用于范围, 记录用户对象"""
            self._ctx["_user"] = self._user

        def __exit__(
            self,
            exc_type: Optional[Type[Exception]],
            exc_value: Optional[Exception],
            exc_tb: Optional[TracebackType],
        ) -> None:
            """退出作用于范围, 删除用户对象"""
            self._ctx.delete("_user")

    def with_tenant_context(self, org: Tenant) -> TenantContext:
        """产生一个租户上下文对象

        Args:
            - `org` (`Tenant`): 租户对象

        Returns:
            `TenantContext`: 租户上下文对象
        """
        return self.TenantContext(self, org)

    def with_current_user(self, user: User) -> CurrentUserContext:
        """产生一个用户上下文对象

        Args:
            - `user` (`User`): 用户对象

        Returns:
            `CurrentUserContext`: 用户上下文对象
        """
        return self.CurrentUserContext(self, user)

    def get_current_tenant(self) -> Tenant:
        """获取上下文中存储的当前租户

        Returns:
            `Tenant`: 租户对象
        """
        return cast(Tenant, self["_tenant"])

    def get_current_user(self) -> Optional[User]:
        """获取上下文中存储的当前用户

        Returns:
            `User`: 用户对象
        """
        return cast(User, self.__getattr__("_user"))


# 实例化上下文对象
context = Context()
