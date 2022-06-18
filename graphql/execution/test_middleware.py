import timeit
from typing import Any, Callable, List, Tuple

from graphene import ResolveInfo

from .middleware import ModificationMiddleware, schema


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
