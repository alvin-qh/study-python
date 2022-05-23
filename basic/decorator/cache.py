import inspect
import re
from typing import (Any, Callable, Dict, Iterable, List, Optional, Tuple,
                    TypeVar)

from wrapt import decorator


class Cache:
    _data: Dict[str, Any]

    def __init__(self) -> None:
        self._data = {}

    def keys(self) -> Iterable[str]:
        return self._data.keys()

    def items(self) -> Dict[Any, Any]:
        return self._data.items()

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def delete(self, key: str) -> None:
        try:
            del self._data[key]
        except AttributeError:
            pass

    def delete_many(
        self,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
    ) -> None:
        for key in list(self.keys()):
            if (
                (prefix and key.startswith(prefix)) or
                (suffix and key.endswith(suffix))
            ):
                self.delete(key)

    def populate(self, data: Dict[Any, Any]):
        for key, value in data.items():
            self.set(key, value)

    def clear(self) -> None:
        self._data = {}


F = TypeVar("F", bound=Callable[..., Any])
Func = Callable[..., Any]


class CacheKeyError(Exception):
    pass


_cache_keys: Dict[str, str] = {}
_cached_arg_names: Dict[Callable, List[str]] = {}
_cached_default_args: Dict[Callable, Dict[str, Any]] = {}
_cache = Cache()

_CACHE_MISS = object()


def _check_duplicated_cache_key(key: str) -> None:
    canonical_key = re.sub("{[^}]*}", "{__exp__}", key)

    existing_key = _cache_keys.get(canonical_key)
    if existing_key:
        raise CacheKeyError(
            f"Duplicate cache key: {key}, existing key: {existing_key}"
        )
    else:
        _cache_keys[canonical_key] = key


def _get_default_args(func: Callable) -> Dict[str, Any]:
    defaults: Dict[str, Any] = {}
    spec = inspect.getfullargspec(func)

    if not spec.defaults:
        _cached_default_args[func] = defaults
        return defaults

    offset = len(spec.args) - len(spec.defaults)

    for idx, default_value in enumerate(spec.defaults):
        arg_name = spec.args[idx + offset]
        defaults[arg_name] = default_value

    _cached_default_args[func] = defaults
    return defaults


def _interpolate_str(
    fmt: str,
    func: Func,
    inst: Any,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    arg_values = args
    if inst is not None:
        arg_values = (inst,) + args  # instance -> self

    try:
        arg_names = _cached_arg_names[func]
    except KeyError:
        _cached_arg_names[func] = arg_names = inspect.getfullargspec(func)[0]

    try:
        default_args = _cached_default_args[func]
    except KeyError:
        default_args = _get_default_args(func)
        _cached_default_args[func] = default_args

    context = default_args
    # e.g. {'self': <instance>}
    context.update(dict(zip(arg_names, arg_values)))
    context.update(kwargs)

    return fmt.format(**context)


def memo(key: str) -> Callable[[F], F]:
    _check_duplicated_cache_key(key)

    @decorator
    def wrapper(
        func: Callable,
        inst: Optional[Any],
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
    ) -> Any:
        interpolated_key = _interpolate_str(key, func, inst, args, kwargs)

        cached_value = _cache.get(interpolated_key, default=_CACHE_MISS)
        if cached_value is not _CACHE_MISS:
            return cached_value

        value = func(*args, **kwargs)
        _cache.set(interpolated_key, value)
        return value

    return wrapper
