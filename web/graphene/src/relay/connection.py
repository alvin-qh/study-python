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
    """表示 Ship 的 Graphql 类型"""

    id = ID(required=True)
    name = String(required=True)


T = TypeVar("T")


class QueryResult(PageInfo, Generic[T]):
    """保存查询结果的类型, 记录一页的数据以及分页信息"""

    # 为继承 `Generic` 类打的补丁
    __parameters__ = ("~T",)

    def __init__(self, data: ListType[T], start: int, end: int, count: int) -> None:
        self._data = data
        self.start = start
        self.end = end
        self.count = count

    @property
    def start_cursor(self) -> int:
        """获取起始游标值

        Returns:
            int: 游标值
        """
        return self.start

    @property
    def end_cursor(self) -> int:
        """获取终止游标值

        Returns:
            int: 游标值
        """
        return self.end

    @property
    def has_next_page(self) -> bool:
        """是否有下一页

        Returns:
            bool: 是否有下一页
        """
        return self.end < self.count

    @property
    def has_previous_page(self) -> bool:
        """是否有上一页

        Returns:
            bool: 是否有上一页
        """
        return self.start > 0

    @property
    def data(self) -> ListType[T]:
        """获取一页的数据

        Returns:
            ListType[T]: 一页数据的集合
        """
        return self._data


class ShipConnection(Connection):
    """`Ship` 类型的连接类型, 用于获取 `Hero` 关联的 `Ship` 集合"""

    class Meta:
        """`Connection` 类型的元数据类, 设定 node 的类型"""

        node = Ship

    class Edge:
        """设置 `Connection` 中的元素"""

        # 增加 link 属性, 表示一个链接地址
        link = String()

        def __init__(self, **kwargs: Any) -> None:
            """占位方法, 不会被调用"""

    # 表示全部数据数量的属性
    total_count = Int()

    def __init__(self, query_result: QueryResult[Ship]) -> None:
        """构造器

        Args:
            query_result (QueryResult[Ship]): 表示一页查询结果数据集合
        """
        self.query_result = query_result

    def resolve_page_info(self, info: ResolveInfo) -> PageInfo:
        """解析页信息属性

        Args:
            info (ResolveInfo): 解析上下文对象

        Returns:
            PageInfo: 页信息对象
        """
        return self.query_result

    def resolve_total_count(self, info: ResolveInfo) -> int:
        """解析总记录数属性

        Args:
            info (ResolveInfo): 解析上下文对象

        Returns:
            int: 总记录数
        """
        return self.query_result.count

    def resolve_edges(self, info: ResolveInfo) -> ListType[Edge]:
        """解析 `edges` 属性

        Args:
            info (ResolveInfo): 解析上下文对象

        Returns:
            ListType[Edge]: Edge 对象集合
        """
        start = self.query_result.start
        return [
            self.Edge(cursor=start + n, node=d, link=f"https://myapp.com/data/{d.id}")
            for n, d in enumerate(self.query_result.data)
        ]


class Hero(ObjectType):
    """表示 Hero 的 Graphql 类型"""

    id = ID(required=True)
    name = String(required=True)
    own_ships = ConnectionField(ShipConnection)

    @staticmethod
    async def resolve_own_ships(
        parent: "Hero", info: ResolveInfo, **kwargs: Any
    ) -> ShipConnection:
        """
        Resolve "own_ships" field, return "ShipConnection" object
        """
        # 计算起始游标值
        first = max(cast(int, kwargs.get("first", 0)), 0)
        # 计算结束游标值
        last = min(
            cast(int, kwargs.get("last", len(parent.own_ships) - 1)),
            len(parent.own_ships) - 1,
        )

        # 根据游标值读取 ShipModel 集合
        data = await ship_loader.load_many(parent.own_ships[first: last + 1])

        # 生成查询结果对象
        result = QueryResult(data, first, last, len(data))
        return ShipConnection(result)


class Dataset:
    """数据集类型, 用于存储 Hero 和 Ship 对象集合"""

    def __init__(self) -> None:
        """构造器"""
        self.heros: Dict[int, Hero] = {}
        self.ships: Dict[int, Ship] = {}

    def get_hero(self, id_: int) -> Hero:
        """获取 `HeroModel` 实体对象

        Args:
            id_ (int): 实体主键

        Returns:
            HeroModel: 实体对象
        """
        return self.heros[id_]

    def save_hero(self, hero: Hero) -> None:
        """存储 `HeroModel` 实体对象

        Args:
            hero (HeroModel): 实体对象
        """
        self.heros[hero.id] = hero

    def get_ship(self, id_: int) -> Hero:
        """获取 `ShipModel` 实体对象

        Args:
            id_ (int): 实体主键

        Returns:
            ShipModel: 实体对象
        """
        return self.ships[id_]

    def save_ship(self, ship: Ship) -> None:
        """存储 `ShipModel` 实体对象

        Args:
            ship (ShipModel): 实体对象
        """
        self.ships[ship.id] = ship

    def clear(self) -> None:
        """清空数据集"""
        self.heros = {}
        self.ships = {}

    @staticmethod
    def build() -> "Dataset":
        """构建数据集

        Returns:
            Dataset: 数据集对象
        """
        last_ship_id = 1
        dataset = Dataset()

        for hero_id in range(1, 21):
            # 为每个 Hero 实体关联 3 个 Ship 实体对象
            ship_ids = [last_ship_id + n for n in range(3)]
            for ship_id in ship_ids:
                dataset.save_ship(Ship(id=ship_id, name=f"Ship-{ship_id}"))

            dataset.save_hero(
                Hero(id=hero_id, name=f"Hero-{hero_id}", own_ships=ship_ids)
            )

            last_ship_id = ship_ids[-1]

        return dataset


# 构建数据集对象
dataset = Dataset.build()


class HeroLoader(DataLoader[int, Hero]):
    """`HeroModel` 对象的读取器"""

    async def batch_load_fn(self, keys: Sequence[ID]) -> ListType[Hero]:
        """批量读取 `HeroModel` 实体对象

        Args:
            keys (Sequence[ID]): 实体主键集合

        Returns:
            ListType[HeroModel]: 实体对象集合
        """
        heros = map(lambda key: dataset.get_hero(int(key)), keys)
        return list(heros)


# 构建数据读取器对象
hero_loader = HeroLoader()


class ShipLoader(DataLoader[int, Ship]):
    """`ShipModel` 对象的读取器"""

    async def batch_load_fn(self, keys: Sequence[ID]) -> ListType[Ship]:
        """批量读取 `ShipModel` 实体对象

        Args:
            keys (Sequence[ID]): 实体主键集合

        Returns:
            ListType[ShipModel]: 实体对象集合
        """
        ships = map(lambda key: dataset.get_ship(int(key)), keys)
        return list(ships)


# 构建数据读取器对象
ship_loader = ShipLoader()


class Query(ObjectType):
    """查询 Graphql 查询类型"""

    hero = Field(Hero, id=Argument(ID, required=True))

    @staticmethod
    async def resolve_hero(parent: Literal[None], info: ResolveInfo, id: ID) -> Hero:
        """
        Args:
            parent (Literal[None]): 上一级 Graphql 对象
            info (ResolveInfo): 解析上下文对象

        Returns:
            HeroModel: 实体对象
        """
        return await hero_loader.load(int(id))


"""定义 schema 结构

对应的 GraphQL 定义为

```
schema {
    query: Query
}
```
"""
schema = Schema(query=Query)
