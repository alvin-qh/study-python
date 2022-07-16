from .operation_name import schema


def test_operation_name() -> None:
    """
    不设置 `root` 参数, 表示不给顶级实体对象设置上级关联对象, `parent` 参数为 `None`
    """
    # 定义查询结构
    query = """
        query getUser($id: ID!) {   # 定义查询参数, 定义操作名称
            user(id: $id) {         # 查询 Query 对象的 user 字段, 传递参数
                id                  # 查询 User 类型的 id 字段
                firstName           # 查询 User 类型的 first_name 字段
                lastName            # 查询 User 类型的 last_name 字段
            }
        }

        query getUserWithFullName($id: ID!) {   # 定义查询参数, 定义操作名称
            user(id: $id) {                     # 查询 Query 对象的 user 字段, 传递参数
                id                              # 查询 User 类型的 id 字段
                fullName                        # 查询 User 类型的 full_name 字段
            }
        }
    """

    # 定义要执行的操作名称
    opt_name = "getUser"
    # 定义查询参数
    vars = {"id": 3}

    # 执行查询
    r = schema.execute(
        query,
        operation_name=opt_name,
        variables=vars,
    )
    # 确保查询执行正确
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
    vars = {"id": 1}

    # 执行查询
    r = schema.execute(
        query,
        operation_name=opt_name,
        variables=vars,
    )
    # 确保查询执行正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "user": {
            "id": "1",
            "fullName": "Alvin·Qu",
        }
    }
