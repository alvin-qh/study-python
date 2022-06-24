import base64
from datetime import date, datetime, timedelta
from decimal import Decimal as DecimalType
from typing import Any, Dict, Literal

import humps
from bson import ObjectId
from graphene import (ID, Boolean, Date, DateTime, Decimal, Field, Float, Int,
                      JSONString, ObjectType, ResolveInfo, Scalar, Schema,
                      String, Time)

from graphql import StringValueNode, ValueNode


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
    def resolve_one_hour_from(
        parent: "Calendar",
        info: ResolveInfo,
        datetime: DateTime,
    ) -> DateTime:
        """
        解析 `one_hour_from` 字段, 根据传入的 `datetime` 参数, 返回其加上一小时后的日期时间

        Args:
            datetime (DateTime): 传入的日期时间参数

        Returns:
            DateTime: 给参数日期时间加上一小时后的日期时间
        """
        return datetime + timedelta(hours=1)

    @staticmethod
    def resolve_one_minute_from(
        parent: "Calendar",
        info: ResolveInfo,
        time: Time,
    ) -> Time:
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
    """
    演示 `Decimal` 大数类型

    对应的 GraphQL 定义如下:

    ```
    type Calculator {
        addOneTo(number: Decimal!): Decimal!
    }
    ```
    """
    # Decimal 类型的字段
    add_one_to = Decimal(required=True, number=Decimal(required=True))

    @staticmethod
    def resolve_add_one_to(
        parent: "Calculator",
        info: ResolveInfo,
        number: Decimal,
    ) -> Decimal:
        """
        解析 `add_one_to` 类型, 对传入的 `Decimal` 类型数值加 `1` 后返回

        Args:
            number (Decimal): 传入的任意 `Decimal` 类型参数

        Returns:
            Decimal: 对传入的参数加 `1` 后返回结果
        """
        return number + DecimalType(1)


class GenericType(Scalar):
    """
    自定义 Scalar 类型, 可以处理泛化类型

    对应的 GraphQL 定义如下:

    ```
    scalar GenericType
    ```
    """

    @staticmethod
    def serialize(value: Any) -> Any:
        """
        将返回客户端的值 (字段值) 序列化成所需的形式

        Args:
            value (Any): 为字段的 `resolve_xxx` 方法返回的结果 (或赋值给字段的值)

        Raises:
            ValueError: 不支持的数据类型

        Returns:
            Any: 返回到客户端的值, 可以为 `str`, `int`, `float`, `boolean` 类型
        """
        # 基本类型和列表集合类型的值, 返回值本身
        if isinstance(value, (str, int, float, bool, tuple, list)):
            return value

        # 字典类型的值, 将字典 key 转换为驼峰命名法后返回字典对象
        if isinstance(value, dict):
            return humps.camelize(value)

        # 对于日期类型的值, 返回 ISO8601 标准格式字符串
        elif isinstance(value, date):
            return value.isoformat()

        # 如果时 ObjectId, 返回字符串
        elif isinstance(value, ObjectId):
            return str(value)

        # 对于无法识别的类型, 抛出异常
        raise ValueError(f"Unable to serialize type: {type(value)}")

    @staticmethod
    def parse_literal(node: ValueNode) -> Any:
        """
        将从发送到服务端的字面量值进行解析

        Args:
            node (ValueNode): 包装字面量的对象

        Returns:
            Any: 返回 `None` 表示本例不支持字面量
        """

    @staticmethod
    def parse_value(value: Any) -> Any:
        """
        将从发送到服务端的值 (参数值) 进行解析

        Args:
            value (Any): 发送到服务端的值, 可以为 `str`, `int`, `float`, `boolean` 类型

        Returns:
            Any: 解析为目标类型后的值
        """
        if isinstance(value, (str, int, float, bool, tuple, list)):
            return value

        return humps.decamelize(value)


class JSONObject(ObjectType):
    """
    演示 `JSONString` json 字符串类型

    对应的 GraphQL 定义如下:

    ```
    type JSONObject {
        updateJsonKey(key: String!, value: GenericType!): JSONString!
    }
    ```
    """

    # 表示原始 json 的字典对象
    _json = {
        "name": "Alvin",
        "age": 42,
    }

    # 表示 JSON 字符串的字段
    update_json_key = JSONString(
        key=String(required=True),  # 表示要修改的 json 的 key 字符串值
        value=GenericType(required=True),  # 表示要修改的 json 的 value 任意值
        required=True,
    )

    @staticmethod
    def resolve_update_json_key(
        parent: "JSONObject", info: ResolveInfo, key: str, value: str,
    ) -> Dict[str, Any]:
        """
        解析 `update_json_key` 字段

        本方法返回类型为一个 `Dict` 字典对象, 但客户端会接收到一个对应的 JSON 字符串

        Args:
            key (str): 要更新的 JSON Key
            value (str): 要更新的 JSON Value 值

        Returns:
            Dict[str, Any]: 返回修改后的 JSON 字典
        """
        # 将原始 json 字典对象进行复制
        json = {**JSONObject._json}

        # 根据参数修改 json 字典对象
        json[key] = value

        # 返回一个 Dict 对象, 客户端接收到一个 json 字符串
        return json


