from datetime import date
from typing import Any, Dict

from pymysql import Connection


def init_tables(conn: Connection) -> None:
    """
    初始化数据表
    """

    # 创建游标对象
    with conn.cursor() as c:
        # 清空所有数据表
        c.execute("DROP TABLE IF EXISTS `core_users`")

        # 创建 "core_users" 数据表
        c.execute("""
            CREATE TABLE `core_users` (
                `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                `id_num` VARCHAR(50) NOT NULL,
                `name` VARCHAR(50) NOT NULL,
                `gender` CHAR(1) NOT NULL,
                `birthday` DATE DEFAULT NULL,
                `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
                PRIMARY KEY (`id`),
                UNIQUE KEY `ux_id_num` (`id_num`),
                KEY `ix_name` (`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""")


def insert_user(conn: Connection, id_num: str, name: str, gender: str, birthday: date) -> int:
    """
    插入用户数据

    Args:
        conn (Connection): 数据库连接对象
        id_num (str): 身份证号
        name (str): 姓名
        gender (str): 性别
        birthday (date): 生日

    Returns:
        int: 数据表主键 ID
    """
    # 设置 SQL 模板
    sql = r"INSERT INTO `core_users` (`id_num`, `name`, `gender`, `birthday`) VALUES (%s, %s, %s, %s)"

    with conn.cursor() as c:
        # 执行 SQL 语句
        c.execute(sql, (id_num, name, gender, birthday))
        # 返回最后一次插入的 ID
        return c.lastrowid


def get_user(conn: Connection, id_: int) -> Dict[str, Any]:
    """
    查询一个用户数据

    Args:
        conn (Connection): 数据库连接对象
        id_ (int): 主键 ID

    Returns:
        Dict[str, Any]: 用户信息字典
    """
    sql = r"SELECT `id`, `id_num`, `name`, `gender`, `birthday` FROM `core_users` WHERE `id` = %s"

    with conn.cursor() as c:
        c.execute(sql, (id_,))
        # 获取查询结果 (一行)
        return c.fetchone()


def update_user(conn: Connection, id_: int, id_num: str, name: str, gender: str, birthday: date) -> int:
    """
    更新用户信息

    Args:
        conn (Connection): 数据库连接对象
        id_ (int): 主键 ID
        id_num (str): 身份证号
        name (str): 姓名
        gender (str): 性别
        birthday (date): 生日

    Returns:
        int: 受影响的行数, 保持为 1
    """
    sql = r"UPDATE `core_users` SET `id_num` = %s, `name` = %s, `gender` = %s, `birthday` = %s WHERE `id` = %s"

    with conn.cursor() as c:
        return c.execute(sql, (id_num, name, gender, birthday, id_))


def delete_user(conn: Connection, id_: int) -> int:
    """
    删除用户数据

    Args:
        conn (Connection): 数据库连接对象
        id_ (int): 主键 ID

    Returns:
        int: 删除的行数, 保持为 1
    """
    sql = r"DELETE from `core_users` WHERE `id` = %s"

    with conn.cursor() as c:
        return c.execute(sql, (id_))
