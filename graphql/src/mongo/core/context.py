from functools import wraps
from types import TracebackType
from typing import Any, Callable, Optional, Type, cast

from werkzeug.local import Local


class AbstractOrg:
    pass


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
        cast(Local, self._ctx).__release_local__()

    class _TenantContext:
        def __init__(self, ctx: "Context", org: AbstractOrg) -> None:
            self._ctx = ctx
            self._org = org

        def __enter__(self) -> None:
            self._ctx["org"] = self._org

        def __exit__(
            self,
            exc_type: Optional[Type[Exception]],
            exc_value: Optional[Exception],
            exc_tb: Optional[TracebackType],
        ) -> None:
            self._ctx.delete("org")

    def with_tenant_context(self, org: AbstractOrg) -> _TenantContext:
        return self._TenantContext(self, org)

    def get_current_org(self) -> AbstractOrg:
        return cast(AbstractOrg, self["org"])


context: Context = Context()


def run_once(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = getattr(func, "_called_once", Ellipsis)
        if result is Ellipsis:
            result = func(*args, **kwargs)
            setattr(func, "_called_once", result)

        return result

    return wrapper
