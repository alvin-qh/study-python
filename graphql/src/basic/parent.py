"""`parent` 参数

Graphene 中的各类方法, 往往要传递一个 `parent` 参数 (例如: resolve 方法或 mutation 方法)

`parent` 参数表示 "上一级解析对象", 即:

当查询顶级字段时 (即定义在 Query 类型中的字段), 第一级解析对象的 `parent` 参数为 `None` 或
从 `schema.execute` 函数的 `root` 参数传递

当解析某字段的下级字段时, `parent` 参数表示的为该查询字段的上一级字段实例, 例如:

```python
class Foo(ObjectType):
    name = String(required=True)

    @staticmethod
    def resolve_name(parent: "Foo", info: ResolveInfo) -> str:
        ...
```

这段代码的含义是: 当要解析 `name` 字段时, 一定存在上一级对 `foo` 字段的解析, 即:

```python
class Query(ObjectType):
    foo = Field(Foo, required=True)

    def resolve_foo(parent: Literal[None], info: ResolveInfo) -> Foo:
        ...
```

所以 `resolve_foo` 返回的对象将作为 `resolve_name` 的 `parent` 参数
"""

from typing import Optional

from graphene import Field, ObjectType, ResolveInfo, Schema, String


class Person(ObjectType):
    """定义实体类型

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
    full_name = String(required=True)

    @staticmethod
    def resolve_full_name(parent: "Person", info: ResolveInfo) -> str:
        """解析 `full_name` 字段

        Args:
            parent (Person): 当前对象本身
            splitter (str): 分割符参数

        Returns:
            str: 返回全名
        """
        return f"{parent.first_name}·{parent.last_name}"


class Query(ObjectType):
    """查询实体类型

    对应的 Graphql 定义:

    ```graphql
    type Query {
        person: Person!
    }
    ```
    """

    person = Field(Person, required=True)

    @staticmethod
    def resolve_person(parent: Optional[str], info: ResolveInfo) -> Person:
        """解析 `person` 字段

        Returns:
            parent: `schema.execute` 函数的 `root` 参数值
            Person: 返回查询的 `Person` 实体对象
        """

        if (parent or "").lower() == "alvin":
            return Person(
                first_name="Alvin",
                last_name="Qu",
            )

        return Person(
            first_name="Emma",
            last_name="Yua",
        )


"""定义 schema 结构

对应的 GraphQL 定义为

```graphql
schema {
    query: Query
}
```
"""
schema = Schema(query=Query)
