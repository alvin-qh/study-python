from typing import Optional

from graphene import ID, Field, ObjectType, ResolveInfo, Schema, String


class User(ObjectType):
    """
    定义实体对象
    """
    id = ID(required=True)  # id 字段, required 表示非空字段
    name = String(required=True)  # 姓名字段


# 实体类的数据集
dataset = {
    1: User(id=1, name="Alvin"),
    2: User(id=2, name="Emma"),
    3: User(id=3, name="Lucy"),
}


class Query(ObjectType):
    """
    定义查询类型
    """
    # 定义一个实体类型字段
    user = Field(User, id=ID())

    @staticmethod
    def resolve_user(parent: Optional[User], info: ResolveInfo, id: Optional[str] = None) -> User:
        """
        解析 `user` 字段

        `parent` 参数表达了上一级关联实体对象的实例.
        在解析顶级实体时, `parent` 参数由 `schema.execute` 的 `root` 参数指定

        Args:
            parent (Optional[User]): 传入的上级实体对象 (即当前对象是被哪个对象级联关联的)
            id (int): 查询参数, 实体的 id

        Returns:
            User: User 类型对象
        """
        # 如果传递了上一级关联对象, 则返回关联对象
        if parent:
            return parent

        if not id:
            raise ValueError("id")

        # 从数据集中查询对象
        return dataset[int(id)]


# 定义 schema 对象, 指定根查询对象
schema = Schema(query=Query)
