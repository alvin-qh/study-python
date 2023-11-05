from enum import Enum
from typing import Any, Type

from mongoengine.base import BaseField
from mongoengine.fields import StringField


class EnumField(BaseField):
    def __init__(self, enum: Type[Enum], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.enum = enum

    @staticmethod
    def _get_value(enum: Any) -> Any:
        return enum.value if hasattr(enum, "value") else enum

    def to_python(self, value: Any) -> Any:
        return self.enum(super().to_python(value))

    def to_mongo(self, value: Any) -> Any:
        return self._get_value(value)

    def prepare_query_value(self, op: Any, value: Any) -> Any:
        return super().prepare_query_value(op, self._get_value(value))

    def validate(self, value: Any, clean: bool = True) -> Any:
        return super().validate(self._get_value(value))

    def _validate(self, value: Any, **kwargs: Any) -> Any:
        return super()._validate(self.enum(self._get_value(value)), **kwargs)


class StringEnumField(EnumField, StringField):
    def __set__(self, instance: Any, value: Any) -> None:
        super().__set__(instance, value)
