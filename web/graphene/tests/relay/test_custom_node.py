from graphene import Context
from pytest import mark
from relay.custom_node import PhotoLoader, UserLoader, schema


@mark.asyncio
async def test_query_users() -> None:
    """
    测试查询 `User` 类型对象

    该对象从 `CustomNode` 类型继承
    """
    # 定义查询结构
    query = """
        query($id: ID!) {       # 设置查询参数
            user(id: $id) {     # 查询 Query 类型 user 字段
                id              # User 类型 id 字段, 该字段从 Node 接口继承
                name            # User 类型 name 字段
            }
        }
    """

    # 定义查询参数
    args = {"id": "User:12"}

    # 异步执行查询
    r = await schema.execute_async(
        query,
        variables=args,
        context=Context(
            user_loader=UserLoader(),  # 将 UserLoader 对象存入 Context 对象
        ),
    )
    # 确保查询执行正确
    assert r.errors is None

    # 确认查询结果正确
    assert r.data == {
        "user": {
            "id": "User:12",
            "name": "User-12",
        }
    }


@mark.asyncio
async def test_query_photo() -> None:
    """
    测试查询 `Photo` 对象

    该对象从 `CustomNode` 类型继承
    """
    # 定义查询结构
    query = """
        query($id: ID!) {       # 设定查询参数
            photo(id: $id) {    # 查询 Query 类型的 photo 字段
                id              # Photo 类型的 id 字段
                forUser {       # Photo 类型的 for_user 字段
                    id
                    name
                }
                datetime
            }
        }
    """

    # 定义查询参数
    args = {"id": "Photo:12"}

    # 异步执行查询
    r = await schema.execute_async(
        query,
        variables=args,
        context=Context(
            user_loader=UserLoader(),  # 将 UserLoader 对象存入 Context 对象
            photo_loader=PhotoLoader(),  # 将 PhotoLoader 对象存入 Context 对象
        ),
    )
    # 确保查询执行正确
    assert r.errors is None

    # 确认查询结果正确
    assert r.data == {
        "photo": {
            "id": "Photo:12",
            "forUser": {"id": "User:7", "name": "User-7"},
            "datetime": "2020-01-01T00:00:11",
        },
    }


@mark.asyncio
async def test_query_node() -> None:
    """
    测试以 `Node` 类型查询结果
    """
    # 定义查询结构
    query = """
        query($id: ID!) {       # 定义查询参数
            node(id: $id) {     # 查询 Query 类型的 node 字段, 传递参数
                __typename      # 查询实体对象类型
                id              # 查询 Node 类型的 id 字段
                ... on User {   # 当查询结果类型为 User 类型
                    name        # 查询 User 类型的 name 字段
                }
                ... on Photo {  # 当查询结果类型为 Photo 类型
                    forUser {   # 查询 Photo 类型的 for_user 字段
                        id      # 查询 User 类型的 id 字段
                        name    # 查询 User 类型的 name 字段
                    }
                    datetime    # 查询 Photo 类型的 datetime 字段
                }
            }
        }
    """

    # 定义查询参数
    # 由于自定义 Global ID 的转换规则, 这里无需通过 base64 编码
    args = {"id": "Photo:12"}

    # 执行查询
    r = await schema.execute_async(
        query,
        variables=args,
        context=Context(  # 定义查询上下文对象
            user_loader=UserLoader(),
            photo_loader=PhotoLoader(),
        ),
    )
    # 确保查询正确
    assert r.errors is None

    # 确认查询结果正确
    assert r.data == {
        "node": {
            "__typename": "Photo",
            "id": "Photo:12",
            "forUser": {
                "id": "User:7",
                "name": "User-7",
            },
            "datetime": "2020-01-01T00:00:11",
        },
    }

    # 定义查询参数
    # 由于自定义 Global ID 的转换规则, 这里无需通过 base64 编码
    args = {"id": "User:12"}

    # 执行查询
    r = await schema.execute_async(
        query,
        variables=args,
        context=Context(
            user_loader=UserLoader(),
            photo_loader=PhotoLoader(),
        ),
    )
    # 确保查询正确
    assert r.errors is None

    # 确认查询结果正确
    assert r.data == {
        "node": {
            "__typename": "User",
            "id": "User:12",
            "name": "User-12",
        },
    }
