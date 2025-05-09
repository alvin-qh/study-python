from datetime import date
from random import randint
from typing import List

from factory import faker, declarations
from alchemy import Gender, Group, User, initialize_tables, session
from alchemy.core import soft_deleted_select
from alchemy.model import UserGroup
from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy import and_, select, update
from sqlalchemy.orm import aliased

from misc import non_none


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = session

    pass


class UserFactory(BaseFactory):
    class Meta:
        model = User

    id_num = faker.Faker("ean", length=13)
    name = faker.Faker("name")
    gender = declarations.LazyFunction(
        lambda: Gender.MALE if randint(0, 1) == 0 else Gender.FEMALE
    )
    birthday = faker.Faker("date_object")


class GroupFactory(BaseFactory):
    class Meta:
        model = Group

    name = faker.Faker("name")


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


def test_find_user() -> None:
    """测试单表查询

    ```sql
    select * from core_user where id = id_
    ```
    """

    expected_user: User = UserFactory.create()
    session.commit()

    assert expected_user is not None

    actual_user = session.scalars(
        select(User).where(User.id == expected_user.id, User.deleted == False)  # noqa
    ).one_or_none()

    assert actual_user == expected_user


def test_find_user_legacy() -> None:
    """测试使用传统方式进行单表查询

    ```sql
    select * from core_user where id = id_
    ```

    由于这种写法可以使用到 `alchemy.core.ExtQuery` 类中定义的过滤器, 所以无需显式指定软删除字段条件
    """

    expected_user: User = UserFactory.create()
    session.commit()

    actual_user = session.query(User).filter(User.id == expected_user.id).one_or_none()
    assert actual_user == expected_user


def test_update_user() -> None:
    """测试通过修改实体对象更新数据

    修改实体对象并执行事务提交, 即可将对象修改的结果进行持久化
    """

    created_user: User = UserFactory.create()
    session.commit()

    user = session.scalars(select(User).where(User.id == created_user.id)).one_or_none()
    assert user is not None

    user.name = "Alvin"
    user.gender = Gender.MALE
    user.birthday = date(1981, 3, 17)
    session.commit()

    user = session.scalars(select(User).where(User.id == user.id)).one_or_none()
    assert user is not None

    assert user.name == "Alvin"
    assert user.gender == Gender.MALE
    assert user.birthday == date(1981, 3, 17)


def test_update_user_by_statement() -> None:
    """测试通过 update 语句更新数据

    通过执行 `update` 语句对数据表记录进行更新
    """

    created_user: User = UserFactory.create()
    session.commit()

    session.execute(
        update(User)
        .where(User.id == created_user.id)
        .values(name="Alvin", gender=Gender.MALE, birthday=date(1981, 3, 17))
    )
    session.commit()

    user = session.scalars(select(User).where(User.id == created_user.id)).one_or_none()
    assert user is not None

    assert user.name == "Alvin"
    assert user.gender == Gender.MALE
    assert user.birthday == date(1981, 3, 17)


def test_add_user_into_group() -> None:
    """测试关联表的使用"""

    # 创建 3 个用户
    users: List[User] = [UserFactory.create() for _ in range(3)]
    group: Group = GroupFactory.create()

    # 将用户逐一加到组中
    for user in users:
        session.add(UserGroup(user=user, group=group))
        session.commit()

    # 从数据库中刷新一次 group
    session.refresh(group)

    # 确认组中包含 3 个用户
    assert len(group.users) == 3

    # 确认组中的用户以及用户对应的组
    assert group.users[0] == users[0]
    assert group.users[0].groups[0] == group

    assert group.users[1] == users[1]
    assert group.users[1].groups[0] == group

    assert group.users[2] == users[2]
    assert group.users[2].groups[0] == group

    # 确认中间表的情况
    assert len(group.user_groups) == 3

    assert group.user_groups[0].user == users[0]
    assert group.user_groups[0].group == group

    assert group.user_groups[1].user == users[1]
    assert group.user_groups[1].group == group

    assert group.user_groups[2].user == users[2]
    assert group.user_groups[2].group == group


