from execution.variable import schema


def test_variables() -> None:
    """
    测试通过变量传递查询参数
    """
    # 定义查询结构
    query = """
        query($id: ID!) {   # 定义查询变量
            user(id: $id) { # 查询 Query 类型的 user 字段, 传递参数
                id          # 查询 User 类型的 id 字段
                name        # 查询 User 类型的 name 字段
            }
        }
    """

    # 查询参数
    args = {"id": 2}  # 定义名为 id 的参数, 对应查询字符串中的参数名

    # 执行查询, 传递查询参数
    r = schema.execute(query, variables=args)

    # 确保查询正确
    assert r.errors is None
    # 确认查询结果
    assert r.data == {"user": {"id": "2", "name": "Emma"}}
