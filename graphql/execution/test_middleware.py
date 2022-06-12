import timeit
from typing import Any, Callable, List, Literal, Optional, Tuple

from graphene import (ID, Argument, Field, InputObjectType, Int, Mutation,
                      ObjectType, ResolveInfo, Schema, String)

from graphql import OperationType


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
    def resolve_user(parent: Literal[None], info: ResolveInfo, id: str) -> User:
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


class ModificationMiddleware:
    """
    定义类型中间件

    `graphene` 具备两种类型的中间件形式, 类型和函数, 当前是类型形式的中间件

    该类型用于在查询和更新数据时, 对符合条件的数据值进行修改
    """

    def resolve(self, next: Callable, instance: Optional[User], info: ResolveInfo, **kwargs) -> Any:
        """
        解析方法, 在查询或更新前对参数或上下文进行处理

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
        """
        判断当前进行的操作

        Args:
            info (ResolveInfo): 上下文信息对象
            type_ (OperationType): 期待的操作类型
            name (str): 期待的操作名称

        Returns:
            bool: 是否为期待的操作
        """
        return (
            info.operation.operation == type_   # 判断操作类型是否符合期待
            and
            info.operation.name.value == name  # 判断操作名称是否符合期待
        )


# 定义 schema 对象
schema = Schema(query=Query, mutation=UserMutation)


def test_middleware_class_query_operation() -> None:
    """
    测试查询操作时, 类型中间件的作用
    """

    query = """
        query getUser($id: ID!) {  # 定义操作名称, 定义查询参数名称
            user(id: $id) { # 对应 Query 类型的 user 字段
                id          # 对应 User 类型的 id 字段
                name        # 对应 User 类型的 name 字段
                age         # 对应 User 类型的 age 字段
                nickname    # 对应 User 类型的 nickname 字段
            }
        }
    """

    # 指定要进行的操作名称
    opt_name = "getUser"
    # 指定查询参数
    var = {"id": 1}

    # 执行查询, 并设置此次操作的中间件链
    r = schema.execute(
        query,
        operation_name=opt_name,
        variables=var,
        middleware=[ModificationMiddleware()],   # 设置中间件操作链
    )
    assert r.errors is None

    # 确认查询结果
    # 因为操作, id 值符合预期, 所以 nickname 字段在中间件 resolve 中被改为 Miuiu
    assert r.data == {
        "user": {
            "id": "1",
            "name": "Alvin",
            "age": 40,
            "nickname": "Miuiu",
        }
    }


def test_middleware_class_mutation_operation() -> None:
    """
    测试更新操作时, 类型中间件的作用
    """
    # 设定更新操作字符串
    mutate = """
        mutation createUser($user: UserInput!) {   # # 定义操作名称, 定义输入参数名称
            userCreate(userInput: $user) {  # 对应 UserMutation 类型的 user_create 字段, 输入名为 user 的参数
                id      # 对应 UserCreate 类型的 id 字段
                name    # 对应 UserCreate 类型的 name 字段
                age     # 对应 UserCreate 类型的 age 字段
            }
        }
    """

    # 指定要进行的操作名称
    opt_name = "createUser"
    # 指定更新参数
    var = {
        "user": {   # 对应更新字符串中的 createUser 操作中的 user 参数
            "name": "Arthur",
            "age": 42,
        }
    }

    # 执行更新操作
    r = schema.execute(
        mutate,
        operation_name=opt_name,
        variables=var,
        middleware=[ModificationMiddleware()],  # 设定更新操作的中间件链
    )
    assert r.errors is None

    # 因为操作类型, 操作名称和输入参数 name 字段符合预期, 所以 age 字段被中间件修改
    assert r.data == {
        "userCreate": {
            "id": "100",
            "name": "Arthur",
            "age": 1024,
        }
    }


# 记录每个字段解析时间的日志集合
runtime_records: List[Tuple[str, float]] = []


def setup_function() -> None:
    """
    测试前清理所有日志
    """
    global runtime_records
    runtime_records = []


def timeit_middleware(next: Callable, instance: Any, info: ResolveInfo, **kwargs) -> Any:
    """
    `graphene` 具备两种类型的中间件形式, 类型和函数, 当前是函数形式的中间件

    Args:
        next (Callable): 调用链, 引用到下一个中间件函数
        instance (Any): 本次处理的实体类型对象
        info (ResolveInfo): 查询上下文对象

    Returns:
        Any: 中间件处理结果
    """
    # 记录起始时间
    start = timeit.default_timer()
    # 执行后续操作
    next_node = next(instance, info, **kwargs)
    # 计算执行时间
    duration = round((timeit.default_timer() - start) * 1000, 2)

    # 获取当前实体的类型
    type_name = (
        instance._meta.name
        if instance and hasattr(instance, "_meta")
        else ""
    )

    if type_name:
        # 记录字段解析日志, info.field_name 是本次处理的字段名
        runtime_records.append((f"{type_name}.{info.field_name}", duration))

    return next_node


def test_middleware_function_query_operation() -> None:
    """
    测试查询操作时, 函数中间件的作用
    """

    query = """
        query getUser($id: ID!) {  # 定义操作名称, 定义查询参数名称
            user(id: $id) { # 对应 Query 类型的 user 字段
                id          # 对应 User 类型的 id 字段
                name        # 对应 User 类型的 name 字段
                age         # 对应 User 类型的 age 字段
                nickname    # 对应 User 类型的 nickname 字段
            }
        }
    """

    # 指定要进行的操作名称
    opt_name = "getUser"
    # 指定查询参数
    var = {"id": 1}

    # 执行查询, 并设置此次操作的中间件链
    r = schema.execute(
        query,
        operation_name=opt_name,
        variables=var,
        middleware=[timeit_middleware],   # 设置中间件操作链
    )
    assert r.errors is None

    # 确认查询结果
    # 因为操作, id 值符合预期, 所以 nickname 字段在中间件 resolve 中被改为 Miuiu
    assert r.data == {
        "user": {
            "id": "1",
            "name": "Alvin",
            "age": 40,
            "nickname": None,
        }
    }

    # 检测日志记录情况
    assert len(runtime_records) == 4
    assert [r[0] for r in runtime_records] == [
        "User.id", "User.name", "User.age", "User.nickname",
    ]


def test_middleware_function_mutation_operation() -> None:
    """
    测试更新操作时, 函数中间件的作用
    """
    # 设定更新操作字符串
    mutate = """
        mutation createUser($user: UserInput!) {   # # 定义操作名称, 定义输入参数名称
            userCreate(userInput: $user) {  # 对应 UserMutation 类型的 user_create 字段, 输入名为 user 的参数
                id      # 对应 UserCreate 类型的 id 字段
                name    # 对应 UserCreate 类型的 name 字段
                age     # 对应 UserCreate 类型的 age 字段
            }
        }
    """

    # 指定要进行的操作名称
    opt_name = "createUser"
    # 指定更新参数
    var = {
        "user": {   # 对应更新字符串中的 createUser 操作中的 user 参数
            "name": "Arthur",
            "age": 42,
        }
    }

    # 执行更新操作
    r = schema.execute(
        mutate,
        operation_name=opt_name,
        variables=var,
        middleware=[timeit_middleware],  # 设定更新操作的中间件链
    )
    assert r.errors is None

    # 因为操作类型, 操作名称和输入参数 name 字段符合预期, 所以 age 字段被中间件修改
    assert r.data == {
        "userCreate": {
            "id": "100",
            "name": "Arthur",
            "age": 42,
        }
    }

    # 检查日志记录情况
    assert len(runtime_records) == 3
    assert [r[0] for r in runtime_records] == [
        "User.id", "User.name", "User.age",
    ]
