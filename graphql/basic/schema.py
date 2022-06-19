from typing import Literal

from graphene import Mutation, ObjectType, ResolveInfo, Schema, String


class RootQuery(ObjectType):
    """
    定义查询类型
    """
    # name 为查询时所需传递的参数; default_value 是参数的默认值
    hello = String(name=String(default_value="World"))  # 定义查询字段
    goodbye = String()  # 定义查询字段

    @staticmethod
    def resolve_hello(parent: Literal[None], info: ResolveInfo, name: str) -> str:
        """
        解析 `hello` 字段

        Args:
            name (str): 查询参数

        Returns:
            str: 查询结果
        """
        return f"Hello {name}"

    @staticmethod
    def resolve_goodbye(parent: Literal[None], info: ResolveInfo) -> str:
        return "See you again"


class RootMutation(Mutation):
    """
    定义更新类型
    """

    class Arguments:
        arg = String()

    field = String()

    @staticmethod
    def mutate(parent: Literal[None], info: ResolveInfo, arg: str) -> None:
        pass


class RootSubscription(ObjectType):
    """
    定义订阅类型
    """
    field = String()

    @staticmethod
    async def subscribe_field(parent: Literal[None], info: ResolveInfo) -> None:
        pass


# 定义 schema 对象, 指定根查询对象
schema = Schema(
    query=RootQuery,   # 设置根查询类型
    mutation=RootMutation,  # 设置根更新类型
    subscription=RootMutation,  # 设置根订阅类型
)
