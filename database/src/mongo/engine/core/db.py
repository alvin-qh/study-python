import signal
from typing import Any, Dict, Optional

from mongoengine import connect
from pymongo import MongoClient
from pymongo.monitoring import (
    ConnectionCheckedInEvent,
    ConnectionCheckedOutEvent,
    ConnectionCheckOutFailedEvent,
    ConnectionCheckOutStartedEvent,
    ConnectionClosedEvent,
    ConnectionCreatedEvent,
    ConnectionPoolListener,
    ConnectionReadyEvent,
    PoolClearedEvent,
    PoolClosedEvent,
    PoolCreatedEvent,
)


class MongoConnectionPoolLogger(ConnectionPoolListener):
    """对 pymongo 的各类事件进行监听"""

    def pool_created(self, event: PoolCreatedEvent) -> None:
        pass

    def pool_cleared(self, event: PoolClearedEvent) -> None:
        pass

    def pool_closed(self, event: PoolClosedEvent) -> None:
        pass

    def connection_created(self, event: ConnectionCreatedEvent) -> None:
        pass

    def connection_closed(self, event: ConnectionClosedEvent) -> None:
        pass

    def connection_check_out_failed(self, event: ConnectionCheckOutFailedEvent) -> None:
        pass

    def connection_ready(self, event: ConnectionReadyEvent) -> None:
        pass

    def connection_check_out_started(
        self, event: ConnectionCheckOutStartedEvent
    ) -> None:
        pass

    def connection_checked_out(self, event: ConnectionCheckedOutEvent) -> None:
        pass

    def connection_checked_in(self, event: ConnectionCheckedInEvent) -> None:
        pass


class MongoDB:
    """mongodb 链接辅助类"""

    _mongo_client: Optional[MongoClient[Dict[str, Any]]]

    def __init__(self) -> None:
        self._mongo_client = None

    def connect(
        self,
        dbname: str,
        host: str,
        port: int,
        username: str = "",
        password: str = "",
        replicaSet: str = "",
        directConnection: bool = False,
    ) -> None:
        """连接数据库

        Args:
            - `dbname` (`str`): 库名称
            - `host` (`str`): mongodb 地址
            - `port` (`int`): mongodb 端口号
            - `username` (`str`, optional): 用户名. Defaults to `""`.
            - `password` (`str`, optional): 密码. Defaults to `""`.
            - `replicaSet` (`str`, optional): 集群名称. Defaults to `""`.
            - `directConnection` (`bool`, optional): 是否直接连结. Defaults to `False`.
        """
        mongo_connection_pool_logger = MongoConnectionPoolLogger()

        kwargs = {
            "host": host,
            "port": port,
            "directConnection": directConnection,
            "authentication_source": "admin",
            "event_listeners": (mongo_connection_pool_logger,),
        }
        if username:
            kwargs["username"] = username

        if password:
            kwargs["password"] = password

        if replicaSet:
            kwargs["replicaset"] = replicaSet

        self._mongo_client = connect(dbname, **kwargs)

    def close(self) -> None:
        """关闭数据库链接"""
        if self._mongo_client:
            self._mongo_client.close()


# 实例化数据库链接辅助对象
mongodb = MongoDB()

# 监听系统信号, 当系统退出时关闭数据库连接
signal.signal(signal.SIGHUP, lambda sig, frame: mongodb.close())
