from typing import List

import pymysql
from alembic_.command import Command


def get_all_tables() -> List[str]:
    """
    获取数据库中所有的表

    Returns:
        List[str]: 数据库中表名称列表
    """

    _conn_options = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "root",
        "db": "study_python",
        "charset": "utf8mb4"
    }

    conn = pymysql.connect(**_conn_options)
    try:
        with conn.cursor() as c:
            # 获取所有的数据表
            c.execute(r"SHOW TABLES")
            rows = c.fetchall()

        return [row[0] for row in rows] if rows else []
    finally:
        conn.close()


def test_alembic_command() -> None:
    cmd = Command(conn_url="mysql+pymysql://root:root@localhost/study_python")
    cmd.reset()

    tables = get_all_tables()
    assert set(tables) == {
        "alembic_version",
        "core_groups",
        "core_users",
        "core_user_groups"
    }
