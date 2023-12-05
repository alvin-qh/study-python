from basic.camel_case import schema


def test_auto_camel_case() -> None:
    """
    测试自动转驼峰命名规则
    """
    # 定义查询结构
    query = """
        query {
            person {           # 查询 Query 中的 person 字段
                lastName       # 查询 Person 中的 last_name 字段, 自动转为驼峰命名
                _other_name_   # 查询 Person 中的 other_name 字段, 通过 name 参数指定了名称
            }
        }
    """

    # 执行查询
    r = schema.execute(query)
    # 确认查询无错误
    assert r.errors is None

    # 验证查询结果
    assert r.data == {
        "person": {
            "lastName": "Qu",
            "_other_name_": "Alvin",
        }
    }
