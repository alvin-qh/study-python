from .parent import schema


def test_parent_argument1() -> None:
    """
    测试使用 `parent` 参数
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
            "firstName": "Alvin",
            "lastName": "Qu",
            "fullName": "Alvin·Qu",
        }
    }


def test_parent_argument2() -> None:
    """
    测试使用 `parent` 参数, 并且传入其它参数
    """
    # 定义查询结构
    query = """
        query($splitter: String!) { # 设置查询参数
            person {                # 查询 Query 类型的 person 字段
                firstName           # 查询 Person 类型的 first_name 字段
                lastName            # 查询 Person 类型的 last_name 字段
                fullName(splitter: $splitter)   # 查询 Person 类型的 full_name 字段, 传递参数
            }
        }
    """

    # 查询参数
    vars = {"splitter": ","}

    # 执行查询
    r = schema.execute(query, variables=vars)
    # 确保查询正确
    assert r.errors is None

    # 确保查询结果正确
    assert r.data == {
        "person": {
            "firstName": "Alvin",
            "lastName": "Qu",
            "fullName": "Alvin,Qu",
        }
    }
