from .list import schema


def test_list() -> None:
    """
    测试 `List` 类型
    """
    # 定义查询结构
    query = """
        query($start: String!, $end: String!) { # 设置查询参数
            items(start: $start, end: $end)     # 查询 Query 类型的 items 字段, 传递查询参数, 结果为列表集合
        }
    """

    # 查询参数
    vars = {
        "start": "A",
        "end": "F",
    }

    # 执行查询
    r = schema.execute(query, variables=vars)
    # 确保查询正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "items": ["A", "B", "C", "D", "E", "F"]
    }
