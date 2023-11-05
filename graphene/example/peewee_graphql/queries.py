from typing import Any, List

from graphene import (
    ObjectType,
    Field,
    String,
    ResolveInfo
)
from graphene.relay import Connection, ConnectionField

from .models import (
    Department as DepartmentModel,
    Employee as EmployeeModel
)
from .types import (
    Department,
    Employee
)


class DepartmentQuery(ObjectType):
    department: Department = Field(Department, args={
        "name": String(required=True)
    })

    @staticmethod
    def resolve_department(parent: Any, info: ResolveInfo, name: str) -> DepartmentModel:
        return DepartmentModel.objects(name=name).first()


class EmployeeConnection(Connection):
    class Meta:
        node = Employee

class EmployeeQuery(ObjectType):
    employee: Employee = Field(Employee, args={
        "name": String(required=True)
    })

    employees: List[Employee] = ConnectionField(
        EmployeeConnection,
        args={
            "department_name": String(required=True)
        }
    )

    @staticmethod
    def resolve_employee(parent: Any, info: ResolveInfo, name: str) -> EmployeeModel:
        return EmployeeModel.objects(name=name).first()
