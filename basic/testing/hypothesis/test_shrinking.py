from typing import List, Tuple

from hypothesis import strategies as st


def test_strategies_mapping_single_value() -> None:
    """
    `SearchStrategy` 类型的 `map` 方法可以将假设的值进行转换.
    `map` 方法的参数为一个 `Callable[[Any], Any]` 类型的函数, 即传入一个原始参数, 返回
    转换结果

    本例演示对单个值进行转换
    """
    # 假设一个整数值, 通过 map 方法转为字符串类型
    r = (
        st.integers(min_value=1, max_value=100)  # 假设一个整数值
        .map(lambda n: str(n))  # 将假设的整数值转为字符串类型
        .example()  # 产生假设值结果
    )

    # 确认假设结果为字符串类型
    assert isinstance(r, str)

    # 确认假设结果为整数转换为字符串
    assert str(int(r)) == r


def test_strategies_mapping_list() -> None:
    """
    `SearchStrategy` 类型的 `map` 方法可以将假设的值进行转换.
    `map` 方法的参数为一个 `Callable[[Any], Any]` 类型的函数, 即传入一个原始参数, 返回
    转换结果

    本例演示对集合类型或复杂类型值进行转换
    """
    # 假设一个列表对象, 并对其假设结果进行排序
    r: List[int] = (
        st.lists(st.integers(  # type: ignore # 假设一个列表, 列表元素为整数类型
            min_value=1,
            max_value=100,
        ))
        .map(sorted)  # type: ignore # 列表转换为排序后的列表
        .example()  # 产生假设结果
    )

    # 确认假设值为一个列表对象
    assert isinstance(r, list)

    # 确认假设的列表有序
    n = r[0]
    for i in range(1, len(r)):
        assert n <= r[i]
        n = r[i]


def test_strategies_filter_simple_value() -> None:
    """
    `SearchStrategy` 类型的 `filter` 的可以从这一组值中挑选符合条件的结果

    本例中从一组假设的整数值中过滤出一个大于 `100` 的值
    """
    r = st.integers().filter(lambda n: n > 100).example()

    # 确保假设值为 int 类型
    assert isinstance(r, int)

    # 确认假设值符合条件
    assert r > 100


def test_strategies_filter_complex_value() -> None:
    """
    `SearchStrategy` 类型的 `filter` 的可以从这一组值中挑选符合条件的结果

    本例中假设一组 `Tuple` 类型, 过滤出其中元素 `1` 小于元素 `2` 的结果
    """
    r: Tuple[int, int] = (
        st.tuples(  # 假设一个 Tuple 对象
            st.integers(min_value=1, max_value=100),  # 假设其中的元素 1
            st.integers(min_value=1, max_value=100),  # 假设其中的元素 2
        )
        .filter(  # type: ignore # 过滤假设, 条件是元素 1 的值小于元素 2
            lambda x: x[0] < x[1],
        )
        .example()
    )

    # 确保假设结果的类型
    assert isinstance(r, tuple)

    # 确保过滤起作用
    assert r[0] < r[1]


def test_strategies_chain_together() -> None:
    """
    `SearchStrategy` 类型的 `flatmap` 方法和 `map` 方法类似, 只是 `flatmap` 返回
    的是一个新的 `SearchStrategy` 对象, 可以进一步通过 `map`, `filter` 方法进行链式
    操作

    本例中通过一个假设的整数值, 产生与之数量匹配的列表项, 进行排序后转为 `Tuple` 类型
    """
    r: Tuple[int, ...] = (
        st.integers(min_value=1, max_value=5)  # 假设一个整数
        # 以假设的整数为长度假设一个列表
        .flatmap(lambda n: st.lists(st.integers(), min_size=n, max_size=n))
        .map(sorted)  # type:ignore # 列表排序
        .map(tuple)  # type: ignore # 列表转为 Tuple
        .example()
    )

    # 确保结果为 Tuple 类型
    assert isinstance(r, tuple)

    # 确保结果有序
    n: int = r[0]
    for i in range(1, len(r)):
        assert n <= r[i]
        n = r[i]
