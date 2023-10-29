from typing import Tuple

import pytest
from _pytest.fixtures import SubRequest  # noqa


@pytest.mark.parametrize(
    argnames="test_input, expected",
    argvalues=[("3 + 5", 8), ("2 + 4", 6), ("6 * 9", 54)],
    ids=["test1", "test2", "test3"]
)
def test_parametrize_func(test_input: str, expected: int) -> None:
    """
    参数化:
        通过 `mark.parametrize` 可以为测试指定一组参数, 并依次传入测试函数进行测试
        有几个参数, 就会执行几次测试函数

    本例中:
        - `test_input` 和 `expected` 为两个参数的名称
        - `test_input` 参数依次为: `3 + 5`, `2 + 4` 和 `6 * 9`
        - `expected` 参数依次为: `8`, `6`, `54`

    参数 `ids` 用于表示每次测试, 便于阅读测试报告
    """
    assert eval(test_input) == expected


@pytest.mark.parametrize(
    argnames="a, b, result",
    argvalues=[
        (1, 2, 3),
        (4, 5, 9),
    ]
)
class TestParamterize:
    """
    参数化也可以应用于测试类, 对类中的所有方法起作用
    """

    def test_parametrize_method(self, a: int, b: int, result: int) -> None:
        assert a + b == result


@pytest.mark.parametrize(
    argnames="a, b, result",
    argvalues=[
        (1, 2, 3),
        pytest.param(4, 5, 9, marks=pytest.mark.skip)
    ]
)
def test_parametrize_with_skip(a: int, b: int, result: int) -> None:
    """
    参数化的值可以用 `pytest.param` 产生, 此时可以传入 `marks`, 对这一组参数的测试用例进行标记
    `skip`, `skipif`, `xpass`, `xfail` 等标记均可以使用
    """
    assert a + b == result


NINE_NINE = [[m * n for m in range(1, n + 1)] for n in range(1, 10)]


@pytest.mark.parametrize("a", [1, 2, 3])
@pytest.mark.parametrize("b", [4, 5, 6])
def test_parametrize_multi_parameter(a: int, b: int) -> None:
    """
    多个参数化装饰器, 传入参数组成笛卡尔积
    本例测试笛卡尔积参数, 并从99乘法表中匹配答案
    """
    assert a * b == NINE_NINE[b - 1][a - 1]


@pytest.fixture
def parametrize_fixture(request: SubRequest) -> Tuple[int, int]:
    """
    `request.param` 表示通过该 `fixture` 传入的参数, 即依次为: `1`, `2`, `3`
    """
    # 返回一个二元组
    return request.param, request.param ** 2


@pytest.mark.parametrize("parametrize_fixture", [1, 2, 3], indirect=True)
def test_parametrize_fixture(parametrize_fixture: Tuple[int, int]):
    """
    参数化可以和 `fixture` 结合使用, 即传入 `fixture` 作为参数. 参数化的参数值会依次传给 `fixture`,
    实际传入测试函数的参数为 `fixture` 的返回值

    此时 `parametrize_fixture_single` 作为参数化的名称, 同时也表示名为
    `parametrize_fixture_single` 的 `fixture`

    `indirect = True`, 表示 "参数间接传递", 即通过 `fixture` 来进行传参
    """
    assert (
        parametrize_fixture[0] * parametrize_fixture[0]
        ==
        parametrize_fixture[1]
    )


@pytest.fixture
def parametrize_fixture_multiple(request: SubRequest) -> Tuple[int, int]:
    """
    此时 `request.param` 为一个字典, 依次为:

    ```json
    {
        "a": 100,
        "b": 200,
        "c": 300,
    },
    {
        "a": 1000,
        "b": 2000,
        "c": 3000,
    }
    ```
    """
    return request.param["a"] + request.param["b"], request.param["c"]


@pytest.mark.parametrize(
    "parametrize_fixture_multiple",
    [
        {"a": 100, "b": 200, "c": 300},
        {"a": 1000, "b": 2000, "c": 3000},
    ],
    indirect=True,
)
def test_parametrize6(parametrize_fixture_multiple: Tuple[int, int]) -> None:
    """
    传递给 `fixture` 的参数可以为一个字典
    """
    assert parametrize_fixture_multiple[0] == parametrize_fixture_multiple[1]


@pytest.fixture
def parametrize_fixture_param1(request: SubRequest) -> int:
    """
    传递给 `request.param` 的参数依次为:

    ```json
    {
        "a": 100,
        "b": 200
    }, {
        "a": 1000,
        "b": 2000
    }
    ```
    """
    a = request.param["a"]
    b = request.param["b"]
    return a + b


@pytest.fixture
def parametrize_fixture_param2(request: SubRequest) -> int:
    """
    传递给 `request.param` 的参数依次为: `300`, `3000`
    """
    return request.param


@pytest.mark.parametrize(
    "parametrize_fixture_param1, parametrize_fixture_param2",
    [
        (
            {
                "a": 100,
                "b": 200,
            },
            300,
        ),
        (
            {
                "a": 1000,
                "b": 2000,
            },
            3000,
        ),
    ],
    indirect=True
)
def test_parametrize7(
    parametrize_fixture_param1: int,
    parametrize_fixture_param2: int,
) -> None:
    """
    可以传递多个 `fixture` 作为参数化参数
    """
    assert parametrize_fixture_param1 == parametrize_fixture_param2
