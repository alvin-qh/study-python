from .root import User, schema


def test_without_parent() -> None:
    """
    不设置 `root` 参数, 表示不给顶级实体对象设置上级关联对象, `parent` 参数为 `None`
    """
    # 查询字符串
    query = """
        query($id: ID!) {   # 定义查询参数的名称为 id
            user(id: $id) { # 对应 Query 类型的 user 字段
                id          # 对应 User 类型的 id 字段
                name        # 对应 User 类型的 name 字段
            }
        }
    """

    root = None
    # 查询参数
    var = {
        "id": 2,  # 定义名为 id 的参数, 对应查询字符串中的参数名
    }

    # 执行查询, 传递查询参数, root 参数为 None
    r = schema.execute(query, variables=var, root=root)

    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "user": {
            "id": "2",
            "name": "Emma",
        },
    }


def test_with_parent() -> None:
    """
    设置 `root` 参数, 为顶级实体对象设置关联对象, 此时 `parent` 参数有值
    """
    # 查询字符串
    query = """
        query {
            user {
                id      # 对应 User 类型的 id 字段
                name    # 对应 User 类型的 name 字段
            }
        }
    """

    # 设置 root 参数
    root = User(id=1, name="Alvin")

    # 执行查询, 并设置 root 参数
    r = schema.execute(query, root=root)

    assert r.errors is None

    # 确认查询结果, 由于设置了 root, 所以查询结果为 root 设置的值
    assert r.data == {
        "user": {
            "id": "1",
            "name": "Alvin",
        },
    }
