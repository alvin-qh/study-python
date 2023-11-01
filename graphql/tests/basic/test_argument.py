from basic.argument import schema


def test_get_human1() -> None:
    """
    测试传递查询参数

    第一种方式, 通过 `Field` 构造器的 `**extra_args` 参数传递, 参数为 `Scalar` 类型对象
    """
    # 定义查询结构
    query = """
        query {
            human1(name: "Alvin·Qu") {  # 查询 Query 类型的 human1 字段, 传递参数
                firstName               # 查询 Human 类型的 first_name 字段
                lastName                # 查询 Human 类型的 last_name 字段
            }
        }
    """

    # 执行查询
    r = schema.execute(query)
    # 确保查询正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "human1": {
            "firstName": "Alvin",
            "lastName": "Qu",
        }
    }


def test_get_human2() -> None:
    """
    测试传递查询参数

    第二种方式, 通过 `Field` 构造器的 `**extra_args` 参数传递, 参数为 `Argument` 类型对象
    """
    # 定义查询结构
    query = """
        query($name: String!) {     # 设定查询参数
            human2(name: $name) {   # 查询 Query 类型的 human2 字段, 传递参数
                firstName           # 查询 Human 类型的 first_name 字段
                lastName            # 查询 Human 类型的 last_name 字段
            }
        }
    """

    # 查询参数
    vars = {"name": "Alvin·Qu"}

    # 执行查询
    r = schema.execute(query, variables=vars)
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "human2": {
            "firstName": "Alvin",
            "lastName": "Qu",
        }
    }


def test_get_human3() -> None:
    """
    测试传递查询参数

    第二种方式, 通过 `Field` 构造器的 `args` 参数传递, 参数为 `Dict` 类型对象
    """
    # 定义查询结构
    query = """
        query($name: String!) {     # 设定查询参数
            human3(name: $name) {   # 查询 Query 类型的 human3 字段, 传递参数
                firstName           # 查询 Human 类型的 first_name 字段
                lastName            # 查询 Human 类型的 last_name 字段
            }
        }
    """

    # 查询参数
    args = {"name": "Alvin·Qu"}

    # 执行查询
    r = schema.execute(query, variables=args)
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "human3": {
            "firstName": "Alvin",
            "lastName": "Qu",
        }
    }
