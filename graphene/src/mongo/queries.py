from typing import Literal, Optional, cast

from graphene import Field, ObjectType, ResolveInfo, String

from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .types import Department, Employee


class DepartmentQuery(ObjectType):
    """部门查询类"""

    # 表示要查询 `Department` 类型结果
    department: Department = Field(
        Department,
        args={
            "name": String(required=True),  # 定义查询参数, 表示部门名称
        },
    )

    @staticmethod
    def resolve_department(
        parent: Literal[None], info: ResolveInfo, name: str
    ) -> Optional[DepartmentModel]:
        """解析 `department` 字段, 表示输出查询结果

        Args:
            - `name` (`str`): 查询参数, 表示部门名称

        Returns:
            `DepartmentModel`: 查询结果, 表示部门实体对象
        """
        return cast(
            Optional[DepartmentModel], DepartmentModel.objects(name=name).first()
        )


class EmployeeQuery(ObjectType):
    """员工查询类型"""

    # 表示要查询 `Employee` 类型结果
    employee: Employee = Field(
        Employee,
        args={
            "name": String(required=True),  # 定义查询参数, 表示员工姓名
        },
    )

    @staticmethod
    def resolve_employee(
        parent: Literal[None], info: ResolveInfo, name: str
    ) -> Optional[EmployeeModel]:
        """解析 `employee` 字段, 表示根据员工姓名查询员工对象

        Args:
            - `name` (`str`): 查询参数, 表示员工姓名

        Returns:
            `Optional[EmployeeModel]`: 查询结果, 为员工实体对象
        """
        return cast(Optional[EmployeeModel], EmployeeModel.objects(name=name).first())
