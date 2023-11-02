from typing import Any, Optional

from graphene import (
    ID,
    ClientIDMutation,
    Enum,
    Field,
    GlobalID,
    InputObjectType,
    Int,
    ObjectType,
    ResolveInfo,
    String,
)
from graphql_relay import from_global_id

from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .models import Role as RoleModel
from .types import Department, Employee


class DepartmentInput(InputObjectType):
    name = String(required=True)
    level = Int(required=True)


class DepartmentMutation(ClientIDMutation):
    class Input:
        department_input = DepartmentInput(required=True)

    department = Field(Department)

    @classmethod
    def mutate_and_get_payload(
        cls,
        root: Any,
        info: ResolveInfo,
        department_input: DepartmentInput,
        client_mutation_id: Optional[ID] = None,
    ) -> "DepartmentMutation":
        department = DepartmentModel(
            name=department_input.name, level=department_input.level
        ).save()
        return cls(department=department)


class Gender(Enum):
    male = "male"
    female = "female"


class EmployeeInput(InputObjectType):
    name: str = String(required=True)
    gender: Gender = Field(Gender, required=True)
    department: str = GlobalID()
    role: str = String()


class EmployeeMutation(ClientIDMutation):
    class Input:
        employee_input = EmployeeInput()

    employee = Field(Employee)

    @classmethod
    def mutate_and_get_payload(
        cls,
        root: Any,
        info: ResolveInfo,
        employee_input: EmployeeInput,
        client_mutation_id: Optional[ID] = None,
    ) -> "EmployeeMutation":
        department: Optional[Department] = None
        if employee_input.department:
            department_type, department_id = from_global_id(employee_input.department)
            assert department_type == DepartmentModel.__name__

            department = DepartmentModel.objects(id=department_id).first()
            if not department:
                raise ValueError("invalid_department")

        if employee_input.role:
            role = RoleModel.objects(name=employee_input.role).first()
            if not role:
                role = RoleModel(name=employee_input.role).save()
        else:
            role = None

        employee = EmployeeModel(
            name=employee_input.name,
            gender=employee_input.gender,
            department=department,
            role=role,
        ).save()

        if role and role.name == "manager":
            if department:
                department.manager = employee
                department.save()

        return EmployeeMutation(employee=employee)


class Mutations(ObjectType):
    department_mutation = DepartmentMutation.Field()
    employee_mutation = EmployeeMutation.Field()
