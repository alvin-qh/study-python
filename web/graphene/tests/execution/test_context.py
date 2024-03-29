from execution.context import schema
from graphene import Context


def test_context_as_dict() -> None:
    """
    测试查询的上下文
    """

    # 定义查询结构
    query = """
        query {
            name  # 查询 Query 类型的 name 字段
        }
    """

    # 执行查询, 传递上下文对象
    r = schema.execute(
        query,
        # 以字典为上下文对象, 对应 resolve_name 方法中 info.context 的值
        context=dict(name="Alvin"),
    )

    # 确认查询正确
    assert r.errors is None
    # 确认查询结果
    assert r.data == {"name": "Alvin"}


def test_context_type() -> None:
    """
    测试查询的上下文
    """

    # 定义查询结构
    query = """
        query {
            name  # 查询 Query 类的 name 字段
        }
    """

    # 执行查询, 传递上下文对象
    r = schema.execute(
        query,
        # 以 Context 对象为上下文对象, 对应 resolve_name 方法中 info.context 的值
        context=Context(name="Alvin"),
    )

    # 确认查询正确
    assert r.errors is None
    # 确认查询结果
    assert r.data == {"name": "Alvin"}
