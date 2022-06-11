from typing import Any

from graphene import ID, Field, ObjectType, ResolveInfo, Schema, String


class User(ObjectType):
    """
    定义实体对象
    """
    id = ID(required=True)  # id 类型字段
    first_name = String(required=True)  # 名字字段
    last_name = String(required=True)  # 姓字段
    full_name = String(required=True)  # 全名字段

    @staticmethod
    def resolve_full_name(parent: "User", info: ResolveInfo) -> str:
        """
        解析 `full_name` 字段.

        `full_name` 字段属于 `User` 类型, 相当于 `User` 类型的关联数据.
        所以此时 `parent` 参数的值为 `User` 类型的对象

        Args:
            parent (User): 相关的 `User` 类型对象

        Returns:
            str: 全名值
        """
        # 返回全名字符串, 由其它两个名字组合而成
        return f"{parent.first_name}·{parent.last_name}"


# 实体类的数据集
dataset = {
    1: User(id=1, first_name="Alvin", last_name="Qu"),
    2: User(id=2, first_name="Emma", last_name="Yua"),
    3: User(id=3, first_name="Lucy", last_name="Green")
}


class Query(ObjectType):
    """
    定义查询类型
    """
    # 定义一个实体类型字段
    user = Field(User, id=ID(required=True))

    @staticmethod
    def resolve_user(parent: Any, info: ResolveInfo, id: str) -> User:
        """
        解析 `user` 字段, 这是整个查询的顶级实体.
        `User` 类型还包括 `full_name` 字段, 相当于是下一级关联实体

        Args:
            id (str): 查询参数, 用户 ID

        Returns:
            User: 查询到的 User 对象
        """
        return dataset[int(id)]


# 定义 schema 对象, 指定根查询对象
schema = Schema(query=Query)


def test_operation_name() -> None:
    """
    不设置 `root` 参数, 表示不给顶级实体对象设置上级关联对象, `parent` 参数为 `None`
    """
    # 查询字符串
    query = """
        query getUser($id: ID!) {   # 定义操作名称, 定义查询参数
            user(id: $id) {
                id           # 对应 User 类型的 id 字段
                firstName    # 对应 User 类型的 first_name 字段
                lastName     # 对应 User 类型的 last_name 字段
            }
        }

        query getUserWithFullName($id: ID!) {   # 定义操作名称, 定义查询参数
            user(id: $id) {
                id          # 对应 User 类型的 id 字段
                fullName    # 对应 User 类型的 full_name 字段
            }
        }
    """

    # 定义要执行的操作名称
    opt_name = "getUser"
    # 定义查询参数
    var = {"id": 3}

    # 执行查询
    r = schema.execute(query, operation_name=opt_name, variables=var)
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "user": {
            "id": "3",
            "firstName": "Lucy",
            "lastName": "Green",
        }
    }

    # 定义要执行的操作名称
    opt_name = "getUserWithFullName"
    # 定义查询参数
    var = {"id": 1}

    # 执行查询
    r = schema.execute(query, operation_name=opt_name, variables=var)
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "user": {
            "id": "1",
            "fullName": "Alvin·Qu",
        }
    }
