import base64
from calendar import calendar
from datetime import date, datetime, timedelta
from decimal import Decimal as DecimalType
from typing import Any, Dict, Literal

from graphene import (ID, Boolean, Date, DateTime, Decimal, Field, Float, Int,
                      JSONString, ObjectType, ResolveInfo, Scalar, Schema,
                      String, Time)

from graphql.language import ast


class Stuff(ObjectType):
    """
    graphene 框架内置了所有 GraphQL 基本类型, 包括:
    - `ID`
    - `String`
    - `Int`
    - `Float`
    - `Boolean`

    对应的 GraphQL 定义如下:

    ```
    type Stuff {
        id: ID!
        name: String
        serialNo: Int!
        price: Float!
        lts: Boolean!
    }
    ```
    """
    # ID 类型表示一个唯一标识, 是一个整数或者字符串
    id = ID(required=True)

    # String 类型表示字符串
    name = String(required=False, default_value="No name")

    # Int 类型表示整数
    serial_no = Int(required=True)

    # Float 类型表示一个浮点数
    price = Float(required=True)

    # Boolean 类型表示一个布尔值
    lts = Boolean(required=True)


class Calendar(ObjectType):
    """
    演示 `Date`, `DateTime` 和 `Time` 三个表示日期时间的类型

    - `Date` 对应 Python 的 `datetime.date` 类型, 表示一个日期
    - `DateTime` 对应 Python 的 `datetime.datetime` 类型, 表示一个日期时间, 格式采用 ISO-8601
    - `Time` 对应 Python 的 `datetime.time` 类型, 表示一个时间

    对应的 GraphQL 定义如下:

    ```
    type Calendar {
        oneWeekFrom(date: Date!): Date!
        oneHourFrom(datetime: DateTime!): DateTime!
        oneMinuteFrom(time: Time!): Time!
    }
    ```
    """
    # 表示日期类型的字段
    one_week_from = Date(required=True, date=Date(required=True))

    # 表示日期时间类型的字段
    one_hour_from = DateTime(required=True, datetime=DateTime(required=True))

    # 表示时间类型的字段
    one_minute_from = Time(required=True, time=Time(required=True))

    @staticmethod
    def resolve_one_week_from(parent: "Calendar", info: ResolveInfo, date: Date) -> Date:
        """
        解析 `one_week_from` 字段, 根据传入的 `date` 参数, 返回其加上一周后的日期

        Args:
            date (Date): 传入的日期参数

        Returns:
            Date: 给参数日期加上一周后的日期
        """
        return date + timedelta(weeks=1)

    @staticmethod
    def resolve_one_hour_from(parent: "Calendar", info: ResolveInfo, datetime: DateTime) -> DateTime:
        """
        解析 `one_hour_from` 字段, 根据传入的 `datetime` 参数, 返回其加上一小时后的日期时间

        Args:
            datetime (DateTime): 传入的日期时间参数

        Returns:
            DateTime: 给参数日期时间加上一小时后的日期时间
        """
        return datetime + timedelta(hours=1)

    @staticmethod
    def resolve_one_minute_from(parent: "Calendar", info: ResolveInfo, time: Time) -> Time:
        """
        解析 `one_minute_from` 字段, 根据传入的 `time` 参数, 返回其加上一分钟后的时间

        Args:
            datetime (DateTime): 传入的时间参数

        Returns:
            DateTime: 给参数时间加上一分钟后的日期时间
        """
        time = datetime.combine(date(1, 1, 1), time)
        return (time + timedelta(minutes=1)).time()


class Calculator(ObjectType):
    add_one_to = Decimal(required=True, decimal=Decimal(required=True))

    @staticmethod
    def resolve_add_one_to(parent: "Calculator", info: ResolveInfo, decimal: Decimal) -> Decimal:
        return decimal + DecimalType("1")


class JSONObject(ObjectType):
    _json = {
        "name": "Alvin",
        "age": 42,
    }

    update_json_key = JSONString(
        key=String(required=True),
        value=String(required=True),
        required=True,
    )

    @staticmethod
    def resolve_update_json_key(
        parent: "JSONObject", info: ResolveInfo, key: str, value: Any,
    ) -> Dict[str, Any]:
        json = JSONObject._json

        json[key] = value
        return json


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


class EncodedId(ObjectType):
    increment_encoded_id = Base64(required=True, value=Base64(required=True))

    @staticmethod
    def resolve_increment_encoded_id(
        parent: "EncodedId", info: ResolveInfo, value: str
    ) -> int:
        return int(base64) + 1


class Query(ObjectType):
    stuff = Field(Stuff, required=True)
    calendar = Field(Calendar, required=True)

    @staticmethod
    def resolve_stuff(parent: Literal[None], info: ResolveInfo) -> Stuff:
        return Stuff(
            id=1,
            name="Music Speaker",
            serial_no=101,
            price=269.9,
            lts=True,
        )

    @staticmethod
    def resolve_calendar(parent: Literal[None], info: ResolveInfo) -> Calculator:
        return Calendar()


"""
定义 schema 对象, 对应的 GraphQL 定义为

```
schema {
    query: Query
}
```
"""
schema = Schema(query=Query)
