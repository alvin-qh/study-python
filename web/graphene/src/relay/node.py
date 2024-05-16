from typing import Dict, Iterable
from typing import List as ListType
from typing import Literal, Self

from aiodataloader import DataLoader
from graphene import ID, Field, Node, ObjectType, ResolveInfo, Schema, String


class Ship(ObjectType):
    """定义实体类型, 该实体类型从 `Node` 接口继承

    `Node` 接口包含 `id` 字段, `id` 字段为 `String` 类型, 保存一个 base64 编码的 ID',
    也称为 Global ID, 即统一 ID

    默认情况下, `Node` 类型的 `id` 属性值为 `类型名:原始ID值`,
    例如一个 `Ship` 类型对象的原始ID值为 `10`, 则 `Node` 类型的 `id` 值应该为 `Ship:10`

    对应的 GraphQL 定义如下:

    ```
    type Ship implements Node {
        name: String!
    }
    ```
    """

    class Meta:
        """指定 `interfaces` 接口集合, 从 `Node` 接口继承"""

        interfaces = (Node,)

    # name 字段, 字符串类型
    name = String(required=True)

    @classmethod
    async def get_node(cls, info: ResolveInfo, id: ID) -> Self:
        """根据 `id` 获取对应当前对象

        该方法为协程异步方法

        Args:
            info (ResolveInfo): 保存上下文对象
            id (ID): 固定参数, 表示获取实体对象的 `id`

        Returns:
            Ship: 根据 ID 获取的 `Ship` 类型实体对象
        """
        # 从上下文对象中获取 ShipLoader 对象
        loader: ShipLoader = info.context.ship_loader

        # 从 loader 对象中根据 id 读取实体对象
        return await loader.load(int(id))


class Dataset:
    """数据集类型"""

    ships: Dict[int, Ship]

    def __init__(self) -> None:
        """初始化数据集对象"""
        self.ships = {}

    def get_ship(self, id: int) -> Ship:
        """从数据集中获取 `Ship` 类型实体对象

        Args:
            id (int): 对象 ID

        Returns:
            Ship: 实体对象
        """
        return self.ships[id]

    def save_ship(self, ship: Ship) -> None:
        """将 `Ship` 类型实体对象保存到数据集中

        Args:
            ship (Ship): `Ship` 实体对象
        """
        self.ships[ship.id] = ship

    @staticmethod
    def build() -> "Dataset":
        """构建测试数据集

        Returns:
            Dataset: 数据集对象
        """
        # 实例化数据集对象
        ds = Dataset()

        # 将 50 个实体对象存储到数据集中
        for id in range(1, 51):
            ds.save_ship(
                Ship(
                    id=id,
                    name=f"Ship-{id}",
                ),
            )

        # 返回数据集对象
        return ds


class ShipLoader(DataLoader[int, Ship]):
    """`Ship` 类型实体对象的数据读取器"""

    # 获取数据集对象
    dataset = Dataset.build()

    async def batch_load_fn(self, keys: Iterable[ID]) -> ListType[Ship]:
        """批量读取 `Ship` 类型实体对象

        Args:
            keys (Iterable[ID]): `Ship` 实体对象的 `ID` 集合

        Returns:
            ListType[Ship]: `Ship` 类型实体对象的集合
        """
        # 从数据集中读取实体对象集合
        ships = map(lambda key: self.dataset.get_ship(key), keys)

        # 返回实体对象的列表集合
        return list(ships)


class Query(ObjectType):
    """查询类型

    对应的 GraphQL 定义如下:

    ```
    type Query {
        ship(id: ID!): Ship!
        shipNode(id: ID!): Ship!
        node(id: ID!): Node!
    }
    ```
    """

    # Ship 实体类型字段
    ship = Field(Ship, id=ID(required=True), required=True)

    # Ship 类型的 Node 实体字段
    # 该字段通过 Ship 类型的 get_node 方法解析
    ship_node = Node.Field(Ship, required=True)

    # Node 接口类型字段
    # 该字段通过 Ship 类型的 get_node 方法解析
    node = Node.Field(required=True)

    @staticmethod
    async def resolve_ship(
        parent: Literal[None],
        info: ResolveInfo,
        id: ID,
    ) -> Ship:
        """解析 `ship` 字段

        Args:
            info (ResolveInfo): 包含上下文对象的参数
            id (ID): 实体对象的 `ID`

        Returns:
            Ship: 实体对象
        """
        # 从上下文对象中获取 ShipLoader 对象
        loader: ShipLoader = info.context.ship_loader

        # 从 loader 对象中根据 id 读取实体对象
        return await loader.load(int(id))


"""定义 schema 结构

对应的 GraphQL 定义为

```
schema {
    query: Query
}
```
"""
schema = Schema(query=Query)
