from typing import Literal

from graphene import ID, Field, ObjectType, ResolveInfo, Schema, String


class User(ObjectType):
    """
    定义实体对象

    对应的 GraphQL 定义为

    ```
    type User {
        id: ID!
        name: String!
    }
    ```
    """

    id = ID(required=True)  # id 字段, required 表示非空字段
    name = String(required=True)  # 姓名字段


# 实体类的数据集
dataset = {
    1: User(id=1, name="Alvin"),
    2: User(id=2, name="Emma"),
    3: User(id=3, name="Lucy"),
}


class Query(ObjectType):
    """
    定义查询类型

    对应的 GraphQL 定义为

    ```
    type Query {
        user(id: ID!): User!
    }
    ```
    """

    # 定义一个实体类型字段
    user = Field(User, id=ID(required=True), required=True)

    @staticmethod
    def resolve_user(parent: Literal[None], info: ResolveInfo, id: int) -> User:
        """
        解析 `user` 字段

        Args:
            id (int): 查询参数, 实体的 id

        Returns:
            User: User 类型对象
        """
        return dataset[int(id)]


"""
定义 schema 结构, 指定根查询对象

对应的 GraphQL 定义为

```
schema {
    query: Query
}
```
"""
schema = Schema(query=Query)
