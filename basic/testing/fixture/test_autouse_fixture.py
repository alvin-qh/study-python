from typing import Generator

from pytest import fixture


class Step:
    """
    步骤记录类
    """

    def __init__(self) -> None:
        """
        初始化, 表示未开始
        """
        self._state = "not start"

    def running(self) -> None:
        """
        初始化, 表示执行中
        """
        self._state = "running"

    def finished(self) -> None:
        """
        初始化, 表示已结束
        """
        self._state = "finished"

    @property
    def state(self) -> str:
        """
        获取状态

        Returns:
            str: 状态值
        """
        return self._state


# 记录步骤的对象
step = Step()


@fixture(autouse=True)
def autouse_fixture() -> Generator[None, None, None]:
    """
    使用 autouse = True
    表示该 fixture 会被自动调用, 无需通过参数引用该 fixture
    """
    assert step.state == "not start"

    # 先将状态设置为 running
    step.running()

    # 执行目标测试函数
    yield

    # 目标测试函数结束后, 将状态设置为 finished
    step.finished()


def test_autouse_fixture() -> None:
    """
    autouse_fixture 函数会被在每个测试中自动调用
    """

    # 确认此时的状态
    assert step.state == "running"


def teardown_module() -> None:
    """
    当前模块中所有测试执行结束后执行
    """

    # 所有测试执行结束后的状态
    assert step.state == "finished"
