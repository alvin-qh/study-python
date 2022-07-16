from .enum_type import schema


def test_standard_enum() -> None:
    """
    测试通过标准方式定义的枚举类型
    """
    # 定义查询结构
    query = """
        query($episode: Episode!) {     # 设置查询参数
            movie(episode: $episode) {  # 查询 Query 对象的 movie 字段, 传递参数
                name                    # 查询 Movie 类型的 name 字段
                episode                 # 查询 Movie 类型的 episode 字段, 为 Episode 枚举类型
            }
        }
    """

    # 定义查询参数
    vars = {"episode": "EMPIRE"}

    # 执行查询
    r = schema.execute(query, variables=vars)
    # 确保查询正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "movie": {
            "episode": "EMPIRE",
            "name": "Empire",
        }
    }


def test_enum_instance() -> None:
    """
    测试通过 `Enum` 实例的方式定义的枚举类型
    """
    # 定义查询结构
    query = """
        query($faction: Faction!) {         # 设定查询参数
            characters(faction: $faction) { # 查询 Query 类型的 characters 字段, 传递参数
                name                        # 查询 Character 类型的 name 字段
                faction                     # 查询 Character 类型的 faction 字段, 为 Faction 枚举类型
            }
        }
    """

    # 定义查询参数
    vars = {"faction": "DARK_SIDE"}

    # 执行查询
    r = schema.execute(query, variables=vars)
    # 确保查询正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "characters": [
            {
                "faction": "DARK_SIDE",
                "name": "Darth Vader",
            },
            {
                "faction": "LIGHT_SIDE",
                "name": "Darth Maul",
            },
        ]
    }
