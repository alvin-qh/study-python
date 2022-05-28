import pytest

from .cases import add, exception


def test_assertion() -> None:
    """
    测试基本断言
    """
    assert add(1, 2) == 3


def test_assertion_with_prompt() -> None:
    """
    测试断言失败后的提示文本
    """
    assert add(1, 2) == 3, "Test prompt"


def test_exception_assertion() -> None:
    """
    检查是否抛出异常的断言
    """
    with pytest.raises(ValueError, match=".*Example error.*") as excinfo:
        exception()

    assert excinfo.type == ValueError
    assert str(excinfo.value) == "Example error"


def test_assume_assertion1() -> None:
    """
    测试多重断言: 使用多重断言表示, 无论之前的断言是否失败, 整个测试用例都会执行完毕, 之后统一输出结果
    """
    pytest.assume(1 + 2 == 3)  # type: ignore
    pytest.assume(1 + 2 == 3)  # type: ignore
    pytest.assume(1 + 2 == 3)  # type: ignore


def test_assume_assertion2() -> None:
    """
    通过 with 语句使用多重断言
    """
    with pytest.assume:  # type: ignore
        assert 1 + 2 == 3

    with pytest.assume:  # type: ignore
        assert 1 + 2 == 3

    with pytest.assume:  # type: ignore
        assert 1 + 2 == 3
