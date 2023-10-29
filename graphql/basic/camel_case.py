"""
Graphql 中的命名规范

Graphql 默认使用 Camel Case (驼峰) 规范命名字段, 而 Python 采用下划线规范进行命名

Graphene 内置了一套规则, 可以自动将下划线命名转换为驼峰命名, 例如:

```
user_name => userName
```

这个过程默认是自动的, 除非对其进行显式的关闭

是否使用名称转换是有 `Schema` 类型的 `auto_camelcase` 参数控制

```python
schema = Schema(query=Query, auto_camelcase=True) # 默认开启名称转换
```

一般情况下, 这个转换规则工作的很好, 无需干预, 但一些特殊情况 (例如名称中确实存在下划线) 下, 需要指定名称避免转换

```python
class Foo(ObjectType):
    b_name = String(name="b_name", required=True)
```

此时, 字段名称不会被转换为 `bName`, 而会保持 `b_name`
"""

from typing import Literal

from graphene import Field, ObjectType, ResolveInfo, Schema, String


class Person(ObjectType):
    """
    定义实体类型用来验证字段名称转化规则

    标准的 GraphQL 要求使用 "驼峰" 法对字段进行命名, Python 一般使用 "下划线" 分割的规则对字段命名.
    为了符合标准, graphene 框架采用了自动转换的规则, 将下划线命名的字段自动转为驼峰命名方式, 规则为:
    删除下划线, 并将下划线后的第一个字母改为大写字母, 例如 `user_name` 会转换为 `userName`.

    驼峰是 GraphQL 的规范命名, 一般情况下无需对其进行修改. 但 `Schema` 类型的构造参数中仍包含了
    `auto_camelcase` 参数, 如果为 `False`, 则 graphene 框架不再自行修改实体字段名称.

    另外, 对于特殊字段, 如需特殊命名, 则字段的 `Scalars` 类型构造器包含了 `name` 参数, 可以对字段
    进行特殊命名

    对应的 GraphQL 定义为:

    ```
    type Person {
        lastName: String
        _other_name_: String
    }
    ```
    """
    # 定义字段, 在查询时, 该字段名称会被自动转化为 lastName, 驼峰命名法
    last_name = String()

    # 指定字段的 name 值, 在查询时, 必须以 _other_name_ 作为字段名
    other_name = String(name="_other_name_")


class Query(ObjectType):
    """
    定义根查询类型

    对应的 GraphQL 定义为:

    ```
    type Query {
        person: Person!
    }
    ```
    """
    # 定义要查询的字段, 为 Person 类型
    person = Field(Person, required=True)

    @staticmethod
    def resolve_person(parent: Literal[None], info: ResolveInfo) -> Person:
        """
        解析 `person` 字段, 返回 `Person` 类型的实体对象

        Returns:
            Student: 获取一个 `Person` 类型的实体对象
        """
        # 定义 Person 实体对象并返回
        return Person(last_name="Qu", other_name="Alvin")


"""
定义 schema 对象, auto_camelcase 为 True (默认值) 表示遵循自动转驼峰的命名规则

对应的 GraphQL 定义为

```
schema {
    query: Query
}
```
"""
schema = Schema(query=Query, auto_camelcase=True)
