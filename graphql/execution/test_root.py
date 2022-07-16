from .root import User, schema


def test_without_parent() -> None:
    """
    不设置 `root` 参数, 表示不给顶级实体对象设置上级关联对象, `parent` 参数为 `None`
    """
    # 定义查询结构
    query = """
        query($id: ID!) {   # 定义查询参数
            user(id: $id) { # 查询 Query 类型的 user 字段
                id          # 查询 User 类型的 id 字段
                name        # 查询 User 类型的 name 字段
            }
        }
    """

    # 定义查询参数
    vars = {"id": 2}  # 定义名为 id 的参数, 对应查询字符串中的参数名

    # 执行查询, 传递查询参数, root 参数为 None
    r = schema.execute(
        query,
        variables=vars,
        root=None,  # 指定 root 参数为 None, 即不指定 root 参数
    )

    # 确保查询执行正确
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
    # 定义查询结构
    query = """
        query {
            user {
                id      # 查询 User 类型的 id 字段
                name    # 查询 User 类型的 name 字段
            }
        }
    """

    # 设置 root 参数
    root = User(id=1, name="Alvin")

    # 执行查询, 并设置 root 参数
    r = schema.execute(
        query,
        root=root,  # 指定 root 参数
    )

    # 确保查询执行正确
    assert r.errors is None

    # 确认查询结果, 由于设置了 root, 所以查询结果为 root 设置的值
    assert r.data == {
        "user": {
            "id": "1",
            "name": "Alvin",
        },
    }
