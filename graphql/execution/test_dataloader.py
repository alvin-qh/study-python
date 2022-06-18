from pytest import mark

from .dataloader import schema


@mark.asyncio
async def test_data_loader() -> None:
    """
    测试异步 DataLoader, 该测试方法需要通过协程异步执行, 即标记为 `@mark.asyncio`

    另外需要参考 `conftest.py` 文件中关于 `event_loop` 变量的 `fixture` 函数
    """
    # 要执行的查询字符串
    query = """
        query getUser($id: ID!) {
            user(id: $id) {
                id
                name
                friends {
                    __typename
                    id
                    name
                }
                bestFriend {
                    __typename
                    id
                    name
                }
            }
        }
    """

    # 查询参数
    vars = {"id": 20}

    # 执行查询, 因为使用了异步的 dataloader, 所以需要使用 execute_async 进行异步操作
    r = await schema.execute_async(query, variables=vars)
    assert r.errors is None

    # 确认查询结果正确性

    # 主实体对象正确性
    assert r.data["user"]["id"]
    assert r.data["user"]["name"]

    # 相关实体对象正确性
    assert r.data["user"]["bestFriend"]
    assert r.data["user"]["bestFriend"]["__typename"] == "User"

    # 相关实体对象集合正确性
    assert len(r.data["user"]["friends"]) >= 3
    assert r.data["user"]["friends"][0]["__typename"] == "User"
    assert r.data["user"]["friends"][0]["id"]
    assert r.data["user"]["friends"][0]["name"]
