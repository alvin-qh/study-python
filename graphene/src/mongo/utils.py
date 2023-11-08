from functools import wraps
from typing import Any, Callable, Optional, Tuple, Union

from graphql import GraphQLError
from graphql_relay import from_global_id, to_global_id
from mongoengine import Document, get_db

# 没有记录返回值时的默认值
_NoReturnValue = object()


def run_once(func: Callable[..., Any]) -> Callable[..., Any]:
    """让目标函数只执行一次的装饰器

    Args:
        - `func` (`Callable[..., Any]`): 目标函数

    Returns:
        `Callable[..., Any]`: 目标函数
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # 从目标函数的 `_called_once` 属性中获取缓存的上次运行的返回值
        result = getattr(func, "_called_once", _NoReturnValue)
        if result is _NoReturnValue:
            # 如果尚未缓存, 则调用一次函数
            result = func(*args, **kwargs)

            # 将函数返回值缓存在函数对象的 `_called_once` 属性上
            setattr(func, "_called_once", result)

        return result

    return wrapper


@run_once
def clear_db() -> None:
    """清除数据库下的所有文档集合"""
    db = get_db()
    for coll in db.list_collection_names():
        db[coll].drop()


@run_once
def ensure_indexes() -> None:
    """重建当前数据库中所有文档的索引"""
    db = get_db()
    for coll in db.list_collection_names():
        db[coll].ensure_indexes()


def make_global_id(doc: Document) -> str:
    """根据 mongo 文档对象创建 Graphql 统一 id

    Args:
        - `doc` (`Document`): mongo 文档对象

    Returns:
        `str`: 统一 id
    """
    # 利用文档类名称作为类型计算统一 id
    return to_global_id(doc.__class__.__name__, doc.id)


def parse_global_id(global_id: str, doc: Optional[Document] = None) -> Tuple[str, str]:
    """从 Graphql 统一 id 还原其类型以及实际 id

    Args:
        - `global_id` (`str`): 统一 id
        - `doc` (`Optional[Document]`, optional): mongo 文档对象, 如果传递该参数, 则会验证统一 id 中的类型部分. Defaults to `None`.

    Raises:
        `GraphQLError`: 如果传递了 `doc` 参数, 且统一 id 中的类型和文档类型不匹配, 则抛出此异常

    Returns:
        `Tuple[str, str]`: 返回 `(原始 id, 类型)` 两部分值
    """
    # 解析统一 id, 返回原始信息
    src = from_global_id(global_id)

    # 如果原始信息中的文档类型不匹配, 则抛出异常
    if doc and src.type != doc.__class__.__name__:
        raise GraphQLError("invalid_global_id_type")

    # 返回原始 id 和类型
    return src.id, src.type


def make_cursor(cursor: Union[int, str]) -> str:
    """产生游标标识字符串, 为一个 Graphql 统一 id

    Args:
        - `cursor` (`Union[int, str]`): 游标原始值

    Returns:
        `str`: 转换为统一 id 的游标值
    """
    # 以 `__cursor__` 为类型, 编码原始游标值
    return to_global_id("__cursor__", cursor)


def parse_cursor(global_id: str) -> str:
    """解析编码为统一 id 的游标标识

    Args:
        - `global_id` (`str`): 统一 id 值

    Raises:
        `GraphQLError`: 如果解析后类型不正确, 则抛出此异常

    Returns:
        `str`: 解码后的原始游标值
    """
    id_ = from_global_id(global_id)
    if id_.type != "__cursor__":
        # 如果类型不正确, 则抛出异常
        raise GraphQLError("invalid_cursor_type")

    return id_.id
