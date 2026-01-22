import os
from os import path
from typing import Generator, cast

from _pytest.fixtures import SubRequest
from pytest import fixture, mark


@fixture
def addfinalizer_fixture(request: SubRequest) -> str:
    """可以通过 `fixture` 的 `request` 参数为其添加一个 `finalizer`

    `finalizer` 表示一个测试结束后执行的 hook 方法
    """

    def _on_finalize() -> None:
        print("'_on_finalize' function is called")

    # 添加 finalize 函数到 request 中, 此时当测试结束后,
    # finalize 函数会被执行一次
    request.addfinalizer(_on_finalize)
    return "addfinalizer_fixture"


def test_addfinalizer_fixture(addfinalizer_fixture: str) -> None:
    """测试为 `fixture` 添加 `finalizer` 钩子函数

    Args:
        - `addfinalizer_fixture` (`str`): `addfinalizer_fixture` 函数的返回值
    """
    assert addfinalizer_fixture == "addfinalizer_fixture"


@fixture
def get_test_information_fixture(
    request: SubRequest,
) -> Generator[tuple[str, str], None, None]:
    """可以通过 `fixture` 的 `request` 参数获取当前测试的 `SubRequest` 对象

    通过 `SubRequest` 对象, 可以获取目标测试函数的信息, 包括测试函数 id 以及测试函数名称等等
    """
    # 获取当前测试的 nodeid
    nodeid = request.node.nodeid
    # 获取当前测试的 name
    node_name = request.node.originalname  # pyright: ignore[reportAttributeAccessIssue]

    yield (nodeid, node_name)


@mark.usefixtures("addfinalizer_fixture")
def test_get_test_information(get_test_information_fixture: tuple[str, str]) -> None:
    """测试获取当前测试的 `request` 对象, 并通过

    注意: 这里使用了 `@mark.usefixtures` 装饰器, 当前测试会使用 `addfinalizer_fixture` 这个 fixture,
    否则当测试执行完毕后, `teardown_module` 函数会报错

    Args:
        - `get_test_information_fixture` (`tuple[str, str]`): `get_test_information_fixture` 函数的返回值
    """
    # 获取当前测试的 nodeid 和 name
    nodeid, node_name = get_test_information_fixture

    # 确认 nodeid 为 ‘当前文件名 (相对路径)::当前测试函数名’
    assert nodeid == f"{path.relpath(__file__, os.getcwd())}::test_get_test_information"

    # 确认 name 为当前测试函数名
    assert node_name == "test_get_test_information"


param_seq = [
    "case1",
    "case2",
    "case3",
]


@fixture(ids=["c1", "c2", "c3"], params=param_seq)
def param_fixture(request: SubRequest) -> str:
    """`@fixture` 装饰器的参数 params 可以指定一个集合

    其中:
    - 集合的数量表示测试被调用的次数
    - 每次测试使用的值通过 request.param 参数传入

    当 `@fixture` 装饰器指定 `params` 参数时, pytest 会自动生成一个测试集合, 并按照 `params` 参数的顺序依次调用测试函数,
    在测试函数内部, 可通过 `request.param` 参数获取本次传递的测试参数

    `@fixture` 装饰器的另一个参数 `ids` 用于表示每次测试的编号, 便于阅读测试报告

    本例中, 测试函数返回 `request.param` 的值, 表示每次测试时, 该 `fixture` 函数表示的值,
    依次为 `"case1"`, `"case2"` 和 `"case3"`

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


@fixture
def passing_arguments_fixture(request: SubRequest) -> tuple[str, int]:
    """通过 `request` 参数获取测试参数

    在执行 `test_passing_arguments_fixture` 测试函数时, 会通过测试函数的 `@mark.parametrize` 装饰器指定传递到 fixture 函数的参数,
    在当前 fixture 函数中, 通过 `request.param` 参数获取传递的参数

    Args:
        - `request` (`SubRequest`): 测试参数

    Returns:
        `tuple[str, int]`: 返回到测试函数的值
    """
    return request.param["name"], request.param["value"]


@mark.parametrize(
    "passing_arguments_fixture", [{"name": "number", "value": 100}], indirect=True
)
def test_passing_arguments_fixture(passing_arguments_fixture: tuple[str, int]) -> None:
    """测试向 fixture 函数传入参数

    pytest 中, 无法为 fixture 函数的参数列表直接传入参数, 但可以通过 fixture 函数的 `request` 参数来传递参数, 方法如下:

    - 在测试函数上使用 `@mark.parametrize` 装饰器, 并为装饰器传递如下参数:
        - `argnames`: 必须为当前测试函数的 fixture 参数的名称
        - `argvalues`: 要传递的参数, 为一个对象
        - `indirect`: 必须为 `True`, 表示要转发参数

    Args:
        - `passing_arguments_fixture` (`tuple[str, int]`): `passing_arguments_fixture` 函数的返回值
    """
    name, value = passing_arguments_fixture

    assert name == "number"
    assert value == 100
