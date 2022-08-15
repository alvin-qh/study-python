from typing import List, Tuple, cast

from hypothesis import strategies as st


def test_strategies_mapping_single_value() -> None:
    """
    `SearchStrategy` 类型的 `map` 方法可以将假设的值进行转换
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
    测试 `SearchStrategy` 类型的 `map` 方法对列表假设的转换
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
    过滤符合条件的假设值 (简单类型)

    `hypothesis` 框架每次会假设一组值, 并在每次调用时返回其中的一个, `filter` 的作用
    就是从这一组值中挑选符合条件的那些
    """
    r = st.integers().filter(lambda n: n > 100).example()

    # 确保假设值为 int 类型
    assert isinstance(r, int)

    # 确认假设值符合条件
    assert r > 100


def test_strategies_filter_complex_value() -> None:
    """
    过滤复杂结构

    本例中, 假设一组 `Tuple` 类型, 过滤出其中元素 1 小于元素 2 的结果
    """
    r: Tuple[int, int] = (
        st.tuples(  # 假设一个 Tuple 对象
            st.integers(min_value=1, max_value=100),  # 假设其中的元素 1
            st.integers(min_value=1, max_value=100),  # 假设其中的元素 2
        )
        .filter(lambda x: x[0] < x[1])  # type: ignore # 过滤假设, 条件是元素 1 的值小于元素 2
        .example()
    )

    # 确保假设结果的类型
    assert isinstance(r, tuple)

    # 确保过滤起作用
    assert r[0] < r[1]
