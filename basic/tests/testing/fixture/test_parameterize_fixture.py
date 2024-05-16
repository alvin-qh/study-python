from typing import cast

from _pytest.fixtures import SubRequest
from pytest import fixture

param_seq = {
    "case1",
    "case2",
    "case3",
}


@fixture(ids=["c1", "c2", "c3"], params=param_seq)
def param_fixture(request: SubRequest) -> str:
    """`@fixture` 装饰器的参数 params 可以指定一个集合

    其中:
    - 集合的数量表示测试被调用的次数
    - 每次测试使用的值通过 request.param 参数传入

    返回 `request.param` 的值, 表示每次测试时, 该 `fixture` 函数表示的值, 依次为 `"case1"`, `"case2"` 和 `"case3"`

    另一个参数 `ids` 用于表示每次测试的编号, 便于阅读测试报告

    Args:
        `request` (`SubRequest`): 测试参数

    Returns:
        `str`: 每次测试从集合中选取的一个值
    """
    return cast(str, request.param)


def test_param_fixture(param_fixture: str) -> None:
    """`param_fixture` 表示调用 `param_fixture` 函数

    该测试方法会被重复调用 `3` 次, `param_fixture` 参数的值分别为 `"case3"`, `"case2"` 和 `"case1"`

    Args:
        - `param_fixture` (`str`): `param_fixture` 函数每次的返回值
    """
    assert param_fixture in param_seq
