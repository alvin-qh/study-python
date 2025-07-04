from _pytest.fixtures import SubRequest
from pytest import fixture

from basic.testing import Step

step = Step()


def finalize() -> None:
    """一个终结器函数, 用于 `fixture` 设置"""

    step.finish()


@fixture
def addfinalizer_fixture(request: SubRequest) -> str:
    """可以通过 `fixture` 的 `request` 参数为其添加一个 `finalizer`

    `finalizer` 表示一个测试结束后执行的 hook 方法
    """
    step.start()

    # 添加 finalize 函数到 request 中, 此时当测试结束后,
    # finalize 函数会被执行一次
    request.addfinalizer(finalize)
    return "addfinalizer_fixture"


def test_addfinalizer_fixture(addfinalizer_fixture: str) -> None:
    """测试为 `fixture` 添加 `finalizer` 钩子函数

    Args:
        - `addfinalizer_fixture` (`str`): `addfinalizer_fixture` 函数的返回值
    """
    assert addfinalizer_fixture == "addfinalizer_fixture"
    assert step.state == "started"


def teardown_module() -> None:
    """在当前模块中所有测试结束后调用"""

    assert step.state == "finished"
