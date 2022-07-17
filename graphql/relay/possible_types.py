import datetime
import time
from typing import Dict

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


class User(ObjectType):
    """
    定义实体对象, 表示用户
    """
    class Meta:
        # 继承 Node 接口
        interfaces = (Node,)
        # 定义当前 Node 接口可能表示的类型
        # possible_types = (UserModel,)

    name = String(required=True)

    @classmethod
    def get_node(cls, info: ResolveInfo, id: ID) -> UserModel:
        """
        根据 ID 获取当前实体对应的模型对象

        Args:
            info (ResolveInfo): 查询上下文对象
            id (ID): 模型对象 ID

        Returns:
            UserModel: 模型对象
        """
        return dataset.get_user(int(id))


class Photo(ObjectType):
    """
    定义实体对象, 表示照片
    """
    class Meta:
        # 继承 CustomNode 接口
        interfaces = (Node,)
        # 定义当前 Node 接口可能表示的类型
        possible_types = (PhotoModel,)

    for_user = Field(User, required=True)
    datetime = DateTime(required=True)

    @staticmethod
    def resolve_for_user(parent: PhotoModel, info: ResolveInfo) -> UserModel:
        """
        解析 `for_user` 字段

        Args:
            parent (PhotoModel): 当前查询的模型对象
            info (ResolveInfo): 查询上下文对象

        Returns:
            UserModel: 用户模型对象
        """
        return dataset.get_user(int(parent.for_user_id))

    @classmethod
    def get_node(cls, info: ResolveInfo, id: ID) -> PhotoModel:
        """
        根据 ID 获取当前实体对应的模型对象

        Args:
            info (ResolveInfo): 查询上下文对象
            id (ID): 模型对象 id

        Returns:
            PhotoModel: 模型对象
        """
        return dataset.get_photo(int(id))


class Query(ObjectType):
    """
    定义查询实体类型
    """
    user = Node.Field(User)
    photo = Node.Field(Photo)
    node = Node.Field()


schema = Schema(query=Query)