def test_join() -> None:
    """联合查询

    通过 `join` 可以在一条 SQL 语句中连接多个表, 同时对相关联的多个实体对象进行查询

    操作方式为 `query.join(model/alias, conditions)`, 其中:

    `join` 会自动生成 `on a.id = b.id` 的连接条件，即:

        ```python
        session.query(UserGroup) \\
            .join(u) \\
            .join(g)
        ```

        相当于

        ```python
        session.query(UserGroup) \\
            .join(u, and_(u.id == UserGroup.user_id)) \\
            .join(g, and_(g.id == UserGroup.group_id))
        ```

    本例中会生成如下 SQL:

    ```sql
    SELECT * FROM core_user_group
        JOIN core_user u ON ug.user_id = u.id
        JOIN core_group g ON ug.group_id = g.id
        WHERE ug.id = id_
    ```

    Args:
        - `id_` (`int`): 用户组关系 ID

    Returns:
        `Tuple[UserGroup, User, Group]`: 同时返回三个实体对象
    """

    expected_user: User = UserFactory.create()
    expected_group: Group = GroupFactory.create()

    session.add(UserGroup(user=expected_user, group=expected_group))
    session.commit()

    # 为实体定义别名
    alias_ug = aliased(UserGroup, name="ug")

    result = session.execute(
        select(User, Group)
        .select_from(User)
        .join(alias_ug)
        .join(Group)
        .where(and_(User.id == expected_user.id, User.deleted == False))  # noqa
    )
    assert result is not None

    user: User
    group: Group

    user, group = non_none(result.first())
    assert user == expected_user
    assert group == expected_group


def test_join_legacy() -> None:
    """联合查询

    通过 `join` 可以在一条 SQL 语句中连接多个表, 同时对相关联的多个实体对象进行查询

    操作方式为 `query.join(model/alias, conditions)`, 其中:

    `join` 会自动生成 `on a.id = b.id` 的连接条件，即:

        ```python
        session.query(UserGroup) \\
            .join(u) \\
            .join(g)
        ```

        相当于

        ```python
        session.query(UserGroup) \\
            .join(u, and_(u.id == UserGroup.user_id)) \\
            .join(g, and_(g.id == UserGroup.group_id))
        ```

    本例中会生成如下 SQL:

    ```sql
    SELECT * FROM core_user_group
        JOIN core_user u ON ug.user_id = u.id
        JOIN core_group g ON ug.group_id = g.id
        WHERE ug.id = id_
    ```

    Args:
        - `id_` (`int`): 用户组关系 ID

    Returns:
        `Tuple[UserGroup, User, Group]`: 同时返回三个实体对象
    """

    expected_user: User = UserFactory.create()
    expected_group: Group = GroupFactory.create()

    session.add(UserGroup(user=expected_user, group=expected_group))
    session.commit()

    # 为实体定义别名
    alias_u = aliased(User, name="u")
    alias_g = aliased(Group, name="g")

    user, group, _ = non_none(
        session.query(User, Group, UserGroup)
        .join(alias_u)
        .join(alias_g)
        .filter(alias_g.id == expected_group.id)
        .one_or_none()
    )

    assert user == expected_user
    assert group == expected_group


def test_soft_delete() -> None:
    """通过扩展的 `select` 函数进行软删除处理

    可以通过自定义的 `soft_deleted_select` 函数, 在其中附加软删除逻辑, 完成软删除的自动处理
    """
    created_user: User = UserFactory.create()
    session.commit()

    created_user.soft_delete()
    session.commit()

    user = session.scalars(
        soft_deleted_select(User).where(User.id == created_user.id)
    ).one_or_none()
    assert user is None


def test_soft_delete_legacy() -> None:
    """通过自定义查询类处理软删除

    通过自定义 `alchemy.core.ExtQuery` 类, 为软删除附加额外的过滤条件, 并在创建 `session` 对象时, 通过
    `query_cls=ExtQuery` 指定使用自定义查询类
    """
    created_user: User = UserFactory.create()
    session.commit()

    created_user.soft_delete()
    session.commit()

    user = session.query(User).filter(User.id == created_user.id).one_or_none()
    assert user is None
