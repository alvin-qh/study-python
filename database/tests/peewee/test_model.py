from random import randint
from typing import Any, Generator, List, Optional, Type

import factory.base
import factory.faker
import factory.fuzzy
from peewee import Model
from peewee_ import (
    Department,
    Employee,
    Gender,
    Org,
    Role,
    context,
    db,
    initialize_tables,
)
from pytest import fixture

from . import non_none


class PeeweeOptions(factory.base.FactoryOptions):
    """定义 Peewee 工厂属性"""

    def _build_default_options(self) -> List[factory.base.OptionDefault]:
        """为工厂构建默认属性值

        Returns:
            `List[factory.base.OptionDefault]`: 返回工厂默认属性集合
        """
        defaults: List[factory.base.OptionDefault] = super()._build_default_options()
        return defaults + []


class PeeweeFactory(factory.base.Factory):
    """定义 Peewee 工厂类型, 用于自动构建 Peewee 实体对象"""

    # 指定提供工厂属性的类型
    _options_class = PeeweeOptions

    class Meta:
        """定义工厂类型元数据"""

    @classmethod
    def _create(cls, model_class: Type[Model], *args: Any, **kwargs: Any) -> Any:
        """定义实体创建方法

        Args:
            - `model_class` (`Type[Model]`): 要创建的实体对象的类型

        Returns:
            Any: 被创建的实体对象
        """
        # 创建实体对象
        model = model_class(*args, **kwargs)

        # 实体对象持久化
        model.save()

        return model


class OrgFactory(PeeweeFactory):
    """组织实体对象工厂类"""

    class Meta:
        # 指定实体类型
        model = Org

    # 构建组织名称字段
    name: str = factory.faker.Faker("name")


class DepartmentFactory(PeeweeFactory):
    """部门实体对象工厂类"""

    class Meta:
        # 指定实体类型
        model = Department

    # 构建部门名称字段
    name: str = factory.faker.Faker("name")

    # 构建部门等级字段
    level: int = factory.fuzzy.FuzzyInteger(1, 10)


class RoleFactory(PeeweeFactory):
    """角色实体对象工厂类"""

    class Meta:
        # 指定实体类型
        model = Role

    # 构建角色名称字段
    name: str = factory.faker.Faker("name")


class EmployeeFactory(PeeweeFactory):
    """员工实体对象工厂类"""

    class Meta:
        # 指定实体类型
        model = Employee

    # 构建员工名称字段
    name: str = factory.faker.Faker("name")

    # 构建员工性别字段
    gender: Gender = factory.LazyFunction(
        lambda: Gender.MALE if randint(0, 1) == 0 else Gender.FEMALE
    )

    # 构建员工角色字段
    role: Role = factory.LazyFunction(lambda: RoleFactory.create())


# 保存当前组织对象
current_org: Optional[Org] = None

# 保存当前用户对象
current_user: Optional[Employee] = None


@fixture(scope="module", autouse=True)
def build_test_context() -> Generator[None, None, None]:
    """为当前测试模块构建测试上下文"""
    global current_org, current_user

    with db.transaction():
        if current_org is None:
            initialize_tables()

            current_org = OrgFactory.create()
            with context.with_tenant_context(current_org):
                role = RoleFactory.create(name="admin")
                current_user = EmployeeFactory.create(role=role)

    with context.with_tenant_context(current_org):
        with context.with_current_user(current_user):
            yield

    assert current_org is not None


def test_current_org() -> None:
    """测试 `current_org` 变量是否正确赋值"""
    assert current_org is not None

    # 根据 id 查询 Org 对象, 确保 current_org 中的对象已被持久化
    org = Org.get_by_id(current_org.id)
    assert org == current_org

    # 确认 current_org 对象已进入线程上下文中
    org = context.get_current_tenant()
    assert org == current_org


def test_current_user() -> None:
    """测试 `current_user` 变量是否正确赋值"""
    assert current_user is not None

    # 根据 id 查询 Employee 对象, 确保 current_user 中的对象已被持久化
    user: Employee = Employee.get_by_id(current_user.id)
    assert user == current_user

    # 确认 current_org 对象已进入线程上下文中
    user = context.get_current_user()
    assert user == current_user

    # 确认上下文用户的角色为 admin
    role: Role = user.role
    assert role.name == "admin"


def test_create_department() -> None:
    with db.atomic():
        employee: Employee = EmployeeFactory.create()
        department: Department = DepartmentFactory.create(manager=employee)

    department = non_none(
        Department.select().where(Department.id == department.id).get_or_none()
    )

    assert department.org_id == context.get_current_tenant().id
    assert department.created_by == context.get_current_user().id
    assert department.manager == employee


def test_join() -> None:
    """测试 join 查询

    ```sql
    SELECT d.*, e.*
    FROM department AS d
    JOIN employee AS e on d.manager_id = e.id
    WHERE e.id = :id
    ```
    """

    with db.atomic():
        employee: Employee = EmployeeFactory.create()
        department: Department = DepartmentFactory.create(manager=employee)

    # 定义实体别名
    alias_d: Department = Department.alias("d")
    alias_e: Employee = Employee.alias("e")

    # 通过联合查询查询部门实体结果
    department = non_none(
        (
            alias_d.select()
            .join(alias_e, on=(alias_d.manager == alias_e.id))
            .where(alias_e.id == employee.id)  # type:ignore
        ).get_or_none()
    )

    # 确认查询结果
    assert department is not None
    assert department.org_id == context.get_current_tenant().id
    assert department.created_by == context.get_current_user().id
    assert department.manager == employee


def test_sub_query() -> None:
    """测试子查询

    ```sql
    SELECT d.*
    FROM department AS d
    WHERE d.manager_id IN (
        SELECT e.id
        FROM Employee AS e
        WHERE e.name = :name
    )
    ```
    """

    with db.atomic():
        employee: Employee = EmployeeFactory.create()
        department: Department = DepartmentFactory.create(manager=employee)

    sub_query = Employee.select(Employee.id).where(Employee.name == employee.name)

    department = non_none(
        Department.select().where(Department.manager.in_(sub_query)).get_or_none()
    )

    # 确认查询结果
    assert department.org_id == context.get_current_tenant().id
    assert department.created_by == context.get_current_user().id
    assert department.manager == employee
