from .variable import schema


def test_variables() -> None:
    """
    测试通过变量传递查询参数
    """
    # 定义查询字符串
    query = """
        query($id: ID!) {      # 定义查询变量名称为 id
            user(id: $id) {    # 对应 Query 类型的 user 字段, 定义参数为 id 参数的值
                id      # 查询 User 类型的 id 字段
                name    # 查询 User 类型的 name 字段
            }
        }
    """

    # 查询参数
    var = {
        "id": 2,  # 定义名为 id 的参数, 对应查询字符串中的参数名
    }

    # 执行查询, 传递查询参数
    r = schema.execute(query, variables=var)

    # 确保查询正确
    assert r.errors is None
    # 确认查询结果
    assert r.data == {
        "user": {
            "id": "2",
            "name": "Emma"
        }
    }
