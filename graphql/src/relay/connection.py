from typing import Any, Dict, Generic
from typing import List as ListType
from typing import Literal, Sequence, TypeVar, cast

from aiodataloader import DataLoader
from graphene import (
    ID,
    Argument,
    Connection,
    ConnectionField,
    Field,
    Int,
    ObjectType,
    PageInfo,
    ResolveInfo,
    Schema,
    String,
)


class Ship(ObjectType):
    id = ID(required=True)
    name = String(required=True)


T = TypeVar("T")


class QueryResult(PageInfo, Generic[T]):
    __parameters__ = ""

    def __init__(self, data: ListType[T], start: int, end: int, count: int) -> None:
        self._data = data
        self._start = start
        self._end = end
        self.count = count

    @property
    def start_cursor(self) -> int:
        return self._start

    @property
    def end_cursor(self) -> int:
        return self._end

    @property
    def has_next_page(self) -> bool:
        return self._end < self.count

    @property
    def has_previous_page(self) -> bool:
        return self._start > 0

    @property
    def data(self) -> ListType[T]:
        return self._data


class ShipConnection(Connection):
    class Meta:
        node = Ship

    class Edge:
        link = String()

        def __init__(self, **kwargs: Any) -> None:
            """占位方法, 不会被调用"""

    total_count = Int()

    def __init__(self, query_result: QueryResult) -> None:
        self.query_result = query_result

    def resolve_page_info(self, info: ResolveInfo) -> QueryResult[Ship]:
        return self.query_result

    def resolve_total_count(self, info: ResolveInfo) -> int:
        return self.query_result.count

    def resolve_edges(self, info: ResolveInfo) -> ListType[Edge]:
        start = self.query_result.start
        return [
            self.Edge(cursor=start + n, node=d, link=f"https://myapp.com/data/{d.id}")
            for n, d in enumerate(self.query_result.data)
        ]


class Hero(ObjectType):
    id = ID(required=True)
    name = String(required=True)
    own_ships = ConnectionField(ShipConnection)

    async def resolve_own_ships(
        self, info: ResolveInfo, **kwargs: Any
    ) -> ListType[Ship]:
        """
        Resolve "own_ships" field, return "ShipConnection" object
        """
        first = max(cast(int, kwargs.get("first", 0)), 0)
        last = min(
            cast(int, kwargs.get("last", len(self.own_ships) - 1)),
            len(self.own_ships) - 1,
        )
        data = await ship_loader.load_many(self.own_ships[first : last + 1])

        result = QueryResult(data, first, last, len(data))
        return ShipConnection(result)


class Dataset:
    def __init__(self) -> None:
        self.heros: Dict[int, Hero] = {}
        self.ships: Dict[int, Ship] = {}

    def get_hero(self, id: ID) -> Hero:
        return self.heros[id]

    def save_hero(self, hero: Hero) -> None:
        self.heros[hero.id] = hero

    def get_ship(self, id: ID) -> Ship:
        return self.ships[id]

    def save_ship(self, ship: Ship) -> None:
        self.ships[ship.id] = ship

    def clear(self) -> None:
        self.heros = {}
        self.ships = {}

    @staticmethod
    def build() -> "Dataset":
        last_ship_id = 1
        dataset = Dataset()

        for hero_id in range(1, 21):
            ship_ids = [last_ship_id + n for n in range(3)]
            for ship_id in ship_ids:
                dataset.save_ship(Ship(id=ship_id, name=f"Ship-{ship_id}"))

            dataset.save_hero(
                Hero(id=hero_id, name=f"Hero-{hero_id}", own_ships=ship_ids)
            )

            last_ship_id = ship_ids[-1]

        return dataset


dataset = Dataset.build()


class HeroLoader(DataLoader):
    async def batch_load_fn(self, keys: Sequence[ID]) -> ListType[Hero]:
        heros = map(lambda key: dataset.get_hero(key), keys)
        return list(heros)


hero_loader = HeroLoader()


class ShipLoader(DataLoader[int, Ship]):
    async def batch_load_fn(self, keys: Sequence[ID]) -> ListType[Ship]:
        ships = map(lambda key: dataset.get_ship(key), keys)
        return list(ships)


ship_loader = ShipLoader()


class Query(ObjectType):
    hero = Field(Hero, id=Argument(ID, required=True))

    @staticmethod
    async def resolve_hero(parent: Literal[None], info: ResolveInfo, id: ID) -> Hero:
        return await hero_loader.load(int(id))


"""
定义 schema 结构

对应的 GraphQL 定义为

```
schema {
    query: Query
}
```
"""
schema = Schema(query=Query)
