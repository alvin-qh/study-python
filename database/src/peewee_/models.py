from enum import Enum
from typing import cast

from peewee import CharField, DeferredForeignKey, ForeignKeyField, IntegerField
from peewee_.core import (
    AuditAtMixin,
    AuditByMixin,
    BaseModel,
    MultiTenantMixin,
    Tenant,
    User,
)


class Org(Tenant, BaseModel, AuditAtMixin):
    """组织实体类型"""

    class Meta:
        # 定义组织表名称
        table_name = "org"

    # 组织名称字段
    name: str = cast(str, CharField(null=False))

    def _get_id(self) -> int:
        """实现 `Tenant` 类的方法, 获取当前实体 id

        Returns:
            int: 当前实体 id
        """
        return self.id


class Department(BaseModel, AuditAtMixin, AuditByMixin, MultiTenantMixin):
    """部门实体类型"""

    class Meta:
        # 定义部门表名称
        table_name = "department"

    # 部门名称字段
    name: str = cast(str, CharField(null=False))

    # 部门等级字段
    level: int = cast(int, IntegerField(null=False, default=0))

    # 部门管理人引用, 通过 `manager_id` 字段对应到 `Employee` 实体的 `id` 字段上, 可以为 `null`
    manager: "Employee" = cast(
        "Employee",
        DeferredForeignKey(
            "Employee",
            object_id_name="manager_id",
            field="id",
            lazy_load=True,
            null=True,
        ),
    )


class Role(BaseModel, AuditAtMixin, MultiTenantMixin):
    """角色实体类型"""

    class Meta:
        # 定义角色表名称
        table_name = "role"

    # 角色名称字段
    name: str = cast(str, CharField(null=False))


class Gender(Enum):
    """性别枚举"""

    MALE = "M"
    FEMALE = "F"


class Employee(User, BaseModel, AuditAtMixin, AuditByMixin, MultiTenantMixin):
    """员工实体类型"""

    class Meta:
        # 定义员工表名称
        table_name = "employee"

    # 员工姓名字段
    name: str = cast(str, CharField(null=False))

    # 员工性别字段
    gender: Gender = cast(Gender, CharField(max_length=1, null=False, default="M"))

    # 员工所属部门引用, 通过 `department_id` 字段对应到 `Department` 实体的 `id` 字段上, 并在
    # `Department` 实体中增加 `employees` 引用, 可以为 `null`
    department: Department = cast(
        Department,
        ForeignKeyField(
            Department,
            object_id_name="department_id",
            field="id",
            backref="employees",
            null=True,
        ),
    )

    # 角色引用, 通过 `role_id` 字段引用到 `Role` 实体的 `id` 字段上, 不能为 `null`
    role: Role = cast(Role, ForeignKeyField(Role, object_id_name="role_id", field="id"))

    def _get_id(self) -> int:
        """实现 `User` 类的方法, 获取当前实体 id

        Returns:
            int: 当前实体 id
        """
        return self.id
