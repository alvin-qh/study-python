from typing import Any, Optional, cast


def non_none[T](val: Optional[T]) -> T:
    """如果传入的值为 `None`, 则抛出 `ValueError` 异常

    Args:
        - `val` (`T`): 待检查的值

    Returns:
        `T`: 待检查的值

    Raises:
        - `ValueError`: 如果传入的值为 `None`
    """
    if val is None:
        raise ValueError("Value cannot be None")
    return val


def col(name: Any) -> str:
    return cast(str, name)
