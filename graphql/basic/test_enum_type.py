from .enum_type import schema


def test_standard_enum() -> None:
    """
    测试通过标准方式定义的枚举类型
    """
    # 定义查询结构
    query = """
        query($episode: Episode!) {
            movie(episode: $episode) {
                name
                episode
            }
        }
    """

    # 定义查询参数
    vars = {
        "episode": "EMPIRE",
    }

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
        query($faction: Faction!) {
            characters(faction: $faction) {
                name
                faction
            }
        }
    """

    # 定义查询参数
    vars = {
        "faction": "DARK_SIDE",
    }

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
