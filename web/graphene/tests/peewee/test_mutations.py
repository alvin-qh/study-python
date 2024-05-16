from peewee_ import DepartmentModel, EmployeeModel

from . import BaseTest
from .factories import DepartmentModelFactory
from .graphqls import CREATE_DEPARTMENT, CREATE_EMPLOYEE


class TestMutation(BaseTest):
    """数据变更操作测试"""

    def test_department_mutation(self) -> None:
        """测试创建部门"""
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

        output = result["data"]["createDepartment"]
        assert (
            DepartmentModel.get_or_none(DepartmentModel.id == int(output["id"]))
            is not None
        )
        assert output["name"] == "研发部"

    def test_employee_mutation(self) -> None:
        """测试创建员工"""
        department = DepartmentModelFactory.create(level=1)

        result = self.client.execute(
            CREATE_EMPLOYEE,
            variables={
                "createEmployeeInput": {
                    "name": "Alvin",
                    "gender": "MALE",
                    "departmentId": department.id,
                    "role": "manager",
                }
            },
        )
        assert result is not None
        assert result["data"] is not None
        assert result["data"]["createEmployee"] is not None

        output = result["data"]["createEmployee"]
        assert (
            EmployeeModel.get_or_none(EmployeeModel.id == int(output["id"])) is not None
        )
        assert output["name"] == "Alvin"
