import base64
from datetime import date, datetime, timedelta
from decimal import Decimal as DecimalType
from typing import Any

from graphene import (ID, Boolean, Date, DateTime, Decimal, Float, Int,
                      ObjectType, ResolveInfo, Scalar, String, Time)

from graphql.language import ast


class Stuff(ObjectType):
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


class Calendar(ObjectType):
    one_week_from = Date(required=True, date=Date(required=True))
    one_hour_from = DateTime(required=True, datetime=DateTime(required=True))
    one_minute_from = Time(required=True, time=Time(required=True))

    @staticmethod
    def resolve_one_week_from(parent: "Calendar", info: ResolveInfo, date: Date) -> Date:
        return date + timedelta(weeks=1)

    @staticmethod
    def resolve_one_hour_from(parent: "Calendar", info: ResolveInfo, datetime: DateTime) -> DateTime:
        return datetime + timedelta(hours=1)

    @staticmethod
    def resolve_one_minute_from(parent: "Calendar", info: ResolveInfo, time: Time) -> Time:
        time = datetime.combine(date(1, 1, 1), time)
        return (time + timedelta(minutes=1)).time()


class Calculator(ObjectType):
    add_one_to = Decimal(required=True, decimal=Decimal(required=True))

    @staticmethod
    def resolve_add_one_to(parent: "Calculator", info: ResolveInfo, decimal: Decimal) -> Decimal:
        return decimal + DecimalType("1")


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
