from typing import Dict, Literal, Optional
from typing import Union as UnionType

from graphene import (
    Argument,
    Field,
    Float,
    ObjectType,
    ResolveInfo,
    Schema,
    String,
    Union,
)


class Human(ObjectType):
    """表示人类的实体类型

    对应的 GraphQL 定义如下:

    ```
    type Human {
        name: String!
        bornIn: String!
    }
    ```
    """

    name = String(required=True)
    born_in = String(required=True)


class Droid(ObjectType):
    """表示机器人的实体类型

    对应的 GraphQL 定义如下:

    ```
    type Droid {
        name: String!
        primaryFunction: String!
    }
    ```
    """

    name = String(required=True)
    primary_function = String(required=True)


class StarShip(ObjectType):
    """
    表示星舰的实体类型

    对应的 GraphQL 定义如下:

    ```
    type Ship {
        name: String!
        length: Int!
    }
    ```
    """

    name = String(required=True)
    length = Float(required=True)


class SearchResult(Union):
    """表示查询结果的实体类型,

    该类型是一个组合类型, 可以同时表示 `Human`, `Droid` 或 `Starship` 之一

    对于组合类型:
    - 需要从 `graphene.Union` 类型继承
    - 不能包含其它字段, 只能组合已有实体类型

    对应的 GraphQL 定义如下:

    ```
    union SearchResult = Human | Droid | Starship
    ```
    """

    class Meta:
        """实体类型元类型, 对于 `Union` 类型来说, 需要说明要组合的类型列表"""

        types = (Human, Droid, StarShip)


# 数据集对象, 用于支持数据查询
dataset: Dict[str, UnionType[Human, Droid, StarShip]] = {
    # 定义人类实体数据
    "Luke Skywalker": Human(
        name="Luke Skywalker",
        born_in="19 BBY",
    ),
    # 定义机器人实体数据
    "3PO": Droid(
        name="3PO",
        primary_function="Protocol",
    ),
    # 定义飞船实体数据
    "Millennium Falcon": StarShip(
        name="Millennium Falcon",
        length=34.75,
    ),
}


class Query(ObjectType):
    """查询类型, 演示 `Union` 实体类型的使用"""

    # 查询结果字段, 为 Union 实体类型字段
    search_result = Field(
        SearchResult,  # 字段类型为 Union 类型
        name=Argument(String, required=True),  # 具备一个 name 参数
    )

    @staticmethod
    def resolve_search_result(
        parent: Literal[None],
        info: ResolveInfo,
        name: str,
    ) -> Optional[UnionType[Human, Droid, StarShip]]:
        """解析 `search_result` 字段

        Args:
            name (str): 查询参数

        Returns:
            Optional[UnionType[Human, Droid, StarShip]]: 返回三种类型的联合类型
        """
        return dataset.get(name)


"""定义 schema 结构, 包括查询对象和定义的类型

对应的 GraphQL 定义为

```
schema {
    query: Query
}
```
"""
schema = Schema(query=Query)
