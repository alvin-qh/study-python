from datetime import date
from typing import Optional, Tuple

from sqlalchemy import and_, orm, select

from .model import Group, User, UserGroup, session


def create_user(id_num: str, name: str, gender: str, birthday: date) -> User:
    """
    创建用户

    Args:
        id_num (str): 身份证号
        name (str): 姓名
        gender (str): 性别
        birthday (date): 生日

    Returns:
        User: 用户实体对象
    """
    user = User(
        id_num=id_num,
        name=name,
        gender=gender,
        birthday=birthday,
    )
    session.add(user)
    session.commit()
    return user


def get_user(id_: int) -> Optional[User]:
    """
    根据用户 ID 查询用户实体对象

    select * from core_user where id = id_
    """
    return session.scalars(select(User).where(User.id == id_)).one()


def update_user(
    id_: int, *, id_num: str, name: str, gender: str, birthday: date
) -> Optional[User]:
    """
    根据 ID 更新用户对象

    Args:
        id_ (int): 用户实体 ID
        id_num (str): 身份证号
        name (str): 姓名
        gender (str): 性别
        birthday (date): 生日

    Returns:
        User: 用户实体对象
    """
    user = session.scalars(select(User).where(User.id == id_)).one()
    if not user:
        return None

    user.id_num = id_num
    user.name = name
    user.gender = gender
    user.birthday = birthday

    session.commit()

    return user


def create_group(name: str) -> Group:
    """
    创建一个组对象

    Args:
        name (str): 组名称

    Returns:
        Group: 组对象
    """
    group = Group(
        name=name,
    )
    session.add(group)
    session.commit()

    return group


def get_group(id_: int) -> Optional[Group]:
    """
    根据组 ID 获取组实体对象

    Args:
        id_ (int): 组 ID

    Returns:
        Optional[Group]: 组实体对象
    """
    return session.query(Group).filter(Group.id == id_).one()


def add_user_into_group(user_id: int, group_id: int) -> UserGroup:
    """
    将用户添加到组中

    Args:
        user_id (int): 用户 ID
        group_id (int): 组 ID

    Returns:
        UserGroup: 用户组关系对象
    """
    # 判断用户是否已经在组中
    user_group = session.scalars(
        select(UserGroup)
        .where(UserGroup.user_id == user_id)
        .where(UserGroup.group_id == group_id)
    ).first()

    if user_group:
        return user_group

    # 创建用户组对象
    user_group = UserGroup(
        user_id=user_id,
        group_id=group_id,
    )
    session.add(user_group)
    session.commit()

    return user_group


def get_user_group_with_user_and_group(id_: int) -> Tuple[UserGroup, User, Group]:
    """
    联合查询

    通过 join 可以在一条 SQL 语句中连接多个表, 同时对相关联的多个实体对象进行查询

    操作方式为 query.join(model/alias, conditions), 其中:
        join 会自动生成 on a.id = b.id 的连接条件，即
            session.query(UserGroup) \
                .join(u) \
                .join(g)
        相当于
            session.query(UserGroup) \
                .join(u, and_(u.id == UserGroup.user_id)) \
                .join(g, and_(g.id == UserGroup.group_id))

    本例中会生成如下 SQL:

    SELECT * FROM core_user_group
        JOIN core_user u ON ug.user_id = u.id
        JOIN core_group g ON ug.group_id = g.id
        WHERE ug.id = id_

    Args:
        id_ (int): 用户组关系 ID

    Returns:
        Tuple[UserGroup, User, Group]: 同时返回三个实体对象
    """
    u = orm.aliased(User, name="u")
    g = orm.aliased(Group, name="g")

    return (
        # 这里同时查询了三个实体类型, 所以返回值的每一行包含这三个结果
        # 由于 UserGroup 是根实体, 必须包括. 其余两个实体可选
        session.query(UserGroup, User, Group)
        .join(u)
        .join(g)
        .filter(UserGroup.id == id_)
        .one()
    )
