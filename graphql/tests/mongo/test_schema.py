from graphql_relay import from_global_id, to_global_id
from mongo.models import Department
from mongo.models import Role as RoleModel
from mongoengine import Document

from . import BaseTest
from .helper.factories import DepartmentFactory, EmployeeFactory
from .helper.queries import (
    CREATE_DEPARTMENT,
    CREATE_EMPLOYEE,
    QUERY_DEPARTMENT_BY_NAME,
    QUERY_EMPLOYEE_BY_NAME,
    QUERY_EMPLOYEES_BY_DEPARTMENT,
)


class TestQueries(BaseTest):
    @staticmethod
    def make_global_id(doc: Document) -> str:
        return to_global_id(doc.__class__.__name__, doc.id)

    @staticmethod
    def make_cursor(cursor: int) -> str:
        return to_global_id("arrayconnection", cursor)

    def setup_method(self) -> None:
        super().setup_method()

        self.role_manager = RoleModel.objects(name="manager").get()
        assert self.role_manager

        self.role_member = RoleModel.objects(name="member").get()
        assert self.role_member

        self.department1 = DepartmentFactory.create(level=1)
        self.department2 = DepartmentFactory.create(level=2)

        self.employee1 = EmployeeFactory.create(
            department=self.department1, role=self.role_manager
        )
        self.employee2 = EmployeeFactory.create(
            department=self.department1, role=self.role_member
        )
        self.employee3 = EmployeeFactory.create(
            department=self.department2, role=self.role_manager
        )

        self.department1.manager = self.employee1
        self.department1.save()

        self.department2.manager = self.employee3
        self.department2.save()

    def test_query_department(self) -> None:
        result = self.client.execute(
            QUERY_DEPARTMENT_BY_NAME, variables={"name": self.department1.name}
        )
        assert result == {
            "data": {
                "department": {
                    "id": self.make_global_id(self.department1),
                    "name": self.department1.name,
                    "level": self.department1.level,
                    "manager": {
                        "id": self.make_global_id(self.employee1),
                        "name": self.employee1.name,
                        "gender": self.employee1.gender.value,
                        "role": {"name": self.role_manager.name},
                    },
                }
            }
        }

    def test_query_employee(self) -> None:
        result = self.client.execute(
            QUERY_EMPLOYEE_BY_NAME, variables={"name": self.employee2.name}
        )
        assert result == {
            "data": {
                "employee": {
                    "id": self.make_global_id(self.employee2),
                    "department": {
                        "id": self.make_global_id(self.department1),
                        "level": self.department1.level,
                        "manager": {
                            "id": self.make_global_id(self.employee1),
                            "gender": self.employee1.gender.value,
                            "name": self.employee1.name,
                            "role": {"name": self.role_manager.name},
                        },
                        "name": self.department1.name,
                    },
                    "gender": self.employee2.gender.value,
                    "name": self.employee2.name,
                    "role": {"name": self.role_member.name},
                }
            }
        }

    def test_query_employees(self) -> None:
        result = self.client.execute(
            QUERY_EMPLOYEES_BY_DEPARTMENT,
            variables={
                "departmentName": self.department1.name,
                "offset": 0,
                "after": self.make_cursor(0),
            },
        )
        assert result == {
            "data": {
                "employees": {
                    "edges": [
                        {
                            "node": {
                                "department": {
                                    "id": self.make_global_id(self.department1)
                                },
                                "gender": self.employee2.gender.value,
                                "id": self.make_global_id(self.employee2),
                                "name": self.employee2.name,
                                "role": {"name": self.role_member.name},
                            }
                        }
                    ],
                    "pageInfo": {
                        "endCursor": self.make_cursor(1),
                        "hasNextPage": False,
                        "hasPreviousPage": False,
                        "startCursor": self.make_cursor(1),
                    },
                }
            }
        }


class TestMutation(BaseTest):
    def test_department_mutation(self) -> None:
        result = self.client.execute(
            CREATE_DEPARTMENT,
            variables={"departmentInput": {"name": "研发部", "level": 2}},
        )
        assert result is not None

        data = result["data"]["departmentMutation"]
        assert len(data) == 1

        department = data["department"]
        assert department["name"] == "研发部"
        assert department["level"] == 2

        assert Department.objects(name="研发部").get()

    def test_employee_mutation(self) -> None:
        department = DepartmentFactory.create(level=1)

        result = self.client.execute(
            CREATE_EMPLOYEE,
            variables={
                "employeeInput": {
                    "name": "Alvin",
                    "gender": "male",
                    "department": to_global_id(
                        department.__class__.__name__, department.id
                    ),
                    "role": "manager",
                }
            },
        )
        assert result is not None

        data = result["data"]["employeeMutation"]
        assert len(data) == 1

        employee = data["employee"]
        assert employee["name"] == "Alvin"
        assert employee["gender"] == "male"
        assert employee["department"]["id"] == to_global_id(
            department.__class__.__name__, department.id
        )
        assert employee["role"]["name"] == "manager"

        department.reload()
        type_, id_ = from_global_id(employee["id"])
        assert type_ == "Employee"
        assert str(department.manager.id) == id_
        assert department.manager.name == "Alvin"
