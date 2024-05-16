from typing import Dict, Literal

from graphene import (
    ID,
    Argument,
    ClientIDMutation,
    Field,
    InputObjectType,
    ObjectType,
    ResolveInfo,
    Schema,
    String,
)


class Ship(ObjectType):
    """定义表示 Ship 的实体类型"""

    id = ID(required=True)

    # 飞船名称
    name = String(required=True)

    # 飞船所属的派系
    faction = Field(lambda: Faction)

    @staticmethod
    def resolve_faction(parent: "Ship", info: ResolveInfo) -> "Faction":
        """解析和当前 Ship 关联的 Faction 对象"""
        return dataset.get_faction(parent.faction)


class Faction(ObjectType):
    """定义表示 Faction 的实体类型"""

    id = ID(required=True)

    # 派系名称
    name = String(required=True)


class Dataset:
    """数据集类型"""

    def __init__(self) -> None:
        self.ships: Dict[int, Ship] = {}
        self.factions: Dict[str, Faction] = {}

    def clear(self) -> None:
        self.ships = {}
        self.factions = {}

    def get_ship(self, id: int) -> Ship:
        return self.ships[id]

    def get_faction(self, id: str) -> Faction:
        return self.factions[id]

    def save_ship(self, ship: Ship) -> None:
        self.ships[ship.id] = ship

    def save_faction(self, faction: Faction) -> None:
        self.factions[faction.id] = faction

    @staticmethod
    def build() -> "Dataset":
        """构建数据集对象"""
        dataset = Dataset()

        for name in [
            "Galactic Republic",
            "Separatist Alliance",
            "Galactic Empire",
            "Rebel Alliance",
            "New Republic",
        ]:
            dataset.save_faction(Faction(name.lower().replace(" ", "_"), name))

        return dataset


# 实例化数据集对象
dataset = Dataset.build()


def create_ship(ship_name: str, faction_id: str) -> Ship:
    """创建一个 Ship 对象并存入数据集中"""
    ship = Ship(id=len(dataset.ships) + 1, name=ship_name, faction=faction_id)
    dataset.save_ship(ship)
    return ship


def create_faction(faction_key: int, faction_name: str) -> Faction:
    """创建一个 Faction 对象并存入数据集中"""
    faction = Faction(id=faction_key, name=faction_name)
    dataset.save_faction(faction)
    return faction


class Query(ObjectType):
    """Graphql 查询类型"""

    # 飞船属性
    ship = Field(Ship, id=Argument(ID, required=True))

    @staticmethod
    def resolve_ship(parent: Literal[None], info: ResolveInfo, id: ID) -> Ship:
        """解析飞船属性"""
        return dataset.get_ship(int(id))


class ShipInput(InputObjectType):
    """输入类型, 输入一个飞船的属性"""

    # 飞船名称
    ship_name = String(required=True)

    # 飞船的派系 ID
    faction_id = ID(required=True)


class IntroduceShipMutation(ClientIDMutation):
    """`ClientIDMutation` 表示一个 Update 和 Query 一次性执行的 Mutation 操作"""

    class Input:
        """表示输入的参数, 类似于 `Mutation` 的 `Arguments`"""

        ship_name = String(required=True)
        faction_id = ID(required=True)

    # 返回客户端的属性
    ship = Field(Ship)
    faction = Field(Faction)

    @staticmethod
    def mutate_and_get_payload(
        parent: Literal[None],
        info: ResolveInfo,
        ship_name: str,
        faction_id: str,
    ) -> "IntroduceShipMutation":
        """创建指定对象并返回一个查询结果"""
        ship = create_ship(ship_name, faction_id)
        faction = dataset.get_faction(faction_id)
        return IntroduceShipMutation(ship=ship, faction=faction)


class Mutation(ObjectType):
    """Mutation 操作类型"""

    introduce_ship = IntroduceShipMutation.Field()


schema = Schema(query=Query, mutation=Mutation)
