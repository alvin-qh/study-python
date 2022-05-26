from types import TracebackType
from typing import Any, Dict, Optional, Tuple, Type


class Context:
    _kv: Dict[str, Any]
    exception: Optional[Tuple[Type[Exception], Exception]]

    def __init__(self, deliver_exc=False) -> None:
        self._kv = {}
        self._deliver_exc = deliver_exc

        self.exception = None

    def put(self, key: str, val: Any) -> None:
        self._kv[key] = val

    def get(self, key: str) -> Any:
        return self._kv[key]

    def close(self) -> None:
        self._kv = {}

    def __enter__(self) -> "Context":
        return self

    def __exit__(
        self,
        exc_type: Type[Exception],
        exc_value: Exception,
        exc_tb: TracebackType,
    ) -> bool:
        self.close()
        self.exception = (exc_type, exc_value)
        return self._deliver_exc
