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
from peewee_ import pg_db

from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .models import Role as RoleModel
from .types import Department, Gender


class CreateDepartmentInput(InputObjectType):
    """创建部门的输入对象类型"""

    # 部门名称
    name = String(required=True)

    # 部门级别
    level = Int(required=True)


class CreateDepartmentPayload(ObjectType):
    """创建部门的返回对象类型"""

    # 部门 id
    id: str = ID(required=True)

    # 部门名称
    name: str = String(required=True)


class CreateDepartment(Mutation):
    """部门创建类型"""

    class Arguments:
        """定义创建部门的参数"""

        # 创建部门参数, 参数名为 `input`
        input = CreateDepartmentInput(required=True)

    # 定义返回值
    Output = CreateDepartmentPayload

    @staticmethod
    def mutate(
        root: Literal[None],
        info: ResolveInfo,
        input: CreateDepartmentInput,
    ) -> CreateDepartmentPayload:
        """执行部门实体创建操作

        Args:
            - `input` (`CreateDepartmentInput`): 输入参数

        Returns:
            `CreateDepartmentPayload`: 返回结果
        """
        with pg_db.atomic():
            # 创建部门实体对象并持久化
            department = DepartmentModel(
                name=input.name,
                level=input.level,
            )
            department.save()

        # 返回结果
        return CreateDepartmentPayload(
            department.id,
            department.name,
        )


class CreateEmployeePayload(ObjectType):
    """员工创建结果类型"""

    # 员工 id
    id: str = ID(required=True)

    # 员工姓名
    name: str = String(required=True)


class CreateEmployee(ClientIDMutation):
    """员工创建

    `ClientIDMutation` 表示一个同时进行写和读操作的类型, 即根据输入参数执行写操作后, 返回结果进行读操作
    """

    class Input:
        """输入参数类型"""

        # 员工姓名
        name: str = String(required=True)

        # 员工性别
        gender: Gender = Field(Gender, required=True)

        # 员工所属部门 id
        department_id: str = ID()

        # 员工角色名称
        role: str = String()

    Output = CreateEmployeePayload

    @staticmethod
    def mutate_and_get_payload(
        root: Literal[None],
        info: ResolveInfo,
        **input: Any,
    ) -> CreateEmployeePayload:
        """_summary_

        Args:
            root (Literal[None]): _description_
            info (ResolveInfo): _description_

        Raises:
            ValueError: _description_

        Returns:
            CreateEmployee: _description_
        """
        department: Optional[Department] = None
        with pg_db.atomic():
            if "department_id" in input:
                department = DepartmentModel.get(
                    DepartmentModel.id == int(input["department_id"])
                )
                if not department:
                    raise ValueError("invalid_department")

            role: Optional[RoleModel] = None
            if "role" in input:
                role = RoleModel.get_or_none(RoleModel.name == input["role"])
                if not role:
                    role = RoleModel(name=input["role"])
                    role.save()

            # 保存员工实体对象
            employee = EmployeeModel(
                name=input["name"],
                gender=input["gender"].value,
                department=department,
                role=role,
            )
            employee.save()

            if role and role.name == "manager":
                if department:
                    department.manager = employee
                    department.save()

        # 返回结果
        return CreateEmployeePayload(
            id=employee.id,
            name=employee.name,
        )


class DepartmentMutation(ObjectType):
    create_department = CreateDepartment.Field()


class EmployeeMutation(ObjectType):
    create_employee = CreateEmployee.Field()
