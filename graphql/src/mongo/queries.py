from typing import Any, List, Type, cast

from graphene import Field, ObjectType, ResolveInfo, String
from graphene_mongo import MongoengineConnectionField
from mongoengine import QuerySet

from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .types import Department, Employee, QueryError


class DepartmentQuery(ObjectType):
    department: Department = Field(Department, args={"name": String(required=True)})

    @staticmethod
    def resolve_department(
        parent: Department, info: ResolveInfo, name: str
    ) -> DepartmentModel:
        return cast(DepartmentModel, DepartmentModel.objects(name=name).first())


def _query_employees_by_department_name(
    model: Type[EmployeeModel], info: ResolveInfo, **kwargs: Any
) -> QuerySet:
    department_name = kwargs.get("department_name")
    department = DepartmentModel.objects(name=department_name).first()

    if not department:
        raise QueryError("invalid_department_name")

    return EmployeeModel.objects(department=department)


class EmployeeQuery(ObjectType):
    employee: Employee = Field(Employee, args={"name": String(required=True)})

    employees: List[Employee] = MongoengineConnectionField(
        Employee,
        args={"department_name": String(required=True)},
        get_queryset=_query_employees_by_department_name,
    )

    @staticmethod
    def resolve_employee(
        parent: Employee, info: ResolveInfo, name: str
    ) -> EmployeeModel:
        return cast(EmployeeModel, EmployeeModel.objects(name=name).first())