from .schema import schema


def test_schema_query() -> None:
    """
    测试查询
    """
    # 定义查询字符串
    query = """
        query {
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
        query {
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


def test_schema_mutation() -> None:
    """
    测试更改
    """
    # 定义更改字符串
    mutation = """
        mutation {
            createSomething(arg: "Args")
        }
    """

    # 执行更改
    r = schema.execute(mutation)

    # 确认更改结果正确
    assert r.errors is None
    assert r.data == {
        "createSomething": "Args mutated",
    }
