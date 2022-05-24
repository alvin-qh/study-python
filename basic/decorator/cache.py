import inspect
import re
from typing import Any, Callable, Dict, Iterable, Optional, Set, Tuple

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


# 用于判断一个 Key 是否被缓存的 Set 集合
_cache_keys: Set[str] = set()

# 缓存函数参数名, 加快获取函数参数过程的效率
# 以函数对象为 Key, 参数列表为 Value
_cached_arg_names: Dict[Callable, Tuple[str, ...]] = {}

# 保存函数参数和默认值的字典
_cached_default_args: Dict[Callable, Dict[str, Any]] = {}

# 缓存
_cache = Cache()


def _check_duplicated_cache_key(key: str) -> None:
    """
    判断 Key 是否已经被使用过

    如果 Key 中包含形如 `{x}`, `{y}` 这类的占位符, 则统一替换为 `{__exp__}` 后进行查找.
    也就是说 `demo_{x}_{y}` 和 `demo_{a}_{b}` 被认为是重复的字符串

    Args:
        key (str): Key 值

    Raises:
        KeyError: 抛出 Key 已经被使用过异常
    """
    # 将 key 参数 中 {} 内的内容替换为 {__exp__}
    canonical_key = re.sub("{[^}]*}", "{__exp__}", key)

    # 判断 canonical_key 是否重复
    if canonical_key in _cache_keys:
        raise KeyError(
            f"Duplicate cache key: {key}, existing key: {key}"
        )

    # 将 canonical_key 值保持, 用于后续检查
    _cache_keys.add(canonical_key)


def _get_default_args(func: Callable) -> Dict[str, Any]:
    """
    获取一个函数的默认参数列表

    Args:
        func (Callable): 函数对象

    Returns:
        Dict[str, Any]: 函数对象的参数列表
    """
    defaults: Dict[str, Any] = {}

    # 获取函数参数的参数和参数默认值
    spec = inspect.getfullargspec(func)
    # 如果函数有默认参数值
    if spec.defaults:
        # 获取默认参数值的偏移量
        # Python 规定默认参数必须位于函数参数列表的末尾, 所以 offset 值为参数列表中默认参数开始的位置
        offset = len(spec.args) - len(spec.defaults)

        # 获取参数列表
        arg_names = spec.args

        # 遍历函数的默认参数
        for idx, default_value in enumerate(spec.defaults):
            # 从参数列表中获取默认参数的参数名
            arg_name = arg_names[idx + offset]
            # 保持默认参数
            defaults[arg_name] = default_value

    return defaults


def _interpolate_str(
    fmt: str,
    func: F,
    inst: Any,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    """
    通过函数的参数和值格式化给定字符串

    通过获取 `func` 的参数名列表, 参数值列表和默认参数值列表, 组成 {参数名, 参数值} 的字典对象.
    以该字典对象对 `fmt` 参数进行字符串格式化, 得到一个作为缓存 key 的字符串.

    例如, 对于函数 `def demo(a: int, b: Optional[str]=None)` 来说
    - Key 为 `demo_{a}_{b}`, 若参数 `a` 为 `1`, 则返回 `demo_1_None`

    对于方法 `def demo(self, a: int, b: Optional[str]=None)` 来说
    - Key 为 `demo_{self.id}_{a}_{b}`, 若 `self.id` 为 `100`, 参数 `a` 为 1,
    则返回 `demo_100_1_None`

    Args:
        fmt (str): 格式化字符串
        func (F): 目标函数
        inst (Any): func 函数如果是全局函数, 则为 `None`, 如果是类方法, 则为类对象
        args (Tuple[Any, ...]): 顺序传参值列表
        kwargs (Dict[str, Any]): 命名传参值字典

    Returns:
        str: 格式化结果, 可作为 `func` 函数调用缓存 Key
    """
    arg_values = args

    # 如果 inst 参数不为 None, 则将其作为 self 参数使用
    if inst is not None:
        # 将 inst 参数作为 self 参数, 放到参数值列表第一位
        arg_values = (inst,) + args

    try:
        # 尝试根据函数对象从缓存中获取函数参数名列表
        arg_names = _cached_arg_names[func]
    except KeyError:
        # 缓存未命中, 获取该函数的参数名列表
        arg_names = _cached_arg_names[func] = inspect.getfullargspec(func).args

    try:
        # 尝试根据函数对象从缓存中获取函数的默认参数
        default_args = _cached_default_args[func]
    except KeyError:
        # 缓存未命中, 获取该函数的默认参数
        default_args = _cached_default_args[func] = _get_default_args(func)

    # 函数参数字典, 初始为默认参数名和参数值
    context = default_args
    # 增加列表方式传入的实际参数名和参数值 (可能会覆盖部分默认参数)
    context.update(dict(zip(arg_names, arg_values)))
    # 增加命名方式传入的实际参数名和参数值 (可能会覆盖部分默认参数)
    context.update(kwargs)

    return fmt.format(**context)


# 通过 @decorator 装饰器返回的代理函数类型
DelegateFn = Callable[
    [
        F, Optional[Any],
        Tuple[Any, ...],
        Dict[str, Any]
    ],
    Any,
]


def memo(key: str) -> DelegateFn:
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
