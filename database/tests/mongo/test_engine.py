from typing import Generator, Optional

import factory
import factory.faker
from factory.mongoengine import MongoEngineFactory
from mongo.engine import (
    Department,
    Employee,
    Org,
    Role,
    clear_db,
    context,
    ensure_indexes,
)
from pytest import fixture


class BaseFactory(MongoEngineFactory):
    """匹配 mongo engine 框架的工厂类"""

    class Meta:
        """工厂元数据类"""


class OrgFactory(BaseFactory):
    """组织实体工厂类"""

    class Meta:
        # 定义实体类型
        model = Org

    # 组织名称属性
    name: str = factory.faker.Faker("name")


class DepartmentFactory(BaseFactory):
    """部门实体工厂类"""

    class Meta:
        # 定义实体类型
        model = Department

    # 部门名称属性
    name: str = factory.faker.Faker("name")


class RoleFactory(BaseFactory):
    """角色实体工厂类"""

    class Meta:
        # 定义实体类型
        model = Role

    # 角色名称属性
    name: str = factory.faker.Faker("name")


class EmployeeFactory(BaseFactory):
    """员工实体工厂类"""

    class Meta:
        # 定义实体类型
        model = Employee

    # 员工姓名属性
    name: str = factory.faker.Faker("name")


current_org: Optional[Org] = None


@fixture(scope="module", autouse=True)
def build_test_context() -> Generator[None, None, None]:
    """构建测试上下文"""
    global current_org

    if current_org is None:
        # 清空当前数据库
        clear_db()

        # 重建文档索引
        ensure_indexes()

        # 创建当前组织实体
        current_org = OrgFactory.create()

        with context.with_tenant_context(current_org):
            # 创建角色实体
            RoleFactory.create(name="manager")
            RoleFactory.create(name="member")

    # 进入上下文作用域
    with context.with_tenant_context(current_org):
        yield


def test_current_org() -> None:
    """测试当前组织实体"""
    assert current_org is not None

    # 从数据库中查询当前组织实体
    org: Org = Org.objects(name=current_org.name).first()
    # 确认 current_org 和查询结果一致
    assert org == current_org

    # 从上下文中获取当前组织实体
    org = context.get_current_tenant()
    # 确认上下文中的实体对象
    assert org == current_org


def test_create_department() -> None:
    """测试创建部门实体"""
    expected_dept: Department = DepartmentFactory.create()

    dept = Department.objects(name=expected_dept.name).first()
    assert dept == expected_dept
    assert dept.org == context.get_current_tenant()


def test_create_employee() -> None:
    """测试创建员工实体"""
    department: Department = DepartmentFactory.create()
    role: Role = Role.objects(name="manager").first()

    expected_employee: Employee = EmployeeFactory.create().set_department(
        department, role
    )

    employee: Employee = Employee.objects(name=expected_employee.name).first()
    assert employee == expected_employee
    assert employee.org == context.get_current_tenant()
    assert employee.role == role
    assert employee == department.manager

    assert department == employee.department
