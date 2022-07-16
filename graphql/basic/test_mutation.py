from .mutation import schema


def test_create_person1() -> None:
    """
    测试通过 scalar 类型参数进行实体更新的 `Mutation` 查询
    """
    # 定义查询结构
    query = """
        mutation($name: String!, $age: Int!) {         # 定义 scalar 类型参数
            createPerson1(name: $name, age: $age) {    # 调用 Mutations 类型的 create_person1 字段, 传入参数
                __typename      # 类型为 Person 类型
                name            # Person 类型的 name 字段
                age             # Person 类型的 age 字段
            }
        }
    """

    # 查询参数
    vars = {"name": "Alvin", "age": 40}

    # 执行查询
    r = schema.execute(query, variables=vars)
    # 确保查询执行正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "createPerson1": {
            "__typename": "Person",
            "age": 40,
            "name": "Alvin",
        }
    }


def test_create_person2() -> None:
    """
    测试通过 `InputObjectType` 作为输入参数更新对象
    """
    # 定义查询结构
    query = """
        mutation($input: PersonInput!) {         # 定义输入参数
            createPerson1(personData: $input) {  # 调用 Mutations 类型的 create_person1 字段, 传入参数
                __typename      # 类型为 Person
                name            # Person 类型的 name 字段
                age             # Person 类型的 age 字段
            }
        }
    """

    # 查询参数
    vars = {
        "input": {
            "name": "Alvin",
            "age": 40,
        }
    }

    # 执行查询
    r = schema.execute(query, variables=vars)
    # 确保查询执行正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "createPerson2": {
            "__typename": "Person",
            "age": 40,
            "name": "Alvin",
        }
    }
