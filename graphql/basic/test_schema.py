from typing import Any

from graphene import ObjectType, ResolveInfo, Schema, String


class Query(ObjectType):
    """
    定义查询类
    """
    # name 为查询时所需传递的参数; default_value 是参数的默认值
    hello = String(name=String(default_value="World"))  # 定义查询字段
    goodbye = String()  # 定义查询字段

    @staticmethod
    def resolve_hello(parent: Any, info: ResolveInfo, name: str) -> str:
        """
        解析 `hello` 字段

        Args:
            name (str): 查询参数

        Returns:
            str: 查询结果
        """
        return f"Hello {name}"

    @staticmethod
    def resolve_goodbye(parent: Any, info: ResolveInfo) -> str:
        return "See you again"


# 定义 schema 对象, 指定根查询对象
schema = Schema(query=Query)


def test_schema() -> None:
    """
    测试查询
    """
    # 定义查询
    query = """
        {
            hello       # 查询 Query 类型的 hello 字段, 不传递参数
            goodbye     # 查询 Query 类型的 goodbye 字段
        }
    """

    # 执行查询
    r = schema.execute(query)

    # 确保查询正确
    assert r.errors is None
    assert r.data == {
        "hello": "Hello World",
        "goodbye": "See you again"
    }

    # 定义查询
    query = """
        {
            hello(name: "Alvin")  # 查询 hello 字段, 传递参数
            goodbye               # 查询 goodbye 字段
        }
    """

    # 执行查询
    r = schema.execute(query)

    # 确保查询正确
    assert r.errors is None
    assert r.data == {
        "hello": "Hello Alvin",
        "goodbye": "See you again"
    }
