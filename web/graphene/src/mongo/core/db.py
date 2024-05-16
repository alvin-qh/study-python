import signal
from typing import Any, Dict, Optional

from mongoengine import connect
from pymongo import MongoClient


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
    ) -> None:
        """连接数据库

        Args:
            - `dbname` (`str`): 库名称
            - `host` (`str`): mongodb 地址
            - `port` (`int`): mongodb 端口号
            - `username` (`str`, optional): 用户名. Defaults to `""`.
            - `password` (`str`, optional): 密码. Defaults to `""`.
        """
        kwargs = {
            "host": host,
            "port": port,
            "authentication_source": "admin",
        }
        if username:
            kwargs["username"] = username

        if password:
            kwargs["password"] = password

        self._mongo_client = connect(dbname, **kwargs)

    def close(self) -> None:
        """关闭数据库链接"""
        if self._mongo_client:
            self._mongo_client.close()


# 实例化数据库链接辅助对象
mongodb = MongoDB()

# 监听系统信号, 当系统退出时关闭数据库连接
signal.signal(signal.SIGHUP, lambda sig, frame: mongodb.close())
