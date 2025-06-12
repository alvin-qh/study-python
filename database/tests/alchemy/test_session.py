from datetime import date

from sqlalchemy import and_, column, select, table
from sqlalchemy.orm import aliased

from database.alchemy import initialize_tables, session


def setup_function() -> None:
    """
    在每个测试执行前执行, 初始化所有数据表
    """
    initialize_tables()


def teardown_function() -> None:
    """
    在每个测试结束后执行, 关闭连接
    """
    session.close()


def test_insert_and_query() -> None:
    """
    测试插入数据和查询数据
    """

    # 通过 table 函数描述一个数据表
    t_user = table(
        "user",
        column("id"),
        column("id_num"),
        column("name"),
        column("gender"),
        column("birthday"),
        column("deleted"),
    )

    # 执行插入操作, 获取插入数据的 ID
    # session.execute 用于执行一条 SQL 语句
    id_ = session.execute(
        t_user.insert().values(
            id_num="61010419810303210X",
            name="Alvin",
            gender="M",
            birthday=date(1981, 3, 17),
            deleted=False,
        )
    ).lastrowid

    session.commit()

    # 执行一条查询语句
    # 对于 one() 函数， 返回一个 dict 对象, 包含查询结果
    user = (
        session.execute(select(t_user).where(t_user.c.id == id_))
        .mappings()
        .one_or_none()
    )

    assert user is not None

    # 检查查询结果
    assert len(user) == 6
    assert user["id"]
    assert user["id_num"] == "61010419810303210X"
    assert user["name"] == "Alvin"
    assert user["gender"] == "M"
    assert user["birthday"] == "1981-03-17"
    assert user["deleted"] == 0


def test_query_by_select() -> None:
    """
    测试插入数据和查询数据
    """

    # 通过 table 函数描述一个数据表
    t_user = table(
        "user",
        column("id"),
        column("id_num"),
        column("name"),
        column("gender"),
        column("birthday"),
        column("deleted"),
    )

    # 插入一条数据
    id_ = session.execute(
        t_user.insert().values(
            id_num="61010419810303210X",
            name="Alvin",
            gender="M",
            birthday=date(1981, 3, 17),
            deleted=False,
        )
    ).lastrowid

    session.commit()

    # 执行一条 select 语句
    # 返回一个 CursorResult 对象, 表示结果集
    res = session.execute(t_user.select().where(t_user.c.id == id_)).mappings()

    # CursorResult 对象可迭代, 获取其第一项
    # 获取结果为 dict, 表示查询一行的结果
    user = next(res)

    assert len(user) == 6
    assert user["id"]
    assert user["id_num"] == "61010419810303210X"
    assert user["name"] == "Alvin"
    assert user["gender"] == "M"
    assert user["birthday"] == "1981-03-17"
    assert user["deleted"] == 0


def test_update() -> None:
    """
    测试数据更新
    """

    # 通过 table 函数描述一个数据表
    t_user = table(
        "user",
        column("id"),
        column("id_num"),
        column("name"),
        column("gender"),
        column("birthday"),
        column("deleted"),
    )

    # 插入一条数据
    id_ = session.execute(
        t_user.insert().values(
            id_num="61010419810303210X",
            name="Alvin",
            gender="M",
            birthday=date(1981, 3, 17),
            deleted=False,
        )
    ).lastrowid

    session.commit()

    # 执行 update 语句更新数据
    # 返回影响的行数
    rowcount = session.execute(
        t_user.update().where(t_user.c.id == id_).values(birthday=date(1981, 3, 19))
    ).rowcount

    session.commit()
    assert rowcount == 1

    # 查询用户对象, 验证更新结果
    user = (
        session.execute(select(t_user).where(t_user.c.id == id_))
        .mappings()
        .one_or_none()
    )
    assert user is not None
    assert user["birthday"] == "1981-03-19"


def test_delete() -> None:
    """
    测试数据删除
    """

    # 通过 table 函数描述一个数据表
    t_user = table(
        "user",
        column("id"),
        column("id_num"),
        column("name"),
        column("gender"),
        column("birthday"),
        column("deleted"),
    )

    # 插入一条数据
    id_ = session.execute(
        t_user.insert().values(
            id_num="61010419810303210X",
            name="Alvin",
            gender="M",
            birthday=date(1981, 3, 17),
            deleted=False,
        )
    ).lastrowid

    session.commit()

    # 执行 delete 删除数据
    # 返回影响的行数
    rowcount = session.execute(t_user.delete().where(t_user.c.id == id_)).rowcount

    session.commit()
    assert rowcount == 1

    # 查询用户对象, 验证删除结果
    user = (
        session.execute(select(t_user).where(t_user.c.id == id_))
        .mappings()
        .one_or_none()
    )
    assert user is None


def test_join() -> None:
    """
    测试多表连接
    """

    # 描述用户表
    t_user = table(
        "user",
        column("id"),
        column("id_num"),
        column("name"),
        column("gender"),
        column("birthday"),
        column("deleted"),
    )

    # 描述组表
    t_group = table("`group`", column("id"), column("name"))

    # 描述用户和组关系表
    t_user_group = table(
        "user_group", column("id"), column("user_id"), column("group_id")
    )

    # 插入用户数据
    user_id = session.execute(
        t_user.insert().values(
            id_num="61010419810303210X",
            name="Alvin",
            gender="M",
            birthday=date(1981, 3, 17),
            deleted=False,
        )
    ).lastrowid

    # 插入组数据
    group_id = session.execute(t_group.insert().values(name="VIP")).lastrowid

    # 插入用户组关系数据
    session.execute(
        t_user_group.insert().values(user_id=user_id, group_id=group_id)
    ).lastrowid

    session.commit()

    # 设置表别名
    ug = aliased(t_user_group, name="ug")
    u = aliased(t_user, name="u")
    g = aliased(t_group, name="g")

    # 通过 join 进行联合查询, 查询结果中包含 core_user, core_group 的结果
    results = (
        session.execute(
            select(
                ug,
                u,
                g,
                u.c.id.label("uid"),
                u.c.name.label("uname"),
                g.c.id.label("gid"),
                g.c.name.label("gname"),
            )
            .join(u, and_(ug.c.user_id == u.c.id))
            .join(g, and_(ug.c.group_id == g.c.id))
            .filter(u.c.id == user_id)
        )
        .mappings()
        .all()
    )

    assert len(results) == 1

    # 获取结果的第一行, 进行验证
    user = results[0]
    assert user["uid"]
    assert user["uname"] == "Alvin"
    assert user["gender"] == "M"
    assert user["birthday"] == "1981-03-17"
    assert user["deleted"] == 0
    assert user["gid"]
    assert user["gname"] == "VIP"
