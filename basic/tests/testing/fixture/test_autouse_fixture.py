from typing import Generator

from pytest import fixture
from testing import Step

# 记录步骤的对象
step = Step()


@fixture(autouse=True)
def autouse_fixture() -> Generator[None, None, None]:
    """
    使用 `autouse = True` 表示该 `fixture` 会被自动调用,
    无需通过参数引用
    """
    assert step.state == "ready"

    # 先将状态设置为 running
    step.start()

    # 执行目标测试函数
    yield

    # 目标测试函数结束后, 将状态设置为 finished
    step.finish()


def test_autouse_fixture() -> None:
    """
    `autouse_fixture` 函数会被在每个测试中自动调用
    """

    # 确认此时的状态
    assert step.state == "started"


def teardown_module() -> None:
    """
    当前模块中所有测试执行结束后执行
    """

    # 所有测试执行结束后的状态
    assert step.state == "finished"
