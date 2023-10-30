from datetime import date

from alchemy import initialize_tables, session
from alchemy.service import (
    add_user_into_group,
    create_group,
    create_user,
    get_group,
    get_user,
    get_user_group_with_user_and_group,
    update_user,
)


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


def test_create_user() -> None:
    """
    测试用户实体的创建和查询
    """

    # 创建用户实体对象
    user = create_user(
        id_num="61010419810303210X",
        name="Alvin",
        gender="M",
        birthday=date(1981, 3, 17),
    )
    assert user
    assert user.id
    assert user.id_num == "61010419810303210X"

    # 查询所创建的用户实体对象
    found_user = get_user(user.id)
    assert user == found_user


def test_update_user() -> None:
    """
    测试更新用户实体对象
    """

    # 创建用户实体对象
    user = create_user(
        id_num="61010419810303210X",
        name="Alvin",
        gender="M",
        birthday=date(1981, 3, 17),
    )

    # 更新用户实体对象
    user = update_user(
        user.id,
        id_num="61010419810303290X",
        name="Emma",
        gender="F",
        birthday=date(1981, 3, 29),
    )

    # 查询所创建的用户实体对象
    user = get_user(user.id)
    assert user.id_num == "61010419810303290X"
    assert user.gender == "F"


def test_user_soft_delete() -> None:
    """
    测试对用户实体的软删除
    """

    # 创建用户实体对象
    user = create_user(
        id_num="61010419810303210X",
        name="Alvin",
        gender="M",
        birthday=date(1981, 3, 17),
    )

    # 执行软删除
    user.soft_delete()
    session.commit()

    # 查询所创建的用户实体对象
    user = get_user(user.id)
    assert user is None


def test_create_group() -> None:
    """
    测试创建组实体对象
    """
    group = create_group("G1")
    assert group.id

    found_group = get_group(group.id)
    assert found_group == group


def test_add_user_into_group() -> None:
    """
    测试将用户添加到组中
    """

    # 创建用户实体对象
    user = create_user(
        id_num="61010419810303210X",
        name="Alvin",
        gender="M",
        birthday=date(1981, 3, 17),
    )

    # 创建组对象
    group = create_group("G1")

    # 将用户加入组中
    user_group = add_user_into_group(user.id, group.id)
    assert user_group.user_id == user.id
    assert user_group.group_id == group.id

    # 查看用户对象上的组关系
    user = get_user(user.id)
    assert user.user_group[0] == user_group
    assert user.groups[0] == group

    # 查看组的用户关系
    group = get_group(group.id)
    assert group.user_group[0] == user_group
    assert group.users[0] == user


def test_join_user_and_group() -> None:
    """
    通过 join 方式查询用户和组
    """

    # 创建用户实体对象
    user = create_user(
        id_num="61010419810303210X",
        name="Alvin",
        gender="M",
        birthday=date(1981, 3, 17),
    )

    # 创建组对象
    group = create_group("G1")

    # 将用户加入组中
    user_group = add_user_into_group(user.id, group.id)
    assert user_group.user_id == user.id
    assert user_group.group_id == group.id

    # 联合查询, 同时获取组关系, 用户对象和组对象
    found_user_group, found_user, found_group = get_user_group_with_user_and_group(
        user_group.id
    )
    assert found_user_group == user_group
    assert found_user == user
    assert found_group == group
