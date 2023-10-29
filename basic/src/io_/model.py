from typing import Any


class PersonModel:
    """
    测试序列化的类
    """

    def __init__(self, id_: int, name: str, message: str) -> None:
        """
        初始化对象
        """
        self.id = id_
        self.name = name
        self.message = message

    def __eq__(self, other: Any) -> Any:
        """
        比较两个对象是否相同

        Args:
            other (Any): 要比较的对象

        Returns:
            bool: 当前对象和要比较的对象是否相同
        """
        # 判断当前对象和待比较对象类型是否相同
        if self.__class__ != other.__class__:
            return False

        # 判断两个对象字段值是否相同
        return (
            self.id == other.id
            and self.name == other.name
            and self.message == other.message
        )
