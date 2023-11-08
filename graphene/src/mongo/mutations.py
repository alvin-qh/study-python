from typing import Any, Literal, Optional

from graphene import (
    ID,
    ClientIDMutation,
    Field,
    InputObjectType,
    Int,
    Mutation,
    ObjectType,
    ResolveInfo,
    String,
)

from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .models import Role as RoleModel
from .types import Department, Employee, Gender


class CreateDepartmentInput(InputObjectType):
    name = String(required=True)
    level = Int(required=True)


class CreateDepartmentPayload(ObjectType):
    id: str = String(required=True)
    name: str = String(required=True)


class CreateDepartment(Mutation):
    class Input:
        name = String(required=True)
        level = Int(required=True)

    department = Field(Department)

    @staticmethod
    def mutate_and_get_payload(
        root: Literal[None],
        info: ResolveInfo,
        **input: Any,
    ) -> "CreateDepartment":
        department = DepartmentModel(name=input["name"], level=input["level"]).save()
        return CreateDepartment(department=department)


class CreateEmployeeInput(InputObjectType):
    name: str = String(required=True)
    gender: Gender = Field(Gender, required=True)
    department_id: str = ID()
    role: str = String()


class CreateEmployee(ClientIDMutation):
    class Input:
        input = CreateEmployeeInput()

    employee = Field(Employee)

    @staticmethod
    def mutate_and_get_payload(
        root: Literal[None],
        info: ResolveInfo,
        input: CreateEmployeeInput,
    ) -> "CreateEmployee":
        department: Optional[Department] = None
        if input.department_id:
            department = DepartmentModel.objects(id=input.department_id).first()
            if not department:
                raise ValueError("invalid_department")

        if input.role:
            role = RoleModel.objects(name=input.role).first()
            if not role:
                role = RoleModel(name=input.role).save()
        else:
            role = None

        employee = EmployeeModel(
            name=input.name,
            gender=input.gender,
            department=department,
            role=role,
        ).save()

        if role and role.name == "manager":
            if department:
                department.manager = employee
                department.save()

        return CreateEmployee(employee=employee)


class DepartmentMutation(ObjectType):
    create_department = CreateDepartment.Field()


class EmployeeMutation(ObjectType):
    create_employee = CreateEmployee.Field()
