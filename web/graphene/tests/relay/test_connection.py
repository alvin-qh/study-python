from pytest import mark
from relay.connection import schema


@mark.asyncio
async def test_connection() -> None:
    query = """
        query($id: ID!, $first: Int!, $last: Int!) {
            hero(id: $id) {
                id
                name
                ownShips(first: $first, last: $last) {
                pageInfo {
                    startCursor
                    endCursor
                    hasNextPage
                    hasPreviousPage
                }
                totalCount
                edges {
                    cursor
                    link
                    node {
                        id
                        name
                    }
                }
            }
            }
        }
    """

    args = {"id": 1, "first": 0, "last": 3}

    # 异步执行查询
    result = await schema.execute_async(
        query,
        variables=args,
    )
    # 确保查询执行正确
    assert result.errors is None

    # 确认查询结果正确
    assert result.data == {
        "hero": {
            "id": "1",
            "name": "Hero-1",
            "ownShips": {
                "pageInfo": {
                    "startCursor": "0",
                    "endCursor": "2",
                    "hasNextPage": True,
                    "hasPreviousPage": False,
                },
                "totalCount": 3,
                "edges": [
                    {
                        "cursor": "0",
                        "link": "https://myapp.com/data/1",
                        "node": {"id": "1", "name": "Ship-1"},
                    },
                    {
                        "cursor": "1",
                        "link": "https://myapp.com/data/2",
                        "node": {"id": "2", "name": "Ship-2"},
                    },
                    {
                        "cursor": "2",
                        "link": "https://myapp.com/data/3",
                        "node": {"id": "3", "name": "Ship-3"},
                    },
                ],
            },
        }
    }
