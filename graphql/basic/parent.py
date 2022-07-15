from typing import Literal

from graphene import Argument, Field, ObjectType, ResolveInfo, Schema, String


class Person(ObjectType):
    """
    定义实体类型

    对应的 Graphql 定义为:

    ```graphql
    type Person {
        firstName: String!
        lastName: String!
        fullName(splitter: String): String!
    }
    ```
    """
    # 第一个名字
    first_name = String(required=True)
    # 第二个名字
    last_name = String(required=True)
    # 全名
    full_name = String(
        splitter=Argument(String, default_value="·"),  # 全名中间的分割符
        required=True,
    )

    @staticmethod
    def resolve_full_name(parent: "Person", info: ResolveInfo, splitter: str) -> str:
        """
        解析 `full_name` 字段

        Args:
            parent (Person): 当前对象本身
            splitter (str): 分割符参数

        Returns:
            str: 返回全名
        """
        return f"{parent.first_name}{splitter}{parent.last_name}"


class Query(ObjectType):
    """
    查询实体类型

    对应的 Graphql 定义:

    ```graphql
    type Query {
        person: Person!
    }
    ```
    """
    person = Field(Person, required=True)

    @staticmethod
    def resolve_person(parent: Literal[None], info: ResolveInfo) -> Person:
        """
        解析 `person` 字段

        Returns:
            Person: 返回查询的 `Person` 实体对象
        """
        return Person(
            first_name="Alvin",
            last_name="Qu",
        )


"""
定义 schema 结构

对应的 GraphQL 定义为

```graphql
schema {
    query: Query
}
```
"""
schema = Schema(query=Query)
