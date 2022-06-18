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
