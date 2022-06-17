from typing import Literal

from graphene import ObjectType, ResolveInfo, Schema, String


class Query(ObjectType):
    """
    定义查询类
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


# 定义 schema
schema = Schema(query=Query)


def test_context() -> None:
    """
    测试查询的上下文
    """

    # 查询字符串
    query = """
        {
            name  # 对应 Query 类的 name 字段
        }
    """

    # 上下文对象
    context = {
        "name": "Alvin",   # 对应 resolve_name 方法中 info.context 的值
    }

    # 执行查询, 传递上下文对象
    r = schema.execute(query, context=context)

    # 确认查询正确
    assert r.errors is None
    # 确认查询结果
    assert r.data == {
        "name": "Alvin"
    }
