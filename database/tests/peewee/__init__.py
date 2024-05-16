from typing import Optional, TypeVar

_T = TypeVar("_T")


def non_none(val: Optional[_T]) -> _T:
    assert val is not None
    return val


__all__ = [
    "non_none",
]
