from basic.resolver import schema


def test_object_type_resolve() -> None:
    """
    测试解析字段
    """
    # 定义查询结构
    query = """
        query($type: String) {      # 定义查询参数
            person(type: $type) {   # 查询 Query 类型的 person 字段
                firstName           # 查询 Person 类型的 first_name 字段
                lastName            # 查询 Person 类型的 last_name 字段
                fullName            # 查询 Person 类型的 full_name 字段
            }
        }
    """

    # 定义查询参数
    vars = {"type": "chinese"}

    # 执行查询, 传入 chinese 参数
    # 此时会令 Query 类型的 resolve_person 方法返回 ChinesePerson 类型对象
    r = schema.execute(query, variables=vars)
    # 确保查询正确
    assert r.errors is None

    # 确认查询结果, 由于 ChinesePerson 类型没有 first_name 和 last_name 字段, 所以这两个字段为 None
    # full_name 字段是由 ChinesePerson 对象的 xing 字段和 ming 字段组合而成
    assert r.data == {
        "person": {
            "firstName": None,
            "lastName": None,
            "fullName": "Qu Hao",
        }
    }

    # 执行查询, 传入 chinese 参数
    # 此时会令 Query 类型的 resolve_person 方法返回 Person 类型对象
    r = schema.execute(query)
    # 确保查询正确
    assert r.errors is None

    # 确认查询结果, 由于 Person 类型具有 first_name 和 last_name 字段, 所以这两个字段正常返回
    # full_name 字段是由 Person 对象的 first_name 字段和 last_name 字段组合而成
    assert r.data == {
        "person": {
            "firstName": "Alvin",
            "lastName": "Qu",
            "fullName": "Alvin·Qu",
        }
    }
