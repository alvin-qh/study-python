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


def test_without_parent() -> None:
    """
    不设置 `root` 参数, 表示不给顶级实体对象设置上级关联对象, `parent` 参数为 `None`
    """
    # 查询字符串
    query = """
        query($id: ID!) {       # 定义查询参数
            user(id: $id) {
                id
                name
            }
        }
    """

    root = None
    # 查询参数
    var = {"id": 2}

    # 执行查询, 传递查询参数, root 参数为 None
    r = schema.execute(query, variables=var, root=root)

    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "user": {
            "id": "2",
            "name": "Emma",
        },
    }


def test_with_parent() -> None:
    """
    设置 `root` 参数, 为顶级实体对象设置关联对象, 此时 `parent` 参数有值
    """
    # 查询字符串
    query = """
        query {
            user {
                id      # 对应 User 类型的 id 字段
                name    # 对应 User 类型的 name 字段
            }
        }
    """

    # 设置 root 参数
    root = User(id=1, name="Alvin")

    # 执行查询, 并设置 root 参数
    r = schema.execute(query, root=root)

    assert r.errors is None

    # 确认查询结果, 由于设置了 root, 所以查询结果为 root 设置的值
    assert r.data == {
        "user": {
            "id": "1",
            "name": "Alvin",
        },
    }
