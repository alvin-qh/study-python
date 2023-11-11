import pytest
from peewee_ import DepartmentModel, EmployeeModel, RoleModel, make_cursor, pg_db

from . import BaseTest
from .factories import DepartmentModelFactory, EmployeeModelFactory
from .graphqls import QUERY_DEPARTMENT_BY_NAME, QUERY_EMPLOYEE_BY_NAME


class TestQueries(BaseTest):
    """查询测试"""

    def setup_method(self) -> None:
        """每次测试前进行初始化"""
        super().setup_method()

        with pg_db.atomic():
            # 获取已初始化好的角色对象
            self.manager_role: RoleModel = RoleModel.get(RoleModel.name == "manager")
            assert self.manager_role is not None

            self.member_role: RoleModel = RoleModel.get(RoleModel.name == "member")
            assert self.member_role

            # 创建 2 个部门对象
            self.department1: DepartmentModel = DepartmentModelFactory.create(level=1)
            self.department2: DepartmentModel = DepartmentModelFactory.create(level=2)

            # 创建 3 个员工对象, 前 2 个属于 部门 1, 后 1 个属于 部门 2
            self.employee1: EmployeeModel = EmployeeModelFactory.create(
                department=self.department1, role=self.manager_role
            )
            self.employee2: EmployeeModel = EmployeeModelFactory.create(
                department=self.department1, role=self.member_role
            )
            self.employee3: EmployeeModel = EmployeeModelFactory.create(
                department=self.department2, role=self.manager_role
            )

            # 为部门设置管理人员
            self.department1.manager = self.employee1
            self.department1.save()

            self.department2.manager = self.employee3
            self.department2.save()

    @pytest.mark.asyncio
    async def test_query_department(self) -> None:
        """测试查询部门

        根据部门名称查询部门数据
        """

        # 执行部门查询 Graphql 语句
        result = await self.client.execute_async(
            QUERY_DEPARTMENT_BY_NAME,
            variables={
                "name": self.department1.name,
                "gender": "MALE",
                "first": 10,
                "after": make_cursor(1),
            },
        )

        # 确认结果正确
        assert result == {
            "data": {
                "department": {
                    "id": str(self.department1.id),
                    "level": 1,
                    "name": self.department1.name,
                    "manager": {
                        "id": str(self.employee1.id),
                        "gender": "MALE",
                        "name": self.employee1.name,
                        "role": {
                            "name": "manager",
                        },
                    },
                    "employees": {
                        "edges": [
                            {
                                "node": {
                                    "id": str(self.employee2.id),
                                    "name": self.employee2.name,
                                    "gender": "MALE",
                                    "role": {
                                        "name": "member",
                                    },
                                }
                            }
                        ],
                        "pageInfo": {
                            "startCursor": "X19jdXJzb3JfXzox",
                            "endCursor": "X19jdXJzb3JfXzoz",
                            "hasNextPage": False,
                            "hasPreviousPage": True,
                        },
                    },
                }
            }
        }

    @pytest.mark.asyncio
    async def test_query_employee(self) -> None:
        """测试查询员工

        根据员工名称查询员工数据
        """

        # 执行员工查询 Graphql 语句
        result = await self.client.execute_async(
            QUERY_EMPLOYEE_BY_NAME,
            variables={
                "name": self.employee2.name,
            },
        )

        # 确认结果正确
        assert result == {
            "data": {
                "employee": {
                    "id": str(self.employee2.id),
                    "name": self.employee2.name,
                    "gender": "MALE",
                    "role": {
                        "name": "member",
                    },
                    "department": {
                        "id": str(self.department1.id),
                        "name": self.department1.name,
                        "level": 1,
                        "manager": {
                            "id": str(self.employee1.id),
                            "name": self.employee1.name,
                            "gender": "MALE",
                            "role": {
                                "name": "manager",
                            },
                        },
                    },
                }
            }
        }
