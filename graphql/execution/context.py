from typing import Literal

from graphene import ObjectType, ResolveInfo, Schema, String


class Query(ObjectType):
    """
    定义查询类

    对应的 GraphQL 定义如下:

    ```
    type Query {
        name: String
    }
    ```
    """
    # 定义 name 字段
    name = String()

    @staticmethod
    def resolve_name(parent: Literal[None], info: ResolveInfo) -> str:
        """
        解析 `name` 字段

        Returns:
            str: 字段值
        """
        return info.context.get("name")


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
