from typing import Any, Callable, Optional

from graphene import (ID, Argument, Field, InputObjectType, Int, Mutation,
                      ObjectType, ResolveInfo, Schema, String)


class User(ObjectType):
    """
    定义实体类型
    """
    id = ID(required=True)  # id 字段
    name = String(required=True)  # 用户名字段
    age = Int()  # 用户年龄字段
    nickname = String()  # 昵称字段


class UserInput(InputObjectType):
    """
    定义创建 `User` 对象的输入对象
    """
    name = String(required=True)  # 姓名字段
    age = Int()  # 年龄字段


class UserCreate(Mutation):
    """
    本类型用于创建 `User` 实体对象
    """
    class Arguments:
        """
        创建实体对象所需的参数定义类型
        """
        # 定义输入参数, 为 UserInput 类型
        user_input = UserInput(required=True)

    # 定义输出结果类型, 操作完毕后返回一个 User 类型对象
    Output = User

    @staticmethod
    def mutate(parent: Any, info: ResolveInfo, user_input: UserInput) -> User:
        """
        定义变更操作

        Args:
            user_input (UserInput): 创建对象的参数

        Returns:
            User: 返回创建的实体对象
        """
        return User(
            id=100,
            name=user_input.name,
            age=user_input.age,
        )


class Query(ObjectType):
    """
    定义查询类型, 用于查询 `User` 类型的实体对象
    """
    # User 实体类型
    user = Field(User, id=Argument(ID, required=True))

    @staticmethod
    def resolve_user(parent: Any, info: ResolveInfo, id: str) -> User:
        """
        解析 `user` 字段

        Args:
            id (str): 查询参数, 要查询 `User` 对象 `id` 值

        Returns:
            User: `User` 实体对象
        """
        id_ = int(id)

        # 根据 id 值返回对应的实体对象
        if id_ == 1:
            return User(id=1, name="Alvin", age=40)

        return User(id=10, name="Emma", age=36)


class UserMutation(ObjectType):
    """
    定义变更类型, 用于创建, 更新, 删除实体对象
    """
    # 创建用户的字段
    user_create = UserCreate.Field()


class AuthorizationMiddleware:
    def resolve(self, next: Callable, instance: Optional[User], info: ResolveInfo, **kwargs) -> Any:
        # Check is "mutation" operation with name "createUser"
        if self._check_operation(info, "mutation", "createUser"):
            # check if "Mutation" field is "user_create"
            if info.field_name == "userCreate":
                # Check if input name and modify the input age argument
                user_input: UserInput = kwargs["user_input"]
                if user_input.name == "Arthur":
                    user_input.age = 1024

        if self._check_operation(info, "query", "getUser"):
            # if resolve is "get nickname", and "user.id" is 1, return nickname
            if info.field_name == "nickname":
                if instance and instance.id == 1:
                    return "purpleswg"

        return next(instance, info, **kwargs)

    @staticmethod
    def _check_operation(info: ResolveInfo, operation: str, operation_name: str) -> bool:
        return (
            info.operation.operation == operation
            and
            info.operation.name.value == operation_name
        )


schema = Schema(query=Query, mutation=UserMutation)


def test_query_operation() -> None:
    query = """
        query getUser($id: ID!) {
            user(id: $id) {
                id
                name
                age
                nickname
            }
        }
    """

    opt_name = "getUser"
    var = {"id": 1}

    r = schema.execute(
        query,
        operation_name=opt_name,
        variables=var,
        middleware=[AuthorizationMiddleware()]
    )
    assert r.errors is None
    assert r.data == {
        "user": {
            "id": "1",
            "name": "Alvin",
            "age": 40,
            "nickname": None,
        }
    }


def test_mutation_operation() -> None:
    query = """
        mutation createUser($user: UserInput!) {
            userCreate(userInput: $user) {
                id
                name
                age
            }
        }
    """

    opt_name = "createUser"
    var = {
        "user": {
            "name": "Arthur",
            "age": 42,
        }
    }

    r = schema.execute(
        query,
        operation_name=opt_name,
        variables=var,
        middleware=[AuthorizationMiddleware()]
    )
    assert r.errors is None
    assert r.data == {
        "userCreate": {
            "id": "100",
            "name": "Arthur",
            "age": 42,
        }
    }
