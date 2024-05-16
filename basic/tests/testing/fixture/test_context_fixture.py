from typing import Generator, cast

from pytest import fixture
from testing.fixture import Context

USERNAME = "Alvin"
ORG_CODE = "alvin.edu"


@fixture
def context() -> Generator[Context, None, None]:
    """通过 `fixture`, 在对应的测试中执行指定的代码, 并将返回值作为测试函数的参数

    Yields:
        `Generator[Context, None, None]`: 上下文对象
    """
    with Context(username=USERNAME, org_code=ORG_CODE) as ctx:
        yield ctx


@fixture
def org_code(context: Context) -> str:
    """定义 `fixture`

    该 `fixture` 的参数是名为 `context` 的 `fixture`, 可以通过在一个 `fixture` 中传入另一个 `fixture` 作为参数的方式进行连锁调用

    Args:
        - `context` (`Context`): `context` 函数的返回值

    Returns:
        `str`: `context` 对象中 `org_code` 的值
    """
    return cast(str, context.org_code)


def test_context(context: Context) -> None:
    """在测试中使用和某个 `fixture` 函数同名的参数

    此时 `pytest` 框架会自动调用对应的 `fixture` 函数, 并用函数返回值作为参数值

    Args:
        `context` (`Context`): context 函数的返回值
    """
    assert context.username == USERNAME
    assert context.org_code == ORG_CODE


def test_org_code(org_code: str) -> None:
    """调用名为 `org_code` 的 fixture

    Args:
        `org_code` (`str`): `org_code` 函数的返回值
    """
    assert org_code == ORG_CODE
