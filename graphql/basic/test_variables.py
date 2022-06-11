from typing import Any

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
    user = Field(User, id=ID(required=True))

    @staticmethod
    def resolve_user(parent: Any, info: ResolveInfo, id: int) -> User:
        """
        解析 `user` 字段

        Args:
            id (int): 查询参数, 实体的 id

        Returns:
            User: User 类型对象
        """
        return dataset[int(id)]


# 定义查询 schema
schema = Schema(query=Query)


def test_variables() -> None:
    """
    测试通过变量传递查询参数
    """
    # 定义查询字符串
    query = """
        query($id: ID!) {      # 定义 $id 参数类型
            user(id: $id) {    # 定义获取 user 字段时需要 id 参数
                id      # 查询 User 类型的 id 字段
                name    # 查询 User 类型的 name 字段
            }
        }
    """

    # 查询参数
    var = {"id": 2}

    # 执行查询, 传递查询参数
    r = schema.execute(query, variables=var)

    # 确保查询正确
    assert r.errors is None
    # 确认查询结果
    assert r.data == {
        "user": {
            "id": "2",
            "name": "Emma"
        }
    }
