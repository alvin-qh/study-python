GLOBAL_VALUE = 100

_dir = dir()


def test_dir_function_and_method() -> None:
    """`dir` 有如下几个作用

    - 在全局位置调用时, 返回一个包含所有全局变量 (包含全局魔法变量) 名称的集合
    - 在局部位置使用时, 返回包含局部变量名称的集合
    """
    # 确认包含全局导入符号 `json`
    assert "GLOBAL_VALUE" in _dir

    # 确认不包含全局变量 a
    assert "a" not in dir()

    # 定义具备变量 `n` 并确定符号 `n` 会随后包含在 `dir` 函数的返回结果中
    n = 100  # noqa
    assert "n" in dir()

    class DemoClass:
        def __init__(self, name: str) -> None:
            self._name = name

        def get_name(self) -> str:
            return self._name

        @property
        def name(self) -> str:
            return self._name

    c = DemoClass("Alvin")

    # 验证指定的方法和属性包含在 dir 函数返回的集合中
    assert "__init__" in dir(c)
    assert "_name" in dir(c)
    assert "get_name" in dir(c)
    assert "name" in dir(c)


def test_override_dir_magic_member() -> None:
    """覆盖 dir 函数

    通过 `__dir__` 魔法方法, 可以覆盖 dir 函数的默认行为.
    """

    class DemoClass:
        def __dir__(self) -> list[str]:
            """可以通过 `__dir__` 魔法方法指定 dir 函数返回的结果

            Returns:
                list[str]: _description_
            """
            return ["a", "b", "c"]

    c = DemoClass()
    # 验证 dir 函数返回的结果
    assert dir(c) == ["a", "b", "c"]
