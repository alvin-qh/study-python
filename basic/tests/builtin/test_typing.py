from typing import List, TypeVar

# 定义一个泛型类型, 限制在 int 和 float 两种类型中
T = TypeVar("T", int, float)


def generic_func(val: T) -> List[T]:
    """
    定义一个函数, 参数和返回值为泛型类型

    Args:
        val (T): 泛型参数

    Returns:
        List[T]: 泛型返回值, 类型和参数类型一致
    """
    # 如果返回值列表元素类型和参数类型不一致, 则 mypy 检查会报错
    return [val] * 3


def test_generic_method() -> None:
    """
    测试泛型函数
    """
    # 参数类型和返回值列表元素类型为 int 类型
    assert generic_func(3) == [3, 3, 3]

    # 参数类型和返回值列表元素类型为 float 类型
    assert generic_func(0.1) == [0.1, 0.1, 0.1]

    # 参数类型和返回值列表元素类型为 str 类型, 此时 mypy 会报错
    assert generic_func("A") == ["A", "A", "A"]  # type: ignore
