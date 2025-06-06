from typing import Any


class Foo:
    """测试排序的类"""

    def __init__(self, name: str, value: Any) -> None:
        """初始化对象

        Args:
            - `name` (`str`): 名称
            - `value` (`Any`): 值
        """
        self.name = name
        self.value = value

    def __eq__(self, other: Any) -> bool:
        """判断两个对象是否相等, 用于测试中断言等值判断

        Args:
            - `other` (`Any`): 被比较的对象

        Returns:
            `bool`: 两个对象是否相等
        """
        if not isinstance(other, Foo):
            return False

        return self.name == other.name and self.value == other.value
