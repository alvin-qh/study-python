from typing import Dict
from typing import List as ListType
from typing import Union

from graphene import (ID, Enum, Field, Int, Interface, List, NonNull, ObjectType,
                      ResolveInfo, Schema, String)


class Character(Interface):
    """
    定义一个接口类型, 该类型可作为所有实体类型 (`ObjectType`) 的接口类型

    对应的 GraphQL 定义如下:

    ```
    interface Character {
        id: ID!
        name: String!
        friends: [Person]!
    }
    ```
    """
    id = ID(required=True)
    name = String(required=True)
    friends = List(lambda: Character)


class ShipType(Enum):
    """
    定义一个枚举实体类型, 表示飞船类型

    对应的 GraphQL 定义如下:

    ```
    enum ShipType {
        CARGO_SHIP
        BATTLE_SHIP
        PASSENGER_SHIP
    }
    ```
    """
    CARGO_SHIP = 1  # 表示货运船
    BATTLE_SHIP = 2  # 表示战舰
    PASSENGER_SHIP = 3  # 表示客运船


class StarShip(ObjectType):
    """
    定义星舰实体类型

    对应的 GraphQL 定义如下:

    ```
    type StarShip {
        name: String!
        shipType: ShipType!
    }
    ```
    """
    name = String(required=True)
    ship_type = Field(ShipType, required=True)


class Human(ObjectType):
    """
    定义人类实体类型, 实现 `Character` 接口

    对应的 GraphQL 定义如下:

    ```
    type Human implements Character {
        starShips: [StarShip!]!
        homePlanet: String!
    }
    ```
    """
    class Meta:
        interfaces = (Character,)

    star_ships = List(NonNull(StarShip), required=True)
    home_planet = String(required=True)


class Droid(ObjectType):
    """
    定义机器人实体类型, 实现 `Character` 接口

    对应的 GraphQL 定义如下:

    ```
    type Human implements Character {
        primaryFunction: String!
    }
    ```
    """
    class Meta:
        interfaces = (Character,)

    primary_function = String(required=True)

# 初始化数据集, 包含定义的实体类型对象
dataset: Dict[str, ListType[Union[StarShip, Human, Droid]]] = {
    # 飞船实体对象集合
    "ships": [
        StarShip(
            name="Millennium Falcon",
            ship_type=ShipType.CARGO_SHIP,
        ),
    ],

    # 人类实体对象集合
    "humans": [
        Human(
            id=1,
            name="Luke Skywalker",
            home_planet="Tatooine",
        ),
        Human(
            id=2,
            name="Obi-Wan Kenobi",
            home_planet="Stewjon",
        ),
        Human(
            id=3,
            name="Han Solo",
            home_planet="Corellia",
        ),
    ],

    # 机器人实体对象合集
    "droids": [
        Droid(
            id=4,
            name="R2-D2",
            primary_function="Astronaut",
        ),
        Droid(
            id=5,
            name="3PO",
            primary_function="Etiquette",
        ),
    ]
}

# 设定实体对象之间的关系
dataset["humans"][0].friends = [
    dataset["humans"][1],
    dataset["humans"][2],
    dataset["droids"][0],
    dataset["droids"][1],
]

dataset["humans"][1].friends = [
    dataset["humans"][0]
]

dataset["humans"][2].friends = [
    dataset["humans"][0],
    dataset["droids"][0],
    dataset["droids"][1],
]

dataset["droids"][0].friends = [
    dataset["droids"][1],
    dataset["humans"][0],
    dataset["humans"][1],
]

dataset["droids"][1].friends = [
    dataset["droids"][0],
    dataset["humans"][0],
    dataset["humans"][1],
]

dataset["humans"][0].star_ships = [
    dataset["ships"][0],
]

dataset["humans"][1].star_ships = [
    dataset["ships"][0],
]


class HeroQuery(ObjectType):
    """
    定义英雄查询类型

    对应的 GraphQL 定义如下:

    ```
    type HeroQuery {
        hero(episode: Int!): Character!
    }
    ```
    """
    # Character 类型字段
    hero = Field(Character, episode=Int(required=True), required=True)

    @staticmethod
    def resolve_hero(parent: Character, info: ResolveInfo, episode: int) -> Character:
        """
        解析 `hero` 字段

        Args:
            episode (int): 参数, 表示电影的阶段

        Returns:
            Character: 返回 `Character` 类型实体对象
        """
        if episode == 5:
            return dataset["humans"][0]

        return dataset["droids"][0]


class HumanQuery(ObjectType):
    """
    定义人类英雄查询类型

    对应的 GraphQL 定义如下:

    ```
    type HumanQuery {
        humanHero(episode: Int!): Human!
    }
    ```
    """
    human_hero = Field(Human, episode=Int(required=True), required=True)

    @staticmethod
    def resolve_human_hero(parent: Human, info: ResolveInfo, episode: int) -> Human:
        """
        解析 `human_hero` 字段

        Args:
            episode (int): 参数, 表示电影的阶段

        Returns:
            Character: 返回 `Human` 类型实体对象
        """
        if episode == 5:
            return dataset["humans"][0]

        return dataset["humans"][2]


class DroidQuery(ObjectType):
    """
    定义机器人英雄查询类型

    对应的 GraphQL 定义如下:

    ```
    type DroidQuery {
        droidHero(episode: Int!): Droid!
    }
    ```
    """
    droid_hero = Field(Droid, episode=Int(required=True), required=True)

    @staticmethod
    def resolve_droid_hero(parent: Droid, info: ResolveInfo, episode: int) -> Droid:
        """
        解析 `droid_hero` 字段

        Args:
            episode (int): 参数, 表示电影的阶段

        Returns:
            Character: 返回 `Droid` 类型实体对象
        """
        if episode == 5:
            return dataset["droids"][0]

        return dataset["droids"][1]


class Query(HeroQuery, HumanQuery, DroidQuery):
    """
    将 `HeroQuery`, `HumanQuery` 和 `DroidQuery` 字段进行组合

    对应的 GraphQL 定义如下:

    ```
    type Query {
        hero(episode: Int!): Character!
        humanHero(episode: Int!): Human!
        droidHero(episode: Int!): Droid!
    }
    ```
    """
    pass


"""
定义 schema 结构, 包括查询对象和定义的类型

对应的 GraphQL 定义为

```
schema {
    query: Query
}
```
"""
schema = Schema(query=Query)
