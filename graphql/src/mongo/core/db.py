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
    _mongo_client: Optional[MongoClient[Dict[str, Any]]]

    def __init__(self) -> None:
        self._mongo_client = None

    def connect(
        self, dbname: str, host: str, port: int, user: str = "", password: str = ""
    ) -> None:
        mongo_connection_pool_logger = MongoConnectionPoolLogger()
        self._mongo_client = connect(
            dbname,
            host=host,
            port=port,
            # username=user,
            # password=password,
            directConnection=True,  # 对于单节点集群, 必须设置为 True
            replicaset="rs0",  # 连接的集群名称
            authentication_source="admin",
            event_listeners=(mongo_connection_pool_logger,),
        )

    def close(self) -> None:
        if self._mongo_client:
            self._mongo_client.close()


mongodb = MongoDB()

signal.signal(signal.SIGHUP, lambda sig, frame: mongodb.close())
