import datetime
import time
from typing import Any, Dict
from typing import List as ListType
from typing import Type, cast

from aiodataloader import DataLoader
from graphene import (ID, DateTime, Field, Node, ObjectType, ResolveInfo,
                      Schema, String)


class UserModel:
    """
    定义模型类型, 表示一个用户
    """
    id: int
    name: str

    def __init__(self, **kwargs) -> None:
        """
        初始化对象
        """
        self.id = kwargs["id"]
        self.name = kwargs["name"]


class PhotoModel:
    """
    定义模型类型, 表示一张照片
    """
    id: int
    for_user_id: int
    datetime: datetime.datetime

    def __init__(self, **kwargs) -> None:
        """
        初始化对象
        """
        self.id = kwargs["id"]
        self.for_user_id = kwargs["for_user_id"]
        self.datetime = kwargs["datetime"]


class Dataset:
    """
    数据集类型
    """
    users: Dict[int, UserModel]
    photos: Dict[int, PhotoModel]

    def __init__(self) -> None:
        self.users = {}
        self.photos = {}

    def get_user(self, id: int) -> UserModel:
        """
        根据用户 ID 获取用户实体对象

        Args:
            id (str): 用户 ID

        Returns:
            User: 用户实体对象
        """
        return self.users[id]

    def get_photo(self, id: int) -> PhotoModel:
        """
        根据 ID 获取照片实体对象

        Args:
            id (int): 照片 ID

        Returns:
            Photo: 照片实体对象
        """
        return self.photos[id]

    def save_user(self, user: UserModel) -> None:
        """
        保存用户实体对象

        Args:
            user (User): 用户实体对象
        """
        self.users[user.id] = user

    def save_photo(self, photo: PhotoModel) -> None:
        """
        存储照片实体对象

        Args:
            photo (Photo): 照片实体对象
        """
        self.photos[photo.id] = photo

    def user_count(self) -> int:
        """
        获取用户数量

        Returns:
            int: 用户数量
        """
        return len(self.users)

    @staticmethod
    def build() -> "Dataset":
        dataset = Dataset()

        # 设置 User 对象集合
        for id in range(1, 21):
            dataset.save_user(
                UserModel(
                    id=id,
                    name=f"User-{id}",
                )
            )

        start_date = int(
            time.mktime(
                time.strptime("2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
            )
        )

        # 设置 Photo 对象集合
        for id in range(1, 21):
            dataset.save_photo(
                PhotoModel(
                    id=id,
                    for_user_id=dataset.user_count() - 1 - id,
                    datetime=datetime.datetime.fromtimestamp(start_date),
                )
            )
            start_date += 1

        return dataset


# 生成数据集对象
dataset = Dataset.build()


class UserModelLoader(DataLoader):
    """
    用户模型对象的 Loader 类
    """

    async def batch_load_fn(self, keys: ListType[int]) -> ListType[UserModel]:
        """
        批量读取模型对象

        Args:
            keys (ListType[int]): 模型对象 id 集合

        Returns:
            ListType[UserModel]: `UserModel` 模型对象列表集合
        """
        users = map(lambda key: dataset.get_user(int(key)), keys)
        return list(users)


class PhotoModelLoader(DataLoader):
    """
    照片模型对象 Loader 类
    """

    async def batch_load_fn(self, keys: ListType[int]) -> ListType[PhotoModel]:
        """
        批量读取实体对象

        Args:
            keys (ListType[ID]): 模型对象 id 集合

        Returns:
            ListType[Photo]: `Photo` 实体对象集合
        """
        photos = map(lambda key: dataset.get_photo(int(key)), keys)
        return list(photos)


class CustomNode(Node):
    """
    自定义 `Node` 类型, 可以同时表示多种实体类型
    """
    class Meta:
        name = "Node"

    @classmethod
    def resolve_type(cls, instance: Any, info: ResolveInfo) -> Type:
        """
        解析当前 `Node` 对象的类型

        Args:
            instance (Any): `Node` 对象实例
            info (ResolveInfo): 查询上下文对象

        Returns:
            Type: 返回当前 `Node` 对象可支持的类型
        """
        if isinstance(instance, (User, UserModel)):
            return User

        if isinstance(instance, (Photo, PhotoModel)):
            return Photo

        return type(instance)


class User(ObjectType):
    """
    定义实体对象, 表示用户
    """
    class Meta:
        # 继承 CustomNode 接口
        interfaces = (CustomNode,)

    name = String(required=True)

    @classmethod
    async def get_node(cls, info: ResolveInfo, id: ID) -> UserModel:
        """
        根据 ID 获取当前实体对应的模型对象

        Args:
            info (ResolveInfo): 查询上下文对象
            id (ID): 模型对象 ID

        Returns:
            UserModel: 模型对象
        """
        loader = cast(UserModelLoader, info.context.user_model_loader)
        return await loader.load(int(id))


class Photo(ObjectType):
    """
    定义实体对象, 表示照片
    """
    class Meta:
        # 继承 CustomNode 接口
        interfaces = (CustomNode,)

    for_user = Field(User, required=True)
    datetime = DateTime(required=True)

    @staticmethod
    async def resolve_for_user(parent: PhotoModel, info: ResolveInfo) -> UserModel:
        """
        解析 `for_user` 字段

        Args:
            parent (PhotoModel): 当前查询的模型对象
            info (ResolveInfo): 查询上下文对象

        Returns:
            UserModel: 用户模型对象
        """
        loader = cast(UserModelLoader, info.context.user_model_loader)
        return await loader.load(int(parent.for_user_id))

    @classmethod
    async def get_node(cls, info: ResolveInfo, id: ID) -> PhotoModel:
        """
        根据 ID 获取当前实体对应的模型对象

        Args:
            info (ResolveInfo): 查询上下文对象
            id (ID): 模型对象 id

        Returns:
            PhotoModel: 模型对象
        """
        loader = cast(PhotoModelLoader, info.context.photo_model_loader)
        return await loader.load(int(id))


class Query(ObjectType):
    """
    定义查询实体类型
    """
    user = CustomNode.Field(User)
    photo = CustomNode.Field(Photo)
    node = CustomNode.Field()


schema = Schema(query=Query)
