from typing import Callable, Generator

from pytest import fixture, mark


class FixtureName:
    """
    记录 fixture 名称的类
    """

    def __init__(self) -> None:
        """
        初始化
        """
        self._fixture_name = ""

    def set(self, fixture: Callable) -> None:
        """
        保存 fixture 的名称

        Args:
            fixture (Callable): fixture 函数
        """
        self._fixture_name = fixture.__name__

    @property
    def value(self) -> str:
        """
        获取保存的 fixture 名称

        Returns:
            str: 保存的 fixture 名称
        """
        return self._fixture_name

    def clear(self) -> None:
        """
        清除保存的 fixture 名称
        """
        self._fixture_name = ""


fixture_name = FixtureName()


@fixture
def default_name_fixture() -> Generator[str, None, None]:
    """
    @fixture 装饰器在默认情况下, 以其修饰的函数名为 fixture 名称

    Yields:
        Generator[None, None, None]: 返回传入测试函数的参数值
    """

    # 存储当前 fixture 的名称
    fixture_name.set(default_name_fixture)

    # 执行测试函数, 返回参数值为当前 fixture 的名称
    yield default_name_fixture.__name__

    # 清空存储的 fixture 名称
    fixture_name.clear()


@fixture(name="specify_named_fixture")
def specify_named_fixture() -> Generator[str, None, None]:
    """
    @fixture 装饰器的 name 参数可以设定该 fixture 的名称

    Yields:
        Generator[str, None, None]: 返回传入测试函数的参数值
    """

    # 存储当前 fixture 的名称
    fixture_name.set(specify_named_fixture)

    # 执行测试函数, 返回参数值为当前 fixture 的名称
    yield specify_named_fixture.__name__

    # 清空存储的 fixture 名称
    fixture_name.clear()


@mark.usefixtures("default_name_fixture")
def test_default_name_fixture() -> None:
    """
    测试名称为 default_name_fixture 的 fixture

    usefixtures 装饰器表示该测试要使用的 fixture 名称
    """
    assert fixture_name.value == "default_name_fixture"


def test_specify_named_fixture(specify_named_fixture: str) -> None:
    """
    测试名称为 specify_named_fixture 的 fixture

    Args:
        specify_named_fixture (str): specify_named_fixture 函数的返回值
    """
    assert specify_named_fixture == "specify_named_fixture"
    assert fixture_name.value == "specify_named_fixture"
