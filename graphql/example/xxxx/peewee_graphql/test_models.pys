from peewee_graphql.core.context import context
from peewee_graphql.models import (
    Role,
    Org,
    Department,
    Employee
)
from tests.peewee_graphql import BaseTest


class TestModel(BaseTest):
    def test_org(self):
        current_org = context.get_current_org()
        org = Org.select().where(Org.id == current_org.id).get()
        assert org == current_org

    def test_role(self):
        role = Role.select().where(Role.name == "member").get()
        assert role.name == "member"
        assert role.org_id == context.get_current_org().id

    def test_department(self):
        new_department = Department(
            name="研发部",
            level=1
        )
        new_department.save()

        current_org = context.get_current_org()
        assert new_department.org_id == current_org.id

        department = Department.select().where(Department.id == new_department.id).get()
        assert department == new_department

    def test_employee(self):
        department1 = Department(name="采购部", level=1)
        department1.save()

        department2 = Department(name="市场部", level=1)
        department2.save()

        users = [
            [
                ("张鹤轩", "M"),
                ("王博超", "M"),
                ("李淳雅", "F"),
                ("宋博文", "M")
            ],
            [
                ("段伟祺", "F"),
                ("马心怡", "F"),
                ("王昊然", "M")
            ]
        ]
        for department, user_group in zip([department1, department2], users):
            for n, (name, gender) in enumerate(user_group):
                if n == 0:
                    role = self.role_manager
                else:
                    role = self.role_member

                employee = Employee(
                    name=name,
                    gender=gender,
                    department=department,
                    role=role
                )
                employee.save()

                if n == 0:
                    department.manager = employee
                    department.save()

        user_names = set(map(lambda user: user[0], users[0]))

        department = Department.select().where(Department.name == "采购部").get()
        assert len(department.employees) == 4
        for employee in department.employees:
            assert employee.name in user_names

        assert department.manager.name == "张鹤轩"
        assert department.manager.role.name == "manager"

        user_names = set(map(lambda user: user[0], users[1]))

        department = Department.select().where(Department.name == "市场部").get()
        assert len(department.employees) == 3
        for employee in department.employees:
            assert employee.name in user_names

        assert department.manager.name == "段伟祺"
        assert department.manager.role.name == "manager"

        role = Role.select().where(Role.name == "manager")
        employees = list(Employee.select().where(Employee.role == role))
        assert len(employees) == 3
        assert employees[0].name in {context.get_current_user().name, "张鹤轩", "段伟祺"}
        assert employees[1].name in {context.get_current_user().name, "张鹤轩", "段伟祺"}
        assert employees[2].name in {context.get_current_user().name, "张鹤轩", "段伟祺"}
