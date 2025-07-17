def expand_list[T](lst: list[T], size: int) -> list[T]:
    """把列表集合扩展到指定的长度

    Args:
        `lst` (`List[T]`): 列表集合对象
        `size` (`int`): 指定的长度

    Returns:
        `List[T]`: 长度扩展到 `size` 后的集合
    """
    while len(lst) < size:
        lst *= 2

    return lst[:size]
