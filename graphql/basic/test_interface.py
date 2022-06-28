from .interface import schema


def test_query_character_type() -> None:
    """
    以接口类型进行结果查询

    对 `Query` 类型的 `hero` 字段进行查询, 该字段为 `Character` 类型, 即接口类型
    """
    # 查询字符串
    query = """
        query($episode: Int!) {
            hero(episode: $episode) {     # 对应 Query 类型的 hero 字段
                id            # 对应 Character 类型的 id 字段
                name          # 对应 Character 类型的 name 字段
                friends {     # 对应 Character 类型的 friends 字段
                    id        # 对应 Character 类型的 id 字段
                    name      # 对应 Character 类型的 name 字段
                }
            }
        }
    """

    # 设置查询阶段 5 的数据
    vars = {"episode": 5}

    # 执行查询
    r = schema.execute(query, variables=vars)
    # 确认查询正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "hero": {
            "id": "1",
            "name": "Luke Skywalker",
            "friends": [
                {
                    "id": "2",
                    "name": "Obi-Wan Kenobi",
                },
                {
                    "id": "3",
                    "name": "Han Solo",
                },
                {
                    "id": "4",
                    "name": "R2-D2",
                },
                {
                    "id": "5",
                    "name": "3PO",
                },
            ],
        },
    }

    # 设置查询阶段 6 的数据
    vars = {"episode": 6}

    # 执行查询
    r = schema.execute(query, variables=vars)
    # 确认查询正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "hero": {
            "id": "4",
            "name": "R2-D2",
            "friends": [
                {
                    "id": "5",
                    "name": "3PO",
                },
                {
                    "id": "1",
                    "name": "Luke Skywalker",
                },
                {
                    "id": "2",
                    "name": "Obi-Wan Kenobi",
                },
            ],
        },
    }


def test_query_human_type() -> None:
    """
    以接口子类型进行结果查询

    对 `Query` 类型的 `humanHero` 字段进行查询, 该字段为 `Human` 类型, 即接口的实现类型
    """
    # 查询字符串
    query = """
        query($episode: Int!) {
            humanHero(episode: $episode) {     # 对应 Query 类型的 human_hero 字段
                id            # 对应 Human 类型的 id 字段
                name          # 对应 Human 类型的 name 字段
                friends {     # 对应 Human 类型的 friends 字段
                    id        # 对应 Character 类型的 id 字段
                    name      # 对应 Character 类型的 name 字段
                }
                starShips {   # 对应 Human 类型的 star_ships 字段
                    name      # 对应 StarShip 类型的 name
                    shipType  # 对应 StarShip 类型的 ship_type
                }
            }
        }
    """

    # 设置查询阶段 5 的数据
    vars = {"episode": 5}

    # 执行查询
    r = schema.execute(query, variables=vars)
    # 确认查询正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "humanHero": {
            "id": "1",
            "name": "Luke Skywalker",
            "friends": [
                {
                    "id": "2",
                    "name": "Obi-Wan Kenobi",
                },
                {
                    "id": "3",
                    "name": "Han Solo",
                },
                {
                    "id": "4",
                    "name": "R2-D2",
                },
                {
                    "id": "5",
                    "name": "3PO",
                },
            ],
            "starShips": [
                {
                    "name": "Millennium Falcon",
                    "shipType": "CARGO_SHIP",
                },
            ],
        }
    }


def test_query_droid_type() -> None:
    """
    以接口子类型进行结果查询

    对 `Query` 类型的 `droidHero` 字段进行查询, 该字段为 `Droid` 类型, 即接口的实现类型
    """
    query = """
        query($episode: Int!) {
            droidHero(episode: $episode) {  # 对应 Query 类型的 droid_hero 字段
                id                  # 对应 Droid 类型的 id 字段
                name                # 对应 Droid 类型的 name 字段
                friends {           # 对应 Droid 类型的 friends 字段
                    id              # 对应 Character 类型的 id 字段
                    name            # 对应 Character 类型的 name 字段
                }
                primaryFunction     # 对应 Droid 类型的 primary_function 字段
            }
        }
    """

    # 设置查询阶段 5 的数据
    vars = {"episode": 5}

    # 执行查询
    r = schema.execute(query, variables=vars)
    # 确认查询正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "droidHero": {
            "id": "4",
            "name": "R2-D2",
            "friends": [
                {
                    "id": "5",
                    "name": "3PO",
                },
                {
                    "id": "1",
                    "name": "Luke Skywalker",
                },
                {
                    "id": "2",
                    "name": "Obi-Wan Kenobi",
                }
            ],
            "primaryFunction": "Astronaut",
        },
    }


def test_query_multiple_type() -> None:
    query = """
        query($episode: Int!) {
            hero(episode: $episode) {   # 对应 Query 类型的 hero 字段
                __typename              # 获取查询结果的实体类型
                name                    # 对应 Character 类型的 name 字段
                ... on Droid {          # 对于查询结果为 Droid 实体类型时
                    primaryFunction     # 对应 Droid 类型的 primary_function 字段
                }
                ... on Human {          # 对于查询结果为 Human 实体类型时
                    homePlanet          # 对应 Human 类型的 home_planet 字段
                }
            }
        }
    """

    # 设置查询阶段 5 的数据
    vars = {"episode": 5}

    # 执行查询
    r = schema.execute(query, variables=vars)
    # 确认查询正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "hero": {
            "__typename": "Human",
            "name": "Luke Skywalker",
            "homePlanet": "Tatooine",
        }
    }

    # 设置查询阶段 6 的数据
    vars = {"episode": 6}

    # 执行查询
    r = schema.execute(query, variables=vars)
    # 确认查询正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "hero": {
            "__typename": "Droid",
            "name": "R2-D2",
            "primaryFunction": "Astronaut",
        },
    }
