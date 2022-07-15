from .mutation import schema


def test_create_person1() -> None:
    """
    测试通过 scalar 类型参数进行实体更新的 `Mutation` 查询
    """
    query = """
        mutation($name: String!, $age: Int!) {         # 定义 scalar 类型参数
            createPerson1(name: $name, age: $age) {    # 调用 Mutations 类型的 
                __typename
                name
                age
            }
        }
    """

    vars = {"name": "Alvin", "age": 40}

    r = schema.execute(query, variables=vars)
    assert r.errors is None
    assert r.data == {
        "createPerson1": {
            "__typename": "Person",
            "age": 40,
            "name": "Alvin",
        }
    }


def test_create_person2() -> None:
    query = """
        mutation($input: PersonInput!) {
            createPerson2(personData: $input) {
                __typename
                name
                age
            }
        }
    """

    vars = {
        "input": {
            "name": "Alvin",
            "age": 40,
        }
    }

    r = schema.execute(query, variables=vars)
    assert r.errors is None

    assert r.data == {
        "createPerson2": {
            "__typename": "Person",
            "age": 40,
            "name": "Alvin",
        }
    }
