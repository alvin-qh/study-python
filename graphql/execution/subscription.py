# Every schema requires a query.
import asyncio
from datetime import datetime, timedelta
from typing import AsyncGenerator, Literal

from graphene import ObjectType, ResolveInfo, Schema, String


class Query(ObjectType):
    """
    查询类型, 在本例中, 该类型仅是为了满足 `graphene` 框架的参数要求
    """
    hello = String()


class Subscription(ObjectType):
    """
    订阅类型, 可以向调用方

    Args:
        ObjectType (_type_): _description_

    Yields:
        _type_: _description_
    """
    # 定义要被订阅的字段值, 字符串类型
    time_of_day = String()

    @staticmethod
    async def subscribe_time_of_day(
        root: Literal[None], info: ResolveInfo,
    ) -> AsyncGenerator[str, None]:
        """
        `time_of_day` 字段在被订阅后如何发送订阅值

        Yields:
            str: 每次发送给订阅方的内容
        """
        start = datetime.utcnow()
        # 循环 5 秒钟
        while (datetime.utcnow() - start) < timedelta(seconds=5):
            # 发送当前时间作为订阅值
            yield datetime.utcnow().isoformat()
            # 协程休眠 1 秒
            await asyncio.sleep(1)


# 设定 schema 的订阅类型
# 注意, schema 中必须包含一个 Query 类型
schema = Schema(query=Query, subscription=Subscription)
