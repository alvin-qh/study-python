from datetime import datetime
from typing import Any, Union

from peewee import (
    Model,
    BigAutoField,
    DateTimeField,
    ModelUpdate,
    BigIntegerField,
    CharField,
    ModelSelect,
    IntegerField, ForeignKeyField, DeferredForeignKey
)

from .core.context import context
from .core.db import db


class BaseModel(Model):
    class Meta:
        database = db

    id = BigAutoField(primary_key=True)


class AuditAtMixin(Model):
    created_at = DateTimeField()
    updated_at = DateTimeField()

    def save(self, force_insert: bool = False, only: Any = None) -> Union[bool, int]:
        if not self.created_at:
            self.created_at = datetime.utcnow()

        self.updated_at = datetime.utcnow()
        return super().save(force_insert, only)

    @classmethod
    def create(cls, **query: Any) -> Model:
        query.update(created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        return super().create(**query)

    @classmethod
    def update(cls, __data=None, **update) -> ModelUpdate:
        update.update(updated_at=datetime.utcnow())
        return super().update(__data, **update)


class MultiTenantMixin(Model):
    org_id = BigIntegerField(null=False)

    @classmethod
    def select(cls, *fields: str) -> ModelSelect:
        select = super().select(*fields)
        org = context.get_current_org()
        if org:
            select = select.where(cls.org_id == org.id)

        return select

    def save(self, force_insert: bool = False, only: Any = None) -> Union[bool, int]:
        org = context.get_current_org()
        if org:
            self.org_id = org.id

        return super().save(force_insert, only)

    @classmethod
    def create(cls, **query: Any) -> Model:
        org = context.get_current_org()
        if org:
            query.update(org_id=org.id)

        return super().create(**query)

    @classmethod
    def update(cls, __data=None, **update) -> ModelUpdate:
        update = super().update(__data, **update)
        org = context.get_current_org()
        if org:
            update = update.where(cls.org_id == org.id)

        return update

    @classmethod
    def delete(cls):
        delete = super().delete()
        org = context.get_current_org()
        if org:
            delete = delete.where(org_id=org.id)

        return delete


class AuditByMixin(Model):
    created_by = BigIntegerField()
    updated_by = BigIntegerField()

    def save(self, force_insert: bool = False, only: Any = None) -> Union[bool, int]:
        user: Employee = context.get_current_user()
        if user:
            self.created_by = user.id
            self.updated_by = user.id

        return super().save(force_insert, only)

    @classmethod
    def create(cls, **query: Any) -> Model:
        user: Employee = context.get_current_user()
        if user:
            query.update(created_by=user.id, updated_by=user.id)

        return super().create(**query)

    @classmethod
    def update(cls, __data=None, **update) -> ModelUpdate:
        user: Employee = context.get_current_user()
        if user:
            update.update(updated_by=user.id)
        return super().update(__data, **update)


class Org(BaseModel, AuditAtMixin):
    class Meta:
        table_name = "gql_org"

    name = CharField(null=False)


class Department(BaseModel, AuditAtMixin, AuditByMixin, MultiTenantMixin):
    class Meta:
        table_name = "gql_department"

    name = CharField(null=False)
    level = IntegerField(null=False, default=0)
    manager = DeferredForeignKey(
        "Employee",
        object_id_name="manager_id",
        field="id",
        lazy_load=True
    )


class Role(BaseModel, AuditAtMixin, MultiTenantMixin):
    class Meta:
        table_name = "gql_role"

    name = CharField(null=False)


class Employee(BaseModel, AuditAtMixin, AuditByMixin, MultiTenantMixin):
    class Meta:
        table_name = "gql_employee"

    name = CharField(null=False)
    gender = CharField(max_length=1, null=False, default="M")
    department = ForeignKeyField(
        Department,
        object_id_name="department_id",
        field="id",
        backref="employees"
    )
    role = ForeignKeyField(
        Role,
        object_id_name="role_id",
        field="id"
    )
