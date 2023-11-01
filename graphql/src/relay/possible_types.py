"""为 `Node` 类型增加 "可能的类型"

如果一个类型 `Foo` 从 `Node` 类型继承, 且在使用 `Foo` 类型定义字段时未明确指定字段的类型,
则需要为 `Foo` 类型指定其可能转化为的类型列表, 可以通过 `Meta.possible_types` 字段或者
`is_type_of` 方法来指定, 例如:

```graphql
class Foo(ObjectType):
    class Meta:
        interfaces = (Node,)    # 从 Node 接口类型继承

    ...
```

此时定义 `Foo` 类型的查询字段

```graphql
type Query(ObjectType):
    foo1 = Node.Field(Foo)   # 此时类型明确
    foo2 = Node.Field()      # 此时类型不明
```

对于查询 `foo1`, 则直接指定查询字段即可

```graphql
query {
    foo1 {
        ...
    }
}
```

对于查询 `foo2`, 因为实际类型未知, 则需要在查询时指定类型

```graphql
query {
    foo2 {
        ... on Foo {
            ...
        }
    }
}
```

但此时查询会出错, 因为 `Foo` 在定义时, 并未明确指定查询何种类型可以返回该类型对象, 所以需要明确:

```python
class Foo(ObjectType):
    class Meta:
        interfaces = (Node,)
        possible_types = (Foo,)  # 由于 Python 的限制, 在类型内无法使用当前类型声明, 所以这里只能填写非当前类型

    ...

    # 如果使用 is_type_of 方法, 则可避免上述问题
    @staticmethod
    def is_type_of(info: ResolveInfo) -> Tuple[ObjectType]:
        return (Foo,)
```

此时, 查询 `foo2` 字段并使用 `... on Foo {}` 即可以得到正确结果
"""

import datetime
import time
from typing import Any, Dict, Tuple

from graphene import ID, DateTime, Field, Node, ObjectType, ResolveInfo, Schema, String


class UserModel:
    """定义模型类型, 表示一个用户"""

    id: int
    name: str

    def __init__(self, **kwargs: Any) -> None:
        """初始化对象"""
        self.id = kwargs["id"]
        self.name = kwargs["name"]


class PhotoModel:
    """定义模型类型, 表示一张照片"""

    id: int
    for_user_id: int
    datetime: datetime.datetime

    def __init__(self, **kwargs: Any) -> None:
        """初始化对象"""
        self.id = kwargs["id"]
        self.for_user_id = kwargs["for_user_id"]
        self.datetime = kwargs["datetime"]


class Dataset:
    """数据集类型"""

    users: Dict[int, UserModel]
    photos: Dict[int, PhotoModel]

    def __init__(self) -> None:
        self.users = {}
        self.photos = {}

    def get_user(self, id: int) -> UserModel:
        """根据用户 ID 获取用户实体对象

        Args:
            id (str): 用户 ID

        Returns:
            User: 用户实体对象
        """
        return self.users[id]

    def get_photo(self, id: int) -> PhotoModel:
        """根据 ID 获取照片实体对象

        Args:
            id (int): 照片 ID

        Returns:
            Photo: 照片实体对象
        """
        return self.photos[id]

    def save_user(self, user: UserModel) -> None:
        """保存用户实体对象

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
                UserModel(
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
    """定义实体对象, 表示用户"""

    class Meta:
        # 继承 Node 接口
        interfaces = (Node,)
        # 定义当前 Node 接口可能表示的类型
        # 由于 Python 语言的限制, 这里无法填写 User 类型, 所以填写了具有相同结构的 UserModel 类型
        # 这种情况下, 更推荐使用 is_type_of 方法返回可能的类型
        possible_types = (UserModel,)

    name = String(required=True)

    @classmethod
    def get_node(cls, info: ResolveInfo, id: ID) -> UserModel:
        """根据 ID 获取当前实体对应的模型对象

        Args:
            info (ResolveInfo): 查询上下文对象
            id (ID): 模型对象 ID

        Returns:
            UserModel: 模型对象
        """
        return dataset.get_user(int(id))


class Photo(ObjectType):
    """定义实体对象, 表示照片"""

    class Meta:
        # 继承 CustomNode 接口
        interfaces = (Node,)
        # 定义当前 Node 接口可能表示的类型
        # possible_types = (PhotoModel,)

    for_user = Field(User, required=True)
    datetime = DateTime(required=True)

    @staticmethod
    def is_type_of(parent: PhotoModel, info: ResolveInfo) -> Tuple[ObjectType]:
        """如果当前类型从 `Node` 接口继承, 且未提供 `Meta.possible_types` 字段,
        则可以通过 `is_type_of` 方法返回可能的类型

        Returns:
            Tuple[ObjectType]: 可能的类型集合
        """
        return (Photo,)

    @staticmethod
    def resolve_for_user(parent: PhotoModel, info: ResolveInfo) -> UserModel:
        """解析 `for_user` 字段

        Args:
            parent (PhotoModel): 当前查询的模型对象
            info (ResolveInfo): 查询上下文对象

        Returns:
            UserModel: 用户模型对象
        """
        return dataset.get_user(int(parent.for_user_id))

    @classmethod
    def get_node(cls, info: ResolveInfo, id: ID) -> PhotoModel:
        """根据 ID 获取当前实体对应的模型对象

        Args:
            info (ResolveInfo): 查询上下文对象
            id (ID): 模型对象 id

        Returns:
            PhotoModel: 模型对象
        """
        return dataset.get_photo(int(id))


class Query(ObjectType):
    """定义查询实体类型"""

    user = Node.Field(User)
    photo = Node.Field(Photo)
    node = Node.Field()


schema = Schema(query=Query)
