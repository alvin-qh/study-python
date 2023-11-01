from typing import Literal

from graphene import Mutation, ObjectType, ResolveInfo, Schema, String


class RootQuery(ObjectType):
    """定义查询类型

    对应的 GraphQL 定义为:

    ```
    type RootQuery {
        hello(name: String = "World"): String
        goodbye: String
    }
    ```
    """

    # name 为查询时所需传递的参数; default_value 是参数的默认值
    hello = String(name=String(default_value="World"))  # 定义查询字段
    goodbye = String()  # 定义查询字段

    @staticmethod
    def resolve_hello(parent: Literal[None], info: ResolveInfo, name: str) -> str:
        """解析 `hello` 字段

        Args:
            name (str): 查询参数

        Returns:
            str: 查询结果
        """
        return f"Hello {name}"

    @staticmethod
    def resolve_goodbye(parent: Literal[None], info: ResolveInfo) -> str:
        return "See you again"


class CreateSomething(Mutation):
    """定义某个具体更改操作的 `Mutation` 类型"""

    class Arguments:
        """更新操作的参数定义"""

        # 定义字符串类型的 arg 参数
        arg = String(required=True)

    # 更新完成后返回字符串值
    Output = String(required=True)

    @staticmethod
    def mutate(parent: Literal[None], info: ResolveInfo, arg: str) -> str:
        return arg + " mutated"


class RootMutation(ObjectType):
    """定义变更类型, 用于创建, 更新, 删除实体对象

    对应的 GraphQL 定义为:

    ```
    type RootMutation {
        createSomething(arg: String!): String!
    }
    ```
    """

    # 创建用户的字段
    create_something = CreateSomething.Field()


class RootSubscription(ObjectType):
    """定义订阅类型"""

    field = String()

    @staticmethod
    async def subscribe_field(parent: Literal[None], info: ResolveInfo) -> None:
        """Empty 定义字段"""


"""定义 schema 结构, 指定根查询对象

对应的 GraphQL 定义为

```
schema {
    query: RootQuery
    mutation: RootMutation
    subscription: RootSubscription
}
```
"""
schema = Schema(
    query=RootQuery,  # 设置根查询类型
    mutation=RootMutation,  # 设置根更新类型
    subscription=RootSubscription,  # 设置根订阅类型
)