class Base64(Scalar):
    """
    自定义 Scalar 类型

    当默认的 Scalar 类型无法满足要求是, 可以自定义所需的 Scalar 类型

    本例中自定义 `Base64` 类型, 可将客户端上传的 base64 编码解析为字符串, 并将服务端返回的任意类型
    序列化为 base64 字符串

    对应的 GraphQL 定义如下:

    ```
    scalar Base64
    ```
    """

    @staticmethod
    def serialize(value: Any) -> Any:
        """
        将返回客户端的值 (字段值) 序列化成所需的形式

        序列化的结果的类型可以为 `str`, `int`, `float`, `boolean` 类型

        Args:
            value (Any): 为字段的 `resolve_xxx` 方法返回的结果 (或赋值给字段的值)

        Returns:
            Any: 返回到客户端的值, 可以为 `str`, `int`, `float`, `boolean` 类型
        """
        return base64.b64encode(str(value).encode()).decode()

    @staticmethod
    def parse_literal(node: ValueNode) -> Any:
        """
        将从发送到服务端的字面量值进行解析

        Args:
            node (ValueNode): 包装字面量的对象

        Returns:
            Any: 当字面量类型不符合转换条件返回 `None`, 否则返回字面量解析后的值
        """
        # 判断字面量是否为字符串类型
        if not isinstance(node, StringValueNode):
            # 非期待类型, 返回 None, 表示不解析
            return None

        # 解析字面量值
        return Base64.parse_value(node.value)

    @staticmethod
    def parse_value(value: Any) -> Any:
        """
        将从发送到服务端的值 (参数值) 进行解析

        客户端发送的值类型可以为 `str`, `int`, `float`, `boolean` 类型, 本方法将其解析为所需
        的类型

        Args:
            value (Any): 发送到服务端的值, 可以为 `str`, `int`, `float`, `boolean` 类型

        Returns:
            Any: 解析为目标类型后的值
        """
        # 本例中, 只对发送到服务端的字符串类型值进行处理
        if isinstance(value, str):
            return base64.b64decode(value.encode()).decode()

        # 对于非期待的类型, 抛出异常
        raise ValueError(
            f"Invalid type of parsing value, need \"str\", but \"{type(value)}\"")


class EncodedId(ObjectType):
    """
    测试自定义 Scalar 类型
    """
    # 定义 Base64 自定义类型字段
    # 字段值会发送到客户端, 执行 Base64 类型的 serialize 方法
    # 参数值会从客户端发送到服务单, 执行 Base64 类型的 parse_value 方法
    increment_encoded_id = Base64(required=True, value=Base64(required=True))

    @staticmethod
    def resolve_increment_encoded_id(
        parent: "EncodedId",
        info: ResolveInfo,
        value: str,
    ) -> int:
        """
        解析 `increment_encoded_id` 字段, 将传上来的 Base64 值解析为整数, 加 `1` 后返回

        Args:
            value (str): `Base64` 值解析后的结果, 解析调用 `Base64` 类型的 `parse_value` 方法

        Returns:
            int: 返回解析结果加 `1` 的值, 该值会执行 `Base64` 类型的 `serialize` 方法后发送到客户端
        """
        return int(value) + 1


class Query(ObjectType):
    """
    组合上述类型为一个 `Query` 类型的字段

    对应的 GraphQL 定义如下:

    ```
    type Query {
        stuff: Stuff!
        calendar: Calendar!
        calculator: Calculator!
        jsonObject: JSONObject!
        encodedId: EncodedId!
    }
    ```
    """
    stuff = Field(Stuff, required=True)  # Stuff 类型字段
    calendar = Field(Calendar, required=True)  # Calendar 类型字段
    calculator = Field(Calculator, required=True)  # Calculator 类型字段
    json_object = Field(JSONObject, required=True)  # JSONObject 类型字段
    encoded_id = Field(EncodedId, required=True)  # EncodedId 类型字段

    @staticmethod
    def resolve_stuff(parent: Literal[None], info: ResolveInfo) -> Stuff:
        """
        解析 `stuff` 字段
        """
        # 返回 Stuff 类型对象
        return Stuff(
            id=1,
            name="Music Speaker",
            serial_no=101,
            price=269.9,
            lts=True,
        )

    @staticmethod
    def resolve_calendar(parent: Literal[None], info: ResolveInfo) -> Calendar:
        """
        解析 `calendar` 字段
        """
        # 返回 Calendar 类型对象
        return Calendar()

    @staticmethod
    def resolve_calculator(parent: Literal[None], info: ResolveInfo) -> Calculator:
        """
        解析 `calculator` 字段
        """
        # 返回 Calculator 类型对象
        return Calculator()

    @staticmethod
    def resolve_json_object(parent: Literal[None], info: ResolveInfo) -> JSONObject:
        """
        解析 `json_object` 字段
        """
        # 返回 JSONObject 类型对象
        return JSONObject()

    @staticmethod
    def resolve_encoded_id(parent: Literal[None], info: ResolveInfo) -> EncodedId:
        """
        解析 `encoded_id` 字段
        """
        # 返回 EncodedId 类型对象
        return EncodedId()


"""
定义 schema 对象, 对应的 GraphQL 定义为

```
schema {
    query: Query
}
```
"""
schema = Schema(query=Query)
