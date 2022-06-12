import random
from typing import Dict, Iterable
from typing import List as ListType
from typing import Literal

from aiodataloader import DataLoader
from graphene import (ID, Argument, Field, List, ObjectType, ResolveInfo,
                      Schema, String)


class User(ObjectType):
    """
    定义实体类型
    """
    id = ID(required=True)  # id 字段
    name = String(required=True)  # 姓名字段
    friends = List(lambda: User)  # 该实体关联的伙伴集合字段
    best_friend = Field(lambda: User)  # 该实体关联的最佳伙伴对象

    @staticmethod
    async def resolve_friends(parent: "User", info: ResolveInfo) -> ListType["User"]:
        return await user_loader.load_many(parent.friends)

    @staticmethod
    async def resolve_best_friend(parent: "User", info: ResolveInfo) -> "User":
        return await user_loader.load(parent.best_friend)


class Dataset:
    """
    数据集类型, 记录 `User` 实体对象集合
    """
    users: Dict[int, User]

    def __init__(self):
        self.users = {}

    def save_user(self, user: User) -> None:
        self.users[user.id] = user

    def get_user(self, id: int) -> User:
        return self.users[id]

    @staticmethod
    def build() -> "Dataset":
        dataset = Dataset()

        for id in range(1, 101):
            friend_ids = [
                n for n in random.sample(
                    range(0, 101), 4,
                ) if n != id
            ]
            best_friend_id = friend_ids[random.randint(0, len(friend_ids) - 1)]

            dataset.save_user(
                User(
                    id=id,
                    name=f"user-{id}",
                    friends=friend_ids,
                    best_friend=best_friend_id,
                )
            )

        return dataset


# 数据集对象
dataset = Dataset.build()


class UserLoader(DataLoader):
    """
    定义 `User` 类型的 Loader 类型
    """
    async def batch_load_fn(self, keys: Iterable[ID]) -> ListType[User]:
        """
        重写 `DataLoader` 的批量读方法, 根据一个 Key 集合批量读取实例对象集合

        Args:
            keys (Iterable[ID]): Key 集合迭代器对象

        Returns:
            Promise[ListType[User]]: 一个异步处理对象, 可获取 `User` 实体类对象集合
        """
        users = map(lambda key: dataset.get_user(int(key)), keys)
        return list(users)


# 实例化 DataLoader 对象
user_loader = UserLoader()


class Query(ObjectType):
    user = Field(User, id=Argument(ID, required=True))

    @staticmethod
    async def resolve_user(parent: Literal[None], info: ResolveInfo, id: ID) -> User:
        return await user_loader.load(int(id))


schema = Schema(query=Query)


def test_data_loader() -> None:
    query = """
        query getUser($id: ID!) {
            user(id: $id) {
                id
                name
                friends {
                    __typename
                    id
                    name
                }
                bestFriend {
                    __typename
                    id
                    name
                }
            }
        }
    """

    vars = {"id": random.randint(1, 100)}

    r = schema.execute(query, variables=vars)
    assert r.errors is None
