import re

from execution.subscription import schema
from pytest import mark

from graphql import ExecutionResult


@mark.asyncio
async def test_subscription() -> None:
    """
    测试产生一个订阅对象
    """
    # 判断结果格式的正则表达式
    p = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+")

    # 使用 graphql 语法, 产生一个订阅字符串
    # timeOfDay 表示订阅 time_of_day 字段的值
    subscription = """
        subscription {
            timeOfDay
        }
    """

    # 进行一次订阅
    rs = await schema.subscribe(subscription)

    # 获取一次订阅值值
    r: ExecutionResult = await rs.__anext__()
    # 确认结果正确
    assert r.errors is None and r.data
    assert p.match(r.data["timeOfDay"])

    # 通过异步 for 循环连续获取订阅值
    async for r in rs:
        # 确认结果正确
        assert r.errors is None and r.data
        assert p.match(r.data["timeOfDay"])
