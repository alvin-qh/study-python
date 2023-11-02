from enum import Enum
from typing import Any, Dict, Optional

from mongoengine.fields import IntField, ReferenceField, StringField

from .core import (
    AbstractOrg,
    AuditedMixin,
    BaseModel,
    MultiTenantMixin,
    ProxyLazyReferenceField,
    StringEnumField,
)


class Org(BaseModel, AuditedMixin, AbstractOrg):
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

    name: str = StringField(required=True)
    level: int = IntField(required=True, default=0)
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

    name: str = StringField(required=True)
    gender: Gender = StringEnumField(Gender, required=True, default=Gender.male)
    department: Optional[Department] = ProxyLazyReferenceField(Department)
    role: Optional[Role] = ProxyLazyReferenceField(Role)

    def set_department(
        self, department: Department, role: Optional[Role] = None
    ) -> "Employee":
        self.department = department
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
        department = self.department

        self.department = None
        self.role = None
        self.save()

        if department and department.manager == self:
            department.manager = None
            department.save()
