from pytest import fixture, mark


class FixtureVisitorCount:
    """
    记录各 fixture 被调用的次数
    """

    def __init__(self) -> None:
        """
        初始化对象
        """
        # 为字典字段设置初始值
        self._counter = {
            "function": 0,
            "class": 0,
            "module": 0,
            "session": 0
        }

    def increase(self, scope: str) -> None:
        """
        增加调用次数

        Args:
            scope (str): 调用的 `fixture` 范围
        """
        self._counter[scope] += 1

    def __getitem__(self, scope: str) -> int:
        """
        获取指定 `scope` 的 `fixture` 调用次数

        Args:
            scope (str): `fixture` 的 `scope` 名称

        Returns:
            int: 调用次数
        """
        return self._counter[scope]


counter = FixtureVisitorCount()


@fixture(scope="function")
def function_scope_fixture() -> str:
    """
    参数 `scope="function"` 表示所有的测试函数 (包括测试类方法) 在执行前会执行一次该
    `fixture`. 测试类中的方法无法通过参数访问到这类 `fixture`

    Returns:
        str: 返回字符串表示当前 `fixture` 的 `scope`
    """
    counter.increase("function")
    return "function"


@fixture(scope="class")
def class_scope_fixture() -> str:
    """
    参数 `scope="class"` 表示所有的测试函数和测试类中的测试方法在执行前会执行一次该
    `fixture`. 所有的测试函数和测试类中的方法均能通过参数访问到这类 `fixture`

    Returns:
        str: 返回字符串表示当前 `fixture` 的 `scope`
    """
    counter.increase("class")
    return "class"


@fixture(scope="module")
def module_scope_fixture() -> str:
    """
    参数 `scope="module"`, 每个模块会执行一次.
    所有的测试函数和测试类中的方法均能通过参数访问到这类 `fixture`

    Returns:
        str: 返回字符串表示当前 `fixture` 的 `scope`
    """
    counter.increase("module")
    return "module"


@fixture(scope="session")
def session_scope_fixture() -> str:
    """
    参数 "scope="session"", 每次测试只会执行一次.
    所有的测试函数和测试类中的方法均能通过参数访问到这类 `fixture`

    Returns:
        str: 返回字符串表示当前 `fixture` 的 `scope`
    """
    counter.increase("session")
    return "session"


@mark.repeat(2)
def test_function_scope(
    function_scope_fixture: str,
    class_scope_fixture: str,
    module_scope_fixture: str,
    session_scope_fixture: str
) -> None:
    """
    在测试函数内, 可以访问 `"session"`, `"module"`, `"class"` 以及 `"function"`
    所有范围内的 `fixture`

    Args:
        function_scope_fixture (str): `scope` 为 `"function"` 的 `fixture` 函数
                                      返回值
        class_scope_fixture (str): `scope` 为 `"class"` 的 `fixture` 函数返回值
        module_scope_fixture (str): `scope` 为 `"module"` 的 `fixture` 函数返回值
        session_scope_fixture (str): `scope` 为 `"session"` 的 `fixture` 函数返回值
    """
    assert function_scope_fixture == "function"
    assert class_scope_fixture == "class"
    assert module_scope_fixture == "module"
    assert session_scope_fixture == "session"


class TestScope:
    """
    测试在类中测试的情况
    """

    @mark.repeat(2)
    def test_class_scope(
        self,
        function_scope_fixture: str,
        class_scope_fixture: str,
        module_scope_fixture: str,
        session_scope_fixture: str
    ) -> None:
        """
        在测试函数内, 可以访问 `"function"`, `"session"`, `"module"`
        以及 `"class"` 范围内的 `fixture`

        Args:
            function_scope_fixture (str): `scope` 为 `"function"`
            的 `fixture` 函数返回值
            class_scope_fixture (str): `scope` 为 `"class"` 的 `fixture` 函数
                                       返回值
            module_scope_fixture (str): `scope` 为 `"module"` 的 `fixture` 函数
                                        返回值
            session_scope_fixture (str): `scope` 为 `"session"`
            的 `fixture` 函数返回值
        """
        assert function_scope_fixture == "function"
        assert class_scope_fixture == "class"
        assert module_scope_fixture == "module"
        assert session_scope_fixture == "session"


def teardown_module():
    """
    当前模块的所有测试结束后调用, 校验所有 `fixture` 调用的次数
    """

    # test_function_scope 和 test_class_scope 各调用 2 次
    assert counter["function"] == 4

    # test_function_scope 调用2次, TestScope 类调用 1 次, 共调用 3 次
    assert counter["class"] == 3

    # 当前模块调用 1 次
    assert counter["module"] == 1

    # 一共调用 1 次
    assert counter["session"] == 1
