from typing import Any, Generator, Optional, cast

import factory
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
    class Meta:
        pass

    pass


class OrgFactory(BaseFactory):
    class Meta:
        model = Org

    name: str = factory.Sequence(lambda n: f"Org-{n}")


class DepartmentFactory(BaseFactory):
    class Meta:
        model = Department

    name: str = factory.Sequence(lambda n: f"Department-{n}")


class RoleFactory(BaseFactory):
    class Meta:
        model = Role


class EmployeeFactory(BaseFactory):
    class Meta:
        model = Employee

    name: str = factory.Sequence(lambda n: f"Employee-{n}")


current_org: Optional[Org] = None


@fixture(scope="module", autouse=True)
def org_context() -> Generator[None, Any, None]:
    global current_org

    if current_org is None:
        clear_db()
        ensure_indexes()

        current_org = cast(Org, OrgFactory.create())

        with context.with_tenant_context(current_org):
            RoleFactory.create(name="manager")
            RoleFactory.create(name="member")

    with context.with_tenant_context(current_org):
        yield


def test_create_org() -> None:
    assert current_org is not None

    org = Org.objects(name=current_org.name).first()
    assert org == current_org


def test_create_department() -> None:
    created_dept: Department = DepartmentFactory.create()

    dept = Department.objects(name=created_dept.name).first()
    assert dept == created_dept
    assert dept.org == context.get_current_tenant()


def test_create_employee() -> None:
    department: Department = DepartmentFactory.create()
    role = Role.objects(name="manager").first()

    created_employee: Employee = EmployeeFactory.create().set_department(
        department, role
    )

    employee = Employee.objects(name=created_employee.name).first()
    assert employee == created_employee
    assert employee.role == role
    assert employee == department.manager

    assert department == employee.department
