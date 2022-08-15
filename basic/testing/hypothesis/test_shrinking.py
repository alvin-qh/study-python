from typing import Any

from hypothesis import strategies as st


def test_strategies_mapping_single_value() -> None:
    """
    `SearchStrategy` 类型的 `map` 方法可以将假设的值进行转换
    """
    # 假设一个整数值, 通过 map 方法转为字符串类型
    r: Any = (
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
    r = (
        st.lists(st.integers(  # 假设一个列表, 列表元素为整数类型
            min_value=1,
            max_value=100,
        ))
        .map(sorted)  # 列表转换为排序后的列表
        .example()  # 产生假设结果
    )

    # 确认假设值为一个列表对象
    assert isinstance(r, list)

    # 确认假设的列表有序
    n = r[0]
    for i in range(1, len(r)):
        assert n < r[i]
        n = r[i]


def test_strategies_filter() -> None:
    r = st.integers().filter(lambda n: n > 100).example()
    assert isinstance(r, int)
