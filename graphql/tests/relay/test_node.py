import base64

from graphene import Context
from pytest import mark
from relay.node import ShipLoader, schema


@mark.asyncio
async def test_query_ship_field() -> None:
    """
    查询普通字段
    """
    # 定义查询结构
    query = """
        query ($id: ID!) {      # 定义参数
            ship(id: $id) {     # 查询 Query 类型的 ship 字段
                id              # 查询 Node 类型的 id 字段
                name            # 查询 Ship 类型的 name 字段
            }
        }
    """

    # 定义查询参数
    args = {"id": 10}

    # 异步执行查询
    result = await schema.execute_async(
        query,
        variables=args,
        context=Context(ship_loader=ShipLoader()),  # 在上下文中传递 ShipLoader 对象
    )
    # 确保查询正确
    assert result.errors is None

    # 确认查询结果
    assert result.data is not None
    assert result.data == {
        "ship": {
            "id": "U2hpcDoxMA==",
            "name": "Ship-10",
        },
    }
    # 确认返回结果中的 ID 字段的解码后内容
    assert base64.b64decode(result.data["ship"]["id"]).decode() == "Ship:10"


@mark.asyncio
async def test_query_ship_node_field() -> None:
    """
    查询 `Node` 接口实现类型字段
    """
    # 定义查询结构
    query = """
        query ($id: ID!) {          # 定义参数
            shipNode(id: $id) {     # 查询 Query 类型的 ship 字段 (以实现了 Node 接口类型方式)
                id                  # 查询 Node 类型的 id 字段
                name                # 查询 Ship 类型的 name 字段
            }
        }
    """

    # 定义查询参数
    # 对于查询 Node 接口的实体对象, ID 需经过编码
    args = {
        "id": base64.b64encode("Ship:10".encode()).decode(),
    }

    # 异步执行查询
    r = await schema.execute_async(
        query,
        variables=args,
        context=Context(ship_loader=ShipLoader()),
    )
    # 确保查询正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "shipNode": {
            "id": "U2hpcDoxMA==",
            "name": "Ship-10",
        }
    }


@mark.asyncio
async def test_query_node_field() -> None:
    """
    查询 `Node` 接口类型字段
    """
    # 定义查询结构
    query = """
        query ($id: ID!) {          # 定义参数
            node(id: $id) {         # 查询 Query 类型的 ship 字段 (以 Node 类型方式)
                id                  # 查询 Node 类型的 id 字段
                ... on Ship {       # 将 Node 类型转为 Ship 类型
                    name            # 查询 Ship 类型的 name 字段
                }
            }
        }
    """

    # 定义查询参数
    # 对于查询 Node 接口的实体对象, ID 需经过编码
    args = {
        "id": base64.b64encode("Ship:10".encode()).decode(),
    }

    # 异步执行查询
    r = await schema.execute_async(
        query,
        variables=args,
        context=Context(ship_loader=ShipLoader()),
    )
    # 确保查询正确
    assert r.errors is None

    # 确认查询结果
    assert r.data == {
        "node": {
            "id": "U2hpcDoxMA==",
            "name": "Ship-10",
        }
    }
