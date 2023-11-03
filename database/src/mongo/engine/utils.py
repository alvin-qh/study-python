from functools import wraps
from typing import Any, Callable

from mongoengine import get_db


def run_once(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = getattr(func, "_called_once", Ellipsis)
        if result is Ellipsis:
            result = func(*args, **kwargs)
            setattr(func, "_called_once", result)

        return result

    return wrapper


@run_once
def clear_db() -> None:
    db = get_db()
    for coll in db.list_collection_names():
        db[coll].drop()


@run_once
def ensure_indexes() -> None:
    db = get_db()
    for coll in db.list_collection_names():
        db[coll].ensure_indexes()
