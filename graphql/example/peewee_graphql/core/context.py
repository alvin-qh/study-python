from functools import wraps
from typing import Any, Callable

from werkzeug.local import Local


class Context:
    def __init__(self) -> None:
        self.__dict__["_ctx"] = Local()

    def __getattr__(self, item: str, default: Any = None) -> Any:
        local: Local = self.__dict__["_ctx"]
        try:
            return local.__getattr__(item)
        except AttributeError:
            return default

    def __setattr__(self, key: str, value: Any) -> None:
        local: Local = self.__dict__["_ctx"]
        local.__setattr__(key, value)

    def __delattr__(self, item: str) -> None:
        local: Local = self.__dict__["_ctx"]
        local.__delattr__(item)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__setattr__(key, value)

    def __getitem__(self, item: str) -> Any:
        return self.__getattr__(item)

    def __delitem__(self, key: str) -> None:
        self.__delitem__(key)

    def delete(self, key: str) -> None:
        self.__delattr__(key)

    def clear(self) -> None:
        self._ctx.__release_local__()

    class _TenantContext:
        def __init__(self, ctx: "Context", org: "Org"):
            self._ctx = ctx
            self._org = org

        def __enter__(self):
            self._ctx["org"] = self._org

        def __exit__(self, exc_type, exc_val, exc_tb):
            self._ctx.delete("org")

    class _LoginUserContext:
        def __init__(self, ctx: "Context", login_user: "Employee"):
            self._ctx = ctx
            self._login_user = login_user

        def __enter__(self):
            self._ctx["user"] = self._login_user

        def __exit__(self, exc_type, exc_val, exc_tb):
            self._ctx.delete("user")

    def with_tenant_context(self, org: "Org"):
        return self._TenantContext(self, org)

    def with_login_user(self, login_user: "Employee"):
        return self._LoginUserContext(self, login_user)

    def get_current_org(self) -> "Org":
        return self["org"]

    def get_current_user(self) -> "Employee":
        return self["user"]


context = Context()


def run_once(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = getattr(func, "_called_once", Ellipsis)
        if result is Ellipsis:
            result = func(*args, **kwargs)
            setattr(func, "_called_once", result)

        return result

    return wrapper
