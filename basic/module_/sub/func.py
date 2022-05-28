from typing import Any


def function() -> str:
    """
    测试导入的函数

    Returns:
        _type_: _description_
    """
    # 从当前包导入 version 变量
    # 位于当前包的 __init__.py 文件中
    from . import version
    return version


class Class:
    """
    测试导入的类
    """

    def __init__(self, a: Any) -> None:
        self.a = a


# 测试导入的值
value = value + 1 if "value" in dir() else 0  # type: ignore
