from .interface import schema


def test_interface() -> None:
    """
    测试接口类型的定义
    """
    # 查询字符串
    query = """
        query findStudent {
            classLeader {   # 对应 Query 中的 class_leader 字段
                id          # 对应 Person 中的 id 字段
                name        # 对应 Person 中的 name 字段
                friends {   # 对应 Person 中的 friends 字段
                    id
                    name
                    # classRoom # The "friends" is "Person" type,
                                # cannot query by "class_room" field.
                                # If the "class_room" is necessary
                                # for "friends" field,
                                # change "friends = List(lambda: Person)"
                                # to "friends = List(lambda: Student)"
                }
                classRoom   # 对应 Student 中的 class_room 字段
            }
        }
    """

    # 执行查询
    r = schema.execute(query)
    # 确认查询正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "classLeader": {
            "id": "1",
            "name": "Alvin",
            "classRoom": "1-1",
            "friends": [
                {
                    "id": "3",
                    "name": "Lucy",
                }
            ],
        }
    }
