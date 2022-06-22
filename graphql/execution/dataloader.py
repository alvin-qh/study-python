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

    对应的 GraphQL 定义如下:

    ```
    type User {
        id: ID!
        name: String!
        friends: [User]
        bestFriend: User
    }
    ```
    """
    id = ID(required=True)  # id 字段
    name = String(required=True)  # 姓名字段
    friends = List(lambda: User)  # 该实体关联的伙伴集合字段
    best_friend = Field(lambda: User)  # 该实体关联的最佳伙伴对象

    @staticmethod
    async def resolve_friends(parent: "User", info: ResolveInfo) -> ListType["User"]:
        """
        使用异步的 dataloader 读取 `User` 实体相关的朋友实体列表

        数据集中, `friends` 字段存储的是朋友实体的 ID 列表, 当前方法将其转换为 `List[User]` 实体对象集合

        Args:
            parent (User): 当前解析依赖的 `User` 实体对象

        Returns:
            ListType["User"]: 返回查询到的 `User` 类型集合
        """
        # 从 dataloader 中读取多条数据
        # 使用 Python 的异步操作语法, 等待调用返回
        return await user_loader.load_many(parent.friends)

    @staticmethod
    async def resolve_best_friend(parent: "User", info: ResolveInfo) -> "User":
        """
        使用异步的 dataloader 读取 `User` 实体相关的朋友实体对象

        数据集中, `best_friend` 字段存储的是朋友实体的 ID 值, 当前方法将其转换为 `User` 实体对象

        Args:
            parent (User): 当前解析依赖的 `User` 实体对象

        Returns:
            User: 返回查询到的 `User` 实体
        """
        # 从 dataloader 中读取一条数据
        # 使用 Python 的异步操作语法, 等待调用返回
        return await user_loader.load(parent.best_friend)


class Dataset:
    """
    数据集类型, 记录 `User` 实体对象集合
    """
    users: Dict[int, User]

    def __init__(self):
        """
        实例化数据集对象
        """
        self.users = {}  # 存储用户实体的字典对象

    def save_user(self, user: User) -> None:
        """
        在数据集中保存一个用户实体对象

        Args:
            user (User): 要保存的用户实体对象
        """
        self.users[user.id] = user

    def get_user(self, id: int) -> User:
        """
        从数据集中读取一个用户实体对象

        Args:
            id (int): 用户实体的 id

        Returns:
            User: 相关的用户实体对象
        """
        return self.users[id]

    @staticmethod
    def build() -> "Dataset":
        """
        构建一个数据集
        """
        # 数据集对象
        dataset = Dataset()

        def make_friend_ids(user_id: int, all_user_ids: ListType[int], friends_count=4) -> ListType[int]:
            """
            构建朋友列表

            Args:
                user_id (int): 当前用户实体 ID
                max_friends (int, optional): 朋友数量. Defaults to 4.

            Returns:
                ListType[int]: 朋友列表集合
            """
            # 从全体用户中随机抽取 friends_count 个 ID 作为朋友 ID 集合
            friend_ids = random.sample(all_user_ids, friends_count)
            # 筛选掉当前用户, 构建朋友 ID 列表集合
            return [id_ for id_ in friend_ids if id_ != user_id]

        def choose_best_friend_id(friend_ids: ListType[int]) -> int:
            """
            从朋友 ID 列表中选择一个作为最好朋友

            Args:
                friend_ids (ListType[int]): 朋友 ID 列表集合

            Returns:
                int: 最好朋友 ID
            """
            return friend_ids[random.randint(0, len(friend_ids) - 1)]

        # 随机构建 100 个用户 ID
        all_user_ids = list(range(1, 101))

        for id in all_user_ids:
            # 随机选择 4 个 ID 作为用户实体的朋友关联
            friend_ids = make_friend_ids(id, all_user_ids)
            # 随机从朋友列表中选择一名最好的朋友
            best_friend_id = choose_best_friend_id(friend_ids)

            # 创建用户实体并存储到数据集
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

        该方法为异步协程方法, 返回一个 `Future` 对象, 异步读取数据.

        所有使用 `DataLoader` 对象的场合, 需要用 `await` 关键字标识为异步调用

        Args:
            keys (Iterable[ID]): Key 集合迭代器对象

        Returns:
            Promise[List[User]]: 一个异步处理对象, 可获取 `User` 实体类对象集合
        """
        users = map(lambda key: dataset.get_user(int(key)), keys)
        return list(users)


# 实例化 DataLoader 对象
user_loader = UserLoader()


class Query(ObjectType):
    """
    查询类型

    对应的 GraphQL 定义如下:

    ```
    type Query {
        user(id: ID!): User
    }
    ```
    """
    # 定义 `user` 字段, 对应 `User` 实体
    user = Field(User, id=Argument(ID, required=True))

    @staticmethod
    def resolve_user(parent: Literal[None], info: ResolveInfo, id: ID) -> User:
        """
        解析 `user` 字段, 返回 `User` 实体对象

        Args:
            id (ID): `User` 实体的 ID 值

        Returns:
            User: `User` 实体对象
        """
        return user_loader.load(int(id))


"""
定义 schema 结构, 指定根查询对象

对应的 GraphQL 定义为

```
schema {
    query: Query
}
```
"""
schema = Schema(query=Query)
