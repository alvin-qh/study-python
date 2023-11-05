from functools import wraps
from typing import Any, Callable, Optional, Tuple, Union

from graphql_relay import from_global_id, to_global_id
from mongoengine import Document, get_db

from graphql import GraphQLError

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
    return to_global_id(doc.__class__.__name__, doc.id)


def parse_global_id(global_id: str, doc: Optional[Document] = None) -> Tuple[str, str]:
    id_ = from_global_id(global_id)
    if doc and id_.type != doc.__class__.__name__:
        raise GraphQLError("invalid_global_id_type")

    return id_.id, id_.type


def make_cursor(cursor: Union[int, str]) -> str:
    return to_global_id("cursor", cursor)


def parse_cursor(global_id: str) -> str:
    id_ = from_global_id(global_id)
    if id_.type != "cursor":
        raise GraphQLError("invalid_cursor_type")

    return id_.id
