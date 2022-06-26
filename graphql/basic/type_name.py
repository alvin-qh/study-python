from graphene import Field, ObjectType, Schema, String


class TypeSong(ObjectType):
    """
    演示为实体类型设置类型名称

    默认情况下, 实体对象的名称即它的类型名称. 但一些必要时候, 需要为实体定义与其类型
    名不同的名称, 以便在 graphql 查询结构中使用

    对应的 GraphQL 定义如下:

    ```
    type Song {
        songName!
        name: String
        serialNo: Int!
        price: Float!
        lts: Boolean!
    }
    ```
    """
    class Meta:
        name = "Song"

    song_name = String(default_value="Hello Song")


class Query(ObjectType):
    song = Field(TypeSong, default_value=TypeSong())


schema = Schema(query=Query)
