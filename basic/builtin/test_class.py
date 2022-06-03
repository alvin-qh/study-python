from typing import List

_dir = dir()


def test_dir_function_and_method() -> None:
    """
    `dir` 有如下几个作用
    - 在全局位置调用时, 返回一个包含所有全局变量 (包含全局魔法变量) 名称的集合
    - 在局部位置使用时, 返回包含局部变量名称的集合
    """
    # 确认
    assert "List" in _dir
    # 此时
    assert "a" not in dir()

    a = 100
    assert "a" in dir()

    class A:
        def __init__(self) -> None:
            self._name = "Alvin"

        def get_name(self) -> str:
            return self._name

        @property
        def name(self) -> str:
            return self._name

    a = A()
    # 验证指定的方法和属性包含在 dir 函数返回的集合中
    assert "__init__" in dir(a)
    assert "get_name" in dir(a)
    assert "name" in dir(a)

    class B:
        def __dir__(self) -> List[str]:
            """
            可以通过 `__dir__` 魔法方法指定 dir 函数返回的结果

            Returns:
                List[str]: _description_
            """
            return ["a", "b", "c"]

    b = B()
    # 验证 dir 函数返回的结果
    assert dir(b) == ["a", "b", "c"]
