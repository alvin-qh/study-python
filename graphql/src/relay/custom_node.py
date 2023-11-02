import time
from datetime import datetime
from typing import Dict
from typing import List as ListType
from typing import Optional, Self, cast

from aiodataloader import DataLoader
from graphene import ID, DateTime, Field, Node, ObjectType, ResolveInfo, Schema, String


class CustomNode(Node):
    """自定义 `Node` 类型

    自定义 `Node` 类型主要是为了解决 Global ID 的编码和解析

    默认情况下, `Node` 接口通过 "类型名:原始ID值" 组合并进行 Base64 编码,
    如果要采用其它方式产生 Global ID, 则需要自定义 `Node` 类型
    """

    class Meta:
        """
        定义实体类型的元类型
        """

        # 设定实体类型名称
        name = "Node"

    @staticmethod
    def to_global_id(type: str, id: str) -> str:
        """将实体类型和实体对象 ID 转为 Global ID

        Args:
            type (str): 实体类型名称
            id (str): 实体对象 ID

        Returns:
            str: 全局 ID (Global ID)
        """
        return f"{type}:{id}"

    @staticmethod
    def get_node_from_global_id(
        info: ResolveInfo,
        global_id: str,
        only_type: Optional[ObjectType] = None,
    ) -> Node:
        """通过 Global ID 获取 `Node` 类型实体对象

        Args:
            info (ResolveInfo): 查询上下文对象
            global_id (str): 全局 ID
            only_type (Optional[ObjectType], optional): 实体类型. Defaults to `None`.

        Returns:
            Node: 实体对象
        """
        type_name, id_ = global_id.split(":", 1)
        if only_type:
            assert type_name == only_type._meta.name

        type_ = info.schema.get_type(type_name)
        assert type_ is not None

        return type_.graphene_type.get_node(info, id_)


class User(ObjectType):
    """定义用户实体类型

    对应的 GraphQL 定义如下:

    ```graphql
    type User implements Node {
        name: String!
    }
    ```
    """

    class Meta:
        """定义实体类型元类型, 指定所实现的接口"""

        interfaces = (CustomNode,)

    # 名字字段
    name = String(required=True)

    @classmethod
    async def get_node(cls, info: ResolveInfo, id: ID) -> Self:
        """根据 `id` 获取当前实体对象

        Args:
            info (ResolveInfo): 上下文对象
            id (ID): 实体对象的 ID

        Returns:
            User: 返回实体对象
        """
        loader = cast(UserLoader, info.context.user_loader)
        return await loader.load(int(id))


class Photo(ObjectType):
    """照片实体对象

    对应的 GraphQL 定义如下:

    ```
    type Photo implements Node {
        forUser: User!
        datetime: DateTime!
    }
    ```
    """

    class Meta:
        """元类型, 指定实体类型所实现的接口"""

        interfaces = (CustomNode,)

    # 用户字段, 表示照片为谁拍摄
    for_user = Field(User, required=True)

    # 时间日期字段, 表示照片拍摄的时间
    datetime = DateTime(required=True)

    @staticmethod
    async def resolve_for_user(parent: "Photo", info: ResolveInfo) -> User:
        """解析 `for_user` 字段

        Args:
            parent (Photo): 当前实体对象
            info (ResolveInfo): 上下文对象

        Returns:
            User: 返回 `User` 实体对象
        """
        loader: UserLoader = info.context.user_loader
        return await loader.load(int(parent.for_user))

    @classmethod
    async def get_node(cls, info: ResolveInfo, id: ID) -> Self:
        """根据 ID 获取当前实体类型对象

        Args:
            info (ResolveInfo): 上下文对象
            id (ID): 实体对象 ID

        Returns:
            Photo: 返回当前类型实体对象
        """
        loader = cast(PhotoLoader, info.context.photo_loader)
        return await loader.load(int(id))


class UserLoader(DataLoader[int, User]):
    """用户实体对象的 Loader 类"""

    async def batch_load_fn(self, keys: ListType[ID]) -> ListType[User]:
        """
        批量读取实体对象

        Args:
            keys (ListType[ID]): 实体对象的 ID 集合

        Returns:
            ListType[User]: `User` 实体对象列表集合
        """
        users = map(lambda key: dataset.get_user(int(key)), keys)
        return list(users)


class PhotoLoader(DataLoader[int, Photo]):
    """照片实体对象 Loader 类"""

    async def batch_load_fn(self, keys: ListType[ID]) -> ListType[Photo]:
        """
        批量读取实体对象

        Args:
            keys (ListType[ID]): 实体对象 ID 集合

        Returns:
            ListType[Photo]: `Photo` 实体对象集合
        """
        photos = map(lambda key: dataset.get_photo(int(key)), keys)
        return list(photos)


class Dataset:
    """数据集类型"""

    users: Dict[int, User]
    photos: Dict[int, Photo]

    def __init__(self) -> None:
        self.users = {}
        self.photos = {}

    def get_user(self, id: int) -> User:
        """根据用户 ID 获取用户实体对象

        Args:
            id (str): 用户 ID

        Returns:
            User: 用户实体对象
        """
        return self.users[id]

    def get_photo(self, id: int) -> Photo:
        """根据 ID 获取照片实体对象

        Args:
            id (int): 照片 ID

        Returns:
            Photo: 照片实体对象
        """
        return self.photos[id]

    def save_user(self, user: User) -> None:
        """保存用户实体对象

        Args:
            user (User): 用户实体对象
        """
        self.users[user.id] = user

    def save_photo(self, photo: Photo) -> None:
        """存储照片实体对象

        Args:
            photo (Photo): 照片实体对象
        """
        self.photos[photo.id] = photo

    def user_count(self) -> int:
        """获取用户数量

        Returns:
            int: 用户数量
        """
        return len(self.users)

    @staticmethod
    def build() -> "Dataset":
        """构建数据集对象"""
        dataset = Dataset()

        # 设置 User 对象集合
        for id in range(1, 21):
            dataset.save_user(
                User(
                    id=id,
                    name=f"User-{id}",
                )
            )

        start_date = int(
            time.mktime(time.strptime("2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"))
        )

        # 设置 Photo 对象集合
        for id in range(1, 21):
            dataset.save_photo(
                Photo(
                    id=id,
                    for_user=dataset.user_count() - 1 - id,
                    datetime=datetime.fromtimestamp(start_date),
                )
            )
            start_date += 1

        return dataset


# 生成数据集对象
dataset = Dataset.build()


class Query(ObjectType):
    """查询实体类型

    对应的 GraphQL 定义如下:

    ```
    type Query {
        user: User
    }
    ```
    """

    # 查询用户
    user = CustomNode.Field(User)
    # 查询图片
    photo = CustomNode.Field(Photo)
    # 查询 Node 对象
    node = CustomNode.Field()


"""定义 schema 结构

对应的 GraphQL 定义为

```
schema {
    query: Query
}
```
"""
schema = Schema(query=Query)
