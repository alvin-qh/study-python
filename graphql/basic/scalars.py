import base64
from typing import Any

from graphene import (ID, Boolean, Date, DateTime, Float, Int, ObjectType,
                      Scalar, String)

from graphql.language import ast


class Base64(Scalar):
    @staticmethod
    def serialize(s: Any) -> str:
        """
        Serialize the result return from "resolve_xxx" function
        """
        return base64.b64encode(str(s).encode()).decode()

    @staticmethod
    def parse_literal(node):
        """
        Parse the literal from query string
        """
        if not isinstance(node, ast.StringValue):
            return None

        return Base64.parse_value(node.value)

    @staticmethod
    def parse_value(value):
        """
        Parse the value from query string
        """
        return base64.b64decode(value.encode()).decode()


class Product(ObjectType):
    """
    graphene 框架内置了所有标准类型, 包括:
    - `ID`
    - `String`
    - `Int`
    - `Float`
    - `Boolean`
    - `Date`
    - `Time`
    - `DateTime`
    - `Decimal`
    - `JSONString`, 对应标准中的 `JSON` (或 `Object`) 类型
    """
    id = ID(required=True)
    name = String(required=False, default_value="No name")
    serial_no = Int(required=True)
    price = Float(required=True)
    lts = Boolean(required=True)
    production_date = Date(required=True)
    quality_time = DateTime(required=True)
