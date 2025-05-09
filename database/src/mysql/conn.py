from typing import Any, cast

import pymysql  # type: ignore[import-untyped]
from dbutils.pooled_db import PooledDB
from pymysql import Connection, connect
from pymysql.cursors import DictCursor  # type: ignore[import-untyped]

from .curd import init_tables

# 连接配置
_conn_options = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "root",
    "db": "study_python_mysql",
    "charset": "utf8mb4",
    "cursorclass": DictCursor,
}


def _init_tables(conn: Connection) -> None:
    """初始化当前数据库中的数据表

    Args:
        - `conn` (`Connection`): 数据库连接对象
    """
    # 启动事务
    conn.begin()
    try:
        # 初始化数据表
        init_tables(conn)
        # 成功后提交事务
        conn.commit()
    except Exception:
        # 异常后回滚事务
        conn.rollback()
        raise


def get_connection() -> Connection:
    """
    获取数据库连接

    Returns:
        `Connection`: 连接对象
    """
    # 根据连接配置连接数据库
    conn: Connection = connect(**_conn_options)
    # 关闭自动提交
    conn.autocommit(False)

    # 初始化数据表
    _init_tables(conn)

    return conn


# 创建连接池对象
pool = PooledDB(pymysql, 5, **_conn_options)


def get_pooled_connection() -> Connection:
    """
    从连接池获取数据库连接

    Returns:
        `Connection`: 连接对象
    """
    # 通过连接池获取连接对象
    conn: Connection = cast(Any, pool.connection())
    # 关闭自动提交
    conn.autocommit_mode = False

    # 初始化数据表
    _init_tables(conn)

    return conn
