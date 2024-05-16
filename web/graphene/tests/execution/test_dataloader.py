from execution.dataloader import schema
from pytest import mark


@mark.asyncio
async def test_data_loader() -> None:
    """
    测试异步 DataLoader, 该测试方法需要通过协程异步执行, 即标记为 `@mark.asyncio`

    另外需要参考 `conftest.py` 文件中关于 `event_loop` 变量的 `fixture` 函数
    """
    # 定义查询结构
    query = """
        query($id: ID!) {       # 定义查询参数
            user(id: $id) {     # 查询 Query 类型的 user 字段, 传递参数
                id              # 查询 User 类型的 id 字段
                name            # 查询 User 类型的 name 字段
                friends {       # 查询 User 类型的 friends 字段, 为集合类型
                    __typename  # 查询实体类型
                    id          # 查询 User 类型的 id 字段
                    name        # 查询 User 类型的 name 字段
                }
                bestFriend {    # 查询 User 类型的 best_friend 字段
                    __typename  # 查询实体类型
                    id          # 查询 User 类型的 id 字段
                    name        # 查询 User 类型的 name 字段
                }
            }
        }
    """

    # 查询参数
    args = {"id": 20}

    # 执行查询, 因为使用了异步的 dataloader, 所以需要使用 execute_async 进行异步操作
    r = await schema.execute_async(query, variables=args)
    assert r.errors is None

    # 确认查询结果正确性
    assert r.data is not None

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
