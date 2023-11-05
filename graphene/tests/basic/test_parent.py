from basic.parent import schema


def test_parent_argument_without_root_argument() -> None:
    """
    测试使用 `parent` 参数

    这个测试中, `Query` 类型 `resolve_person` 方法的 `parent` 参数为 `None`, 因为
    schema.execute 函数的 `root` 参数取默认值 `None`

    `resolve_person` 方法返回了一个 `Person` 类型对象, 作为 `Person` 类型
    `resolve_full_name` 方法的 `parent` 参数
    """
    # 定义查询结构
    query = """
        query {
            person {        # 查询 Query 类型的 person 字段
                firstName   # 查询 Person 类型的 first_name 字段
                lastName    # 查询 Person 类型的 last_name 字段
                fullName    # 查询 Person 类型的 full_name 字段
            }
        }
    """

    # 执行查询
    r = schema.execute(query)
    # 确保查询正确
    assert r.errors is None

    # 确保查询结果正确
    assert r.data == {
        "person": {
            "firstName": "Emma",
            "lastName": "Yua",
            "fullName": "Emma·Yua",
        }
    }


def test_parent_argument_with_root_argument() -> None:
    """
    测试使用 `parent` 参数, 并且传入其它参数
    """
    # 定义查询结构
    query = """
        query {
            person {                # 查询 Query 类型的 person 字段
                firstName           # 查询 Person 类型的 first_name 字段
                lastName            # 查询 Person 类型的 last_name 字段
                fullName            # 查询 Person 类型的 full_name 字段
            }
        }
    """

    # 执行查询
    r = schema.execute(query, root="Alvin")
    # 确保查询正确
    assert r.errors is None

    # 确保查询结果正确
    assert r.data == {
        "person": {
            "firstName": "Alvin",
            "lastName": "Qu",
            "fullName": "Alvin·Qu",
        }
    }
