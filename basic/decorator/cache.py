import inspect
import re
from typing import (Any, Callable, Dict, Iterable, List, Optional, Set, Tuple,
                    TypeVar)

from wrapt import decorator


class Cache:
    """
    定义缓存类
    """
    _data: Dict[str, Any]

    def __init__(self) -> None:
        """
        构造器, 初始化缓存存储 Dict 对象
        """
        self._data = {}

    def keys(self) -> Iterable[str]:
        """
        获取缓存中所有的 Key 值集合

        Returns:
            Iterable[str]: Key 值集合的迭代器对象
        """
        return self._data.keys()

    def items(self) -> Iterable[Tuple[str, Any]]:
        """
        获取缓存中所有的 Key/Value 键值对

        Returns:
            Iterable[Tuple[str, Any]]: 键值对迭代器对象
        """
        return self._data.items()

    def set(self, key: str, value: Any) -> None:
        """
        设置缓存内容

        Args:
            key (str): 缓存项的 Key 值
            value (Any): 缓存项的值
        """
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        根据 Key 值获取对应的缓存项值

        Args:
            key (str): 缓存项的 Key 值
            default (Any, optional): 缓存项默认值, 即当缓存项不存在时返回的值. Defaults to None.

        Returns:
            Any: 缓存项的值
        """
        return self._data.get(key, default)

    def delete(self, key: str) -> None:
        """
        根据 Key 值删除指定的缓存项

        Args:
            key (str): 缓存项的 Key 值
        """
        try:
            del self._data[key]
        except AttributeError:
            pass

    def delete_many(
        self,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
    ) -> None:
        """
        根据缓存项的 Key 值的前缀和后缀删除对应的缓存项

        Args:
            prefix (Optional[str], optional): 缓存项 Key 值得前缀. Defaults to None.
            suffix (Optional[str], optional): 缓存项 key 值得后缀. Defaults to None.
        """
        for key in list(self.keys()):
            if (
                (prefix and key.startswith(prefix)) or
                (suffix and key.endswith(suffix))
            ):
                self.delete(key)

    def populate(self, items: Dict[Any, Any]) -> None:
        """
        将一批 Key/Value 值设置到缓存中

        Args:
            items (Dict[Any, Any]): 包含若干 Key/Value 的字典对象
        """
        for key, value in items.items():
            self.set(key, value)

    def clear(self) -> None:
        """
        清空缓存内容
        """
        self._data = {}


# 定义一个函数类型, 任意参数且返回 Any
F = Callable[..., Any]

# 定义 Cache 未命中时返回的缺省值
_CACHE_MISS = object()


# 用于
_cache_keys: Set[str] = set()

#
_cached_default_args: Dict[Callable, Dict[str, Any]] = {}
# 缓存函数参数名, 加快获取函数参数过程的效率
# 以函数对象为 Key, 参数列表为 Value
_cached_arg_names: Dict[Callable, List[str]] = {}


# 缓存对象, 保存
_cache = Cache()


def _check_duplicated_cache_key(key: str) -> None:
    canonical_key = re.sub("{[^}]*}", "{__exp__}", key)

    existing_key = _cache_keys.get(canonical_key)
    if existing_key:
        raise KeyError(
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
    func: F,
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
    context.update(dict(zip(arg_names, arg_values)))
    context.update(kwargs)

    return fmt.format(**context)


def memo(key: str) -> Callable[[F, Optional[Any], Tuple[Any, ...], Dict[str, Any]], Any]:
    _check_duplicated_cache_key(key)

    @decorator
    def wrapper(
        func: F,
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
