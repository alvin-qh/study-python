from mongo_graphql.core.context import context
from mongo_graphql.models import (
    Org,
    Department,
    Employee,
    Role
)
from .factories import (
    OrgFactory,
    DepartmentFactory,
    EmployeeFactory
)
from ..mongo_graphql import BaseTest


class TestModules(BaseTest):
    def test_create_org(self):
        org = OrgFactory.create()
        assert Org.objects(name=org.name).first() == org

    def test_create_department(self):
        created_dept: Department = DepartmentFactory.create()

        dept = Department.objects(name=created_dept.name).first()
        assert dept == created_dept
        assert dept.org == context.get_current_org()

    def test_create_employee(self):
        department: Department = DepartmentFactory.create()
        role = Role.objects(name="manager").first()

        created_employee: Employee = (
            EmployeeFactory.create()
                .set_department(department, role)
        )

        employee = Employee.objects(name=created_employee.name).first()
        assert employee == created_employee
        assert employee.role == role
        assert employee == department.manager

        assert department == employee.department
