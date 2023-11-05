from typing import Any
from typing import List as ListType
from typing import Literal, Optional, cast

from graphene import ConnectionField, Field, ObjectType, ResolveInfo, String

from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .types import BaseConnection, Department, Employee, QueryError, QueryResult
from .utils import parse_cursor


class DepartmentQuery(ObjectType):
    department: Department = Field(
        Department,
        args={
            "name": String(required=True),
        },
    )

    @staticmethod
    def resolve_department(
        parent: Literal[None], info: ResolveInfo, name: str
    ) -> DepartmentModel:
        return cast(DepartmentModel, DepartmentModel.objects(name=name).first())


class EmployeeConnection(BaseConnection[Employee]):
    class Meta:
        """`Connection` 类型的元数据类, 设定 node 的类型"""

        node = Employee


class EmployeeQuery(ObjectType):
    employee: Employee = Field(
        Employee,
        args={
            "name": String(required=True),
        },
    )

    employees: ListType[Employee] = ConnectionField(
        EmployeeConnection,
        args={
            "department_name": String(required=True),
        },
    )

    @staticmethod
    def resolve_employee(
        parent: Literal[None], info: ResolveInfo, name: str
    ) -> EmployeeModel:
        return cast(EmployeeModel, EmployeeModel.objects(name=name).first())

    @staticmethod
    def resolve_employees(
        parent: Literal[None], info: ResolveInfo, **kwargs: Any
    ) -> EmployeeConnection:
        department_name: Optional[str] = kwargs.get("department_name")
        if not department_name:
            raise QueryError("invalid_department_name")

        page_size: int = max(cast(int, kwargs.get("first", 0)), 0)
        if page_size == 0:
            raise QueryError("invalid_first_argument")

        after: str = kwargs.get("after", "")
        if after:
            start = int(parse_cursor(after))
        else:
            start = 0

        department: Department = DepartmentModel.objects(name=department_name).first()

        total_count: int = EmployeeModel.objects(department=department).count()
        employees: ListType[EmployeeModel] = list(
            EmployeeModel.objects(department=department).limit(page_size).skip(start)
        )

        page_size = len(employees)
        result = QueryResult(employees, start, start + page_size, total_count)

        return EmployeeConnection(result)
