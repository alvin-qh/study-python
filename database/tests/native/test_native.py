from datetime import date

import pytest
from native import (
    delete_user,
    get_connection,
    get_pooled_connection,
    get_user,
    insert_user,
    update_user,
)
from pymysql import Connection


def run_curd(conn: Connection) -> None:
    """
    测试 pymysql 的增删改查
    """

    # 启动事务
    conn.begin()
    try:
        # 测试插入数据

        # 插入用户数据, 获取返回的主键 ID
        id_ = insert_user(
            conn,
            "61010419810303210",
            "Alvin",
            "M",
            date(1981, 3, 3),
        )
        assert id_

        # 测试查询数据

        # 根据主键 ID 获取用户数据
        user = get_user(conn, id_)
        assert user["id"] == id_
        assert user["id_num"] == "61010419810303210"
        assert user["name"] == "Alvin"
        assert user["gender"] == "M"
        assert user["birthday"] == date(1981, 3, 3)

        # 测试更新数据

        # 根据主键 ID, 更新用户数据
        count = update_user(
            conn,
            id_,
            "61010419810303211",
            "Emma",
            "F",
            date(1981, 3, 9),
        )
        # 更新了一行数据
        assert count == 1

        # 再次获取用户数据, 验证更新结果
        user = get_user(conn, id_)
        assert user["id"] == id_
        assert user["id_num"] == "61010419810303211"
        assert user["name"] == "Emma"
        assert user["gender"] == "F"
        assert user["birthday"] == date(1981, 3, 9)

        # 测试删除数据

        # 根据主键 ID, 删除用户数据
        count = delete_user(conn, id_)
        # 删除了一行数据
        assert count == 1

        # 确保删除成果
        user = get_user(conn, id_)
        assert user is None

        # 提交事务
        conn.commit()
    except Exception:
        conn.rollback()
        pytest.fail()
    finally:
        conn.close()


def test_curd() -> None:
    """
    测试 pymysql 的增删改查
    """

    run_curd(get_connection())


def test_pooled_curd() -> None:
    """
    通过连接池获取连接, 测试增删改查
    """

    run_curd(get_pooled_connection())
