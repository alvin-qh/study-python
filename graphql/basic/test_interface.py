from .interface import schema


def test_interface() -> None:
    """
    测试接口类型的定义
    """
    # 查询字符串
    query = """
        query findStudent {
            classLeader {     # 对应 Query 类型的 class_leader 字段
                id            # 对应 Student 类型的 id 字段
                name          # 对应 Student 类型的 name 字段
                friends {     # 对应 Student 类型的 friends 字段
                    id        # 对应 Person 类型的 id 字段
                    name      # 对应 Person 类型的 name 字段
                }
                classRoom     # 对应 Student 类型的 class_room 字段
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


def test_type_exchange() -> None:
    """
    测试接口类型的定义
    """
    # 查询字符串
    query = """
        query findStudent {
            classLeader {         # 对应 Query 类型的 class_leader 字段
                ... on Person {   # 将 Student 类型转为 Person 类型
                    id            # 对应 Person 类型的 id 字段
                    name          # 对应 Person 类型的 name 字段
                    friends {     # 对应 Person 类型的 friends 字段
                        id        # 对应 Person 类型的 id 字段
                        name      # 对应 Person 类型的 name 字段
                    }
                }
                classRoom         # 对应 Student 类型的 class_room 字段
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
