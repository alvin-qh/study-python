from mongo.core.context import context
from mongo.models import Department, Employee, Org, Role

from . import BaseTest
from .helper.factories import DepartmentFactory, EmployeeFactory, OrgFactory


class TestModules(BaseTest):
    def test_create_org(self) -> None:
        org = OrgFactory.create()
        assert Org.objects(name=org.name).first() == org

    def test_create_department(self) -> None:
        created_dept: Department = DepartmentFactory.create()

        dept = Department.objects(name=created_dept.name).first()
        assert dept == created_dept
        assert dept.org == context.get_current_org()

    def test_create_employee(self) -> None:
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
