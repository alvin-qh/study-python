from .union_type import schema


def test_union_type() -> None:
    """
    测试 `Union` 实体类型, 该类型可以组合其它实体类型
    """
    # 查询结构
    query = """
        query($name: String!) {             # 定义查询 name 参数
            searchResult(name: $name) {     # 查询 Query 类型的 search_result 字段
                ...on Human {               # 查询结果为 Human 类型时
                    __typename              # 查询实体类型
                    name                    # 查询 Human 类型的 name 字段
                    bornIn                  # 查询 Human 类型的 bornIn 字段
                }

                ...on Droid {               # 查询结果为 Droid 类型时
                    __typename              # 查询实体类型
                    name                    # 查询 Droid 类型的 name 字段
                    primaryFunction         # 查询 Droid 类型的 primaryFunction 字段
                }

                ...on StarShip {            # 查询结果为 StarShip 类型时
                    __typename              # 查询实体类型
                    name                    # 查询 StarShip 类型的 name 字段
                    length                  # 查询 StarShip 类型的 length 字段
                }
            }
        }
    """

    # 查询参数
    vars = {
        "name": "3PO",
    }

    # 执行查询
    r = schema.execute(query, variables=vars)
    # 确保查询正确
    assert r.errors is None

    # 确认查询结果, 为 Droid 类型结果
    assert r.data == {
        "searchResult": {
            "__typename": "Droid",
            "name": "3PO",
            "primaryFunction": "Protocol",
        }
    }
