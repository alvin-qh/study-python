from enum import Enum
from typing import Any, Dict, Optional

from mongoengine.fields import IntField, LazyReferenceField, StringField

from .core import AuditedMixin, BaseModel, MultiTenantMixin, StringEnumField, Tenant


class Org(Tenant, BaseModel, AuditedMixin):
    """组织模型类"""

    # 定义模型元数据
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

    # 定义姓名字段
    name: str = StringField(required=True)


class Department(BaseModel, MultiTenantMixin, AuditedMixin):
    """定义部门模型类"""

    # 定义模型元数据
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

    # 定义名称字段
    name: str = StringField(required=True)

    # 定义级别字段
    level: int = IntField(required=True, default=0)

    # 定义部门负责人字段
    manager: Optional["Employee"] = LazyReferenceField("Employee")


class Role(BaseModel, MultiTenantMixin):
    """定义员工角色实体类"""

    # 定义模型元数据
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

    # 定义名称字段
    name: str = StringField(required=True)


class Gender(Enum):
    """定义性别枚举"""

    male = "male"
    female = "female"


class Employee(BaseModel, MultiTenantMixin, AuditedMixin):
    """定义员工实体模型类"""

    # 定义模型元数据
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

    # 定义名称字段
    name: str = StringField(required=True)

    # 定义性别字段
    gender: Gender = StringEnumField(Gender, required=True, default=Gender.male)

    # 定义员工所属部门字段
    department: Optional[Department] = LazyReferenceField(Department)

    # 定义角色字段
    role: Optional[Role] = LazyReferenceField(Role)

    def set_department(
        self, department: Department, role: Optional[Role] = None
    ) -> "Employee":
        """设置员工所属部门

        Args:
            - `department` (`Department`): 部门实体对象
            - `role` (`Optional[Role]`, optional): 员工在部门内的角色. Defaults to `None`.

        Returns:
            Employee: _description_
        """
        self.department = department
        if role is None:
            role = self.role
        else:
            self.role = role

        self.save()

        # 如果员工在部门的角色为 "manager", 则设置部门的负责人字段为当前用户对象
        if role and role.name == "manager" and department.manager != self:
            department.manager = self
            department.save()

        return self

    def leave_department(self) -> None:
        """当前用户退出当前部门"""
        department = self.department

        # 设置员工的部门和角色为空, 表示员工不属于任何部门
        self.department = None
        self.role = None
        self.save()

        # 如果当前用户是部门的管理员, 则取消部门的管理员
        if department and department.manager == self:
            department.manager = None
            department.save()
