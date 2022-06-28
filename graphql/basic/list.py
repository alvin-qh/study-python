from typing import List as ListType
from typing import Literal

from graphene import List, NonNull, ObjectType, ResolveInfo, Schema, String


class Query(ObjectType):
    """
    演示 `List` 类型使用

    对应的 GraphQL 定义如下:

    ```
    type Query {
        items(start: String!, end: String!): [String!]!
    }
    ```
    """
    items = List(
        NonNull(String),  # 相当于 String!
        start=String(required=True),
        end=String(required=True),
        required=True,  # 相当于 [String!]!
    )

    @staticmethod
    def resolve_items(
        parent: Literal[None],
        info: ResolveInfo,
        start: str,
        end: str,
    ) -> ListType[str]:
        """
        解析 `items` 字段

        Args:
            start (str): 返回数组的起始字符
            end (str): 返回数组的结束字符

        Returns:
            ListType[str]: 返回从起始字符到结束字符的列表集合
        """
        return [chr(c) for c in range(ord(start), ord(end) + 1)]


"""
定义 schema 对象, 对应的 GraphQL 定义为

```
schema {
    query: Query
}
```
"""
schema = Schema(query=Query)
