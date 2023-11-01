from typing import Any, Dict, Literal, Union, cast

from graphene import Context, ObjectType, ResolveInfo, Schema, String


class Query(ObjectType):
    """定义查询类

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
        """解析 `name` 字段

        Returns:
            str: 字段值
        """
        ctx: Union[Dict[str, Any], Context] = info.context

        if isinstance(ctx, Dict):
            return cast(str, ctx.get("name"))

        if isinstance(ctx, Context):
            return ctx.name  # type: ignore

        raise ValueError("")


"""定义 schema 结构, 指定根查询对象

对应的 GraphQL 定义为

```
schema {
    query: Query
}
```
"""
schema = Schema(query=Query)
