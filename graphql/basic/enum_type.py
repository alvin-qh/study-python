from typing import Literal, List as ListType
from graphene import Argument, Enum, Field, List, ObjectType, ResolveInfo, Schema, String


class Episode(Enum):
    """
    以标准形式定义 graphql 枚举类型

    对应的 GraphQL 定义如下:

    ```
    enum Episode {
        NEWHOPE
        EMPIRE
        JEDI
    }
    ```
    """
    NEWHOPE = 4
    EMPIRE = 5
    JEDI = 6


class Movie(ObjectType):
    """
    定义一个表示影片的类型

    对应的 GraphQL 定义如下:

    ```
    type Movie {
        name: String!
        episode: Episode!
    }
    ```
    """
    # 影片名称字段
    name = String(required=True)

    # 影片阶段字段, 通过枚举类型定义字段
    episode = Episode(required=True)


"""
以 Enum 实例形式定义 graphql 枚举类型

对应的 GraphQL 定义如下:

```
enum Faction {
    LIGHT_SIDE
    DARK_SIDE
}
```
"""
Faction = Enum("Faction", [("LIGHT_SIDE", 2), ("DARK_SIDE", 3)])


class Character(ObjectType):
    """
    定义一个表示角色的类型

    对应的 GraphQL 定义如下:

    ```
    type Movie {
        name: String!
        faction: Faction!
    }
    ```
    """
    # 角色名称字段
    name = String(required=True)

    # 角色派别字段, 通过枚举类型定义字段
    # 枚举类型和其它实体类型一样, 在定义字段时可以通过 Field 类型定义, 也可以通过枚举类型直接定义
    faction = Field(Faction, required=True)


class Query(ObjectType):
    """
    定义查询类型

    对应的 GraphQL 定义如下:

    ```
    type Query {
        movie(episode: Episode!): Movie!
        characters(faction: Faction!): [Character]!
    }
    ```
    """
    # 影片字段, 通过影片所处的阶段查询
    movie = Field(
        Movie,
        episode=Argument(Episode, required=True),
        required=True,
    )

    # 角色列表字段, 通过角色所属的派别查询
    characters = List(
        Character,
        faction=Argument(Faction, required=True),
        required=True,
    )

    @staticmethod
    def resolve_movie(parent: Literal[None], info: ResolveInfo, episode: Episode) -> Movie:
        """
        解析影片字段

        Args:
            episode (Episode): 影片所属的阶段 (枚举类型)

        Raises:
            ValueError: `episode` 参数传递了不被支持的值

        Returns:
            Movie: 查询到的影片实体对象
        """
        if episode is Episode.NEWHOPE:
            return Movie(name="New Hope", episode=episode)

        if episode is Episode.EMPIRE:
            return Movie(name="Empire", episode=episode)

        if episode is Episode.JEDI:
            return Movie(name="Jedi", episode=episode)

        raise ValueError("episode_name")

    @staticmethod
    def resolve_characters(
        parent: Literal[None],
        info: ResolveInfo,
        faction: Faction,  # type: ignore
    ) -> ListType[Character]:
        """
        解析角色字段

        Args:
            faction (Faction): 角色的派别

        Raises:
            ValueError: `faction` 参数传递了不被支持的值

        Returns:
            ListType[Character]: 查询到的角色实体对象列表
        """
        if faction == Faction.LIGHT_SIDE:
            return [
                Character(name="Anakin Skywalker", faction=Faction.LIGHT_SIDE),
                Character(name="Obi-Wan Kenobi", faction=Faction.LIGHT_SIDE),
            ]

        elif faction == Faction.DARK_SIDE:
            return [
                Character(name="Darth Vader", faction=Faction.DARK_SIDE),
                Character(name="Darth Maul", faction=Faction.LIGHT_SIDE),
            ]

        raise ValueError("faction")


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
