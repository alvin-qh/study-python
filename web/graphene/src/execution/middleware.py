from typing import Any, Callable, Literal, Optional

from graphene import (
    ID,
    Argument,
    Field,
    InputObjectType,
    Int,
    Mutation,
    ObjectType,
    ResolveInfo,
    Schema,
    String,
)
from mypy_extensions import KwArg

from graphql import OperationType


class User(ObjectType):
    """定义实体类型

    对应的 GraphQL 定义如下:

    ```
    type User {
        id: ID!
        name: String!
        age: Int
        nickname: String
    }
    ```
    """

    id = ID(required=True)  # id 字段
    name = String(required=True)  # 用户名字段
    age = Int()  # 用户年龄字段
    nickname = String()  # 昵称字段


class Query(ObjectType):
    """定义查询类型, 用于查询 `User` 类型的实体对象

    对应的 GraphQL 定义如下:

    ```
    type Query {
        user(id: ID!): User
    }
    ```
    """

    # User 实体类型
    user = Field(User, id=Argument(ID, required=True))

    @staticmethod
    def resolve_user(parent: Literal[None], info: ResolveInfo, id: str) -> User:
        """解析 `user` 字段

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


class UserInput(InputObjectType):
    """定义创建 `User` 对象的输入对象

    对应的 GraphQL 定义如下:

    ```
    input UserInput {
        name: String!
        age: Int
    }
    ```
    """

    name = String(required=True)  # 姓名字段
    age = Int()  # 年龄字段


class UserCreate(Mutation):
    """本类型用于创建 `User` 实体对象"""

    class Arguments:
        """创建实体对象所需的参数定义类型"""

        # 定义输入参数, 为 UserInput 类型
        user_input = UserInput(required=True)

    # 定义输出结果类型, 操作完毕后返回一个 User 类型对象
    Output = User

    @staticmethod
    def mutate(parent: Any, info: ResolveInfo, user_input: UserInput) -> User:
        """定义变更操作

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


class UserMutation(ObjectType):
    """定义变更类型, 用于创建, 更新, 删除实体对象

    对应的 GraphQL 定义如下:

    ```
    type UserMutation {
        userCreate(userInput: UserInput!): User!
    }
    ```
    """

    # 创建用户的字段
    user_create = UserCreate.Field()


class ModificationMiddleware:
    """定义类型中间件

    `graphene` 具备两种类型的中间件形式, 类型和函数, 当前是类型形式的中间件

    该类型用于在查询和更新数据时, 对符合条件的数据值进行修改
    """

    def resolve(
        self,
        next: Callable[[Optional[User], ResolveInfo, KwArg(Any)], Any],
        instance: Optional[User],
        info: ResolveInfo,
        **kwargs: Any,
    ) -> Any:
        """解析方法, 在查询或更新前对参数或上下文进行处理

        Args:
            next (Callable): 下一个中间件解析方法
            instance (Optional[User]): 要处理的实体对象
            info (ResolveInfo): 上下文信息对象
        """
        # 判断是否进行了 getUser 的查询操作
        if self._check_operation(info, OperationType.QUERY, "getUser"):
            # 判断是否在查询 nickname 字段 (对应 User 类型的 nickname 字段)
            if info.field_name == "nickname":
                # 判断查询结果的 id 字段是否为 1
                if instance and instance.id == 1:
                    # 将查询结果的 nickname 字段进行修改
                    instance.nickname = "Miuiu"

        # 判断是否进行了 createUser 的更新操作
        if self._check_operation(info, OperationType.MUTATION, "createUser"):
            # 判断是否是对 userCreate 字段进行更新 (对应 UserMutation 类型的 user_create 字段)
            if info.field_name == "userCreate":
                # 获取更新操作的参数 (UserInput 类型字段)
                user_input: UserInput = kwargs["user_input"]
                if user_input.name == "Arthur":
                    # 将 name 字段匹配的更新参数中 age 字段进行修改
                    user_input.age = 1024

        # 调用下一个中间件操作
        return next(instance, info, **kwargs)

    @staticmethod
    def _check_operation(info: ResolveInfo, type_: OperationType, name: str) -> bool:
        """判断当前进行的操作

        Args:
            info (ResolveInfo): 上下文信息对象
            type_ (OperationType): 期待的操作类型
            name (str): 期待的操作名称

        Returns:
            bool: 是否为期待的操作
        """
        return (  # 判断操作名称是否符合期待
            bool(info.operation.operation == type_)
            and info.operation.name is not None
            and info.operation.name.value == name
        )


"""定义 schema 结构, 指定根查询对象

对应的 GraphQL 定义为

```
schema {
    query: Query
    mutation: UserMutation
}
```
"""
schema = Schema(query=Query, mutation=UserMutation)
