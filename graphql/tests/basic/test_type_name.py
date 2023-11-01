from basic.type_name import schema


def test_define_type_name() -> None:
    """
    测试通过 `Meta` 类型定义实体类型的类型名称
    """
    # 定义查询结构
    query = """
        query {
            song {          # 查询 Query 类型的 song 字段
                songName    # 查询 TypeSong 类型的 songName 字段
            }
        }
    """

    # 执行查询
    r = schema.execute(query)
    # 确保查询正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {"song": {"songName": "Hello Song"}}
