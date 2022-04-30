from enum import Enum
from typing import Optional

from mongoengine.fields import (StringField, IntField)

from .core.fields import ProxyLazyReferenceField, StringEnumField
from .core.models import BaseModel, MultiTenantMixin, AuditedMixin


class Org(BaseModel, AuditedMixin):
    meta = {
        "indexes": [
            {
                "fields": ["name"],
                "unique": True,
                "partialFilterExpression": {
                    "name": {
                        "$type": "string"
                    }
                }
            }
        ]
    }

    name: str = StringField(reqired=True)


class Department(BaseModel, MultiTenantMixin, AuditedMixin):
    meta = {
        "indexes": [
            {
                "fields": ["org", "name"],
                "unique": True
            }
        ]
    }

    name: str = StringField(required=True)
    level: int = IntField(required=True, default=0)
    manager: "Employee" = ProxyLazyReferenceField("Employee")


class Role(BaseModel, MultiTenantMixin):
    meta = {
        "indexes": [
            {
                "fields": ["org", "name"],
                "unique": True
            }
        ]
    }

    name: str = StringField(required=True)


class Gender(Enum):
    male = "male"
    female = "female"


class Employee(BaseModel, MultiTenantMixin, AuditedMixin):
    meta = {
        "indexes": [
            {
                "fields": ["org", "name"],
                "unique": True
            }
        ]
    }

    name: str = StringField(required=True)
    gender: Gender = StringEnumField(Gender, required=True, default=Gender.male)
    department: Optional[Department] = ProxyLazyReferenceField(Department)
    role: Optional[Role] = ProxyLazyReferenceField(Role)

    def set_department(self, department: Department, role: Optional[Role] = None) -> "Employee":
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

    def leave_department(self):
        department = self.department

        self.department = None
        self.role = None
        self.save()

        if department.manager == self:
            department.manager = None
            department.save()
