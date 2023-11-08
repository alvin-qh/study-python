from graphql_relay import from_global_id, to_global_id
from mongo import DepartmentModel

from . import BaseTest
from .factories import DepartmentModelFactory
from .graphqls import CREATE_DEPARTMENT, CREATE_EMPLOYEE


class TestMutation(BaseTest):
    def test_department_mutation(self) -> None:
        result = self.client.execute(
            CREATE_DEPARTMENT,
            variables={
                "createDepartmentInput": {
                    "name": "研发部",
                    "level": 2,
                },
            },
        )
        assert result is not None

        assert result["data"] is not None
        assert result["data"]["createDepartment"] is not None

        department = result["data"]["createDepartment"]["department"]
        assert department["name"] == "研发部"
        assert department["level"] == 2

        assert DepartmentModel.objects(name="研发部").get() is not None

    def test_employee_mutation(self) -> None:
        department = DepartmentModelFactory.create(level=1)

        result = self.client.execute(
            CREATE_EMPLOYEE,
            variables={
                "createEmployeeInput": {
                    "name": "Alvin",
                    "gender": "male",
                    "departmentId": str(department.id),
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
