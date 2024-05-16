from enum import Enum
from typing import Any, Dict, Optional

from mongoengine.fields import IntField, ReferenceField, StringField

from .core import (
    AuditedMixin,
    BaseModel,
    MultiTenantMixin,
    ProxyLazyReferenceField,
    StringEnumField,
    Tenant,
)


class Org(Tenant, BaseModel, AuditedMixin):
    """租户文档模型"""

    meta: Dict[str, Any] = {
        "indexes": [
            {
                "fields": ["name"],
                "unique": True,
                "partialFilterExpression": {
                    "name": {
                        "$type": "string",
                    },
                },
            }
        ]
    }

    name: str = StringField(required=True)


class Department(BaseModel, MultiTenantMixin, AuditedMixin):
    """部门文档模型"""

    meta: Dict[str, Any] = {
        "indexes": [
            {
                "fields": [
                    "org",
                    "name",
                ],
                "unique": True,
            }
        ]
    }

    # 部门名称属性
    name: str = StringField(required=True)

    # 部门等级属性
    level: int = IntField(required=True, default=0)

    # 部门管理人员属性
    manager: Optional["Employee"] = ReferenceField("Employee")


class Role(BaseModel, MultiTenantMixin):
    meta: Dict[str, Any] = {
        "indexes": [
            {
                "fields": [
                    "org",
                    "name",
                ],
                "unique": True,
            }
        ]
    }

    # 角色名称属性
    name: str = StringField(required=True)


class Gender(Enum):
    male = "male"
    female = "female"


class Employee(BaseModel, MultiTenantMixin, AuditedMixin):
    meta: Dict[str, Any] = {
        "indexes": [
            {
                "fields": [
                    "org",
                    "name",
                ],
                "unique": True,
            }
        ]
    }

    # 员工姓名属性
    name: str = StringField(required=True)

    # 员工性别属性
    gender: Gender = StringEnumField(Gender, required=True, default=Gender.male)

    # 员工所属部门属性
    department: Optional[Department] = ProxyLazyReferenceField(Department)

    # 员工权限属性
    role: Optional[Role] = ProxyLazyReferenceField(Role)

    def set_department(
        self, department: Department, role: Optional[Role] = None
    ) -> "Employee":
        """设置当前员工所属的部门

        Args:
            - `department` (`Department`): 部门文档对象
            - `role` (`Optional[Role]`, optional): 权限对象, 表示当前员工在目标部门的权限. Defaults to `None`.

        Returns:
            `Employee`: 当前员工对象
        """
        # 设置部门对象
        self.department = department
        # 获取当前
        if role is None:
            role = self.role
        else:
            self.role = role

        self.save()

        if role and role.name == "manager" and department.manager != self:
            department.manager = self
            department.save()

        return self

    def leave_department(self) -> None:
        """当前员工离开当前部门"""
        department = self.department

        # 取消当员工的部门
        self.department = None
        self.role = None
        self.save()

        # 如果当前员工同时是部门的管理员, 则取消该部门管理员
        if department and department.manager == self:
            department.manager = None
            department.save()
