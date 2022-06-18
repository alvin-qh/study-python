from .operation_name import schema


def test_operation_name() -> None:
    """
    不设置 `root` 参数, 表示不给顶级实体对象设置上级关联对象, `parent` 参数为 `None`
    """
    # 查询字符串
    query = """
        query getUser($id: ID!) {   # 定义操作名称, 定义查询参数的参数名称
            user(id: $id) {  # 对应 Query 对象的 user 字段, 传递名为 id 的参数
                id           # 对应 User 类型的 id 字段
                firstName    # 对应 User 类型的 first_name 字段
                lastName     # 对应 User 类型的 last_name 字段
            }
        }

        query getUserWithFullName($id: ID!) {   # 定义操作名称, 定义查询参数名称
            user(id: $id) { # 对应 Query 对象的 user 字段, 传递名为 id 的参数
                id          # 对应 User 类型的 id 字段
                fullName    # 对应 User 类型的 full_name 字段
            }
        }
    """

    # 定义要执行的操作名称
    opt_name = "getUser"
    # 定义查询参数
    var = {"id": 3}

    # 执行查询
    r = schema.execute(query, operation_name=opt_name, variables=var)
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "user": {
            "id": "3",
            "firstName": "Lucy",
            "lastName": "Green",
        }
    }

    # 定义要执行的操作名称
    opt_name = "getUserWithFullName"
    # 定义查询参数
    var = {"id": 1}

    # 执行查询
    r = schema.execute(query, operation_name=opt_name, variables=var)
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "user": {
            "id": "1",
            "fullName": "Alvin·Qu",
        }
    }
