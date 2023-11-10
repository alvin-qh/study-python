from enum import Enum
from typing import Any, Type

from mongoengine.base import BaseField
from mongoengine.fields import StringField


class EnumField(BaseField):
    """枚举类型 mongo 字段"""

    def __init__(self, enum: Type[Enum], *args: Any, **kwargs: Any) -> None:
        """将 Python 枚举类型包装为 mongo 枚举字段

        Args:
            - `enum` (`Type[Enum]`): Python 枚举类型
        """
        super().__init__(*args, **kwargs)
        self.enum = enum

    @staticmethod
    def _get_value(enum: Any) -> Any:
        """获取 Python 枚举对象的值

        Args:
           - `enum` (`Any`): Python 枚举对象

        Returns:
            `Any`: 枚举对象的值
        """
        return enum.value if hasattr(enum, "value") else enum

    def to_python(self, value: Any) -> Any:
        """将字段值转为 Python 值

        Args:
            - `value` (`Any`): 字段值

        Returns:
            `Any`: `value` 参数值对应的 Python 枚举对象
        """
        return self.enum(super().to_python(value))

    def to_mongo(self, value: Any) -> Any:
        """将枚举对象值转为 mongo 字段值

        Args:
            - `value` (`Any`): Python 枚举对象值

        Returns:
            `Any`: mongo 字段值
        """
        return self._get_value(value)

    def prepare_query_value(self, op: Any, value: Any) -> Any:
        """准备用于查询操作的值

        Args:
            - `op` (`Any`): 查询操作
            - `value` (`Any`): 查询的值

        Returns:
            `Any`: 用于查询操作的值
        """
        return super().prepare_query_value(op, self._get_value(value))

    def validate(self, value: Any, clean: bool = True) -> Any:
        """验证字段值, 确保字段有效且当字段为必填时字段值存在

        Args:
            - `value` (`Any`): 字段值
            - `clean` (`bool`, optional): 是否执行数据清理, 本字段无效. Defaults to `True`.

        Returns:
            `Any`: _description_
        """
        return super().validate(self._get_value(value))

    def _validate(self, value: Any, **kwargs: Any) -> Any:
        return super()._validate(self.enum(self._get_value(value)), **kwargs)


class StringEnumField(EnumField, StringField):
    """值为字符串的枚举字段类型

    该字段类型用于存储如下类型 Python 值

    ```python
    class MyEnum(Enum):
        A = "A"
        B = "B"
    ```

    该字段类型同时具备 `EnumField` 以及 `StringField` 字段类型的特性
    """

    def __set__(self, instance: Any, value: Any) -> None:
        """将 `value` 参数表示的值设置到 `instance` 表示的对象中

        Args:
            - `instance` (`Any`): 目标对象
            - `value` (`Any`): 枚举的字符串值
        """
        super().__set__(instance, value)
