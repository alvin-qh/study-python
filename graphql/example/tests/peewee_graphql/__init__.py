from typing import Callable

import pytest
from graphene.test import Client

from peewee_graphql.core.context import context, run_once
from peewee_graphql.core.db import db
from peewee_graphql.models import (
    Org,
    Employee,
    Role
)
from peewee_graphql.schemas import schema
from tests.peewee_graphql.factories import (
    OrgFactory,
    RoleFactory,
    EmployeeFactory,
    DepartmentFactory
)


class BaseTest:
    client: Client
    current_org: Org
    role_member: Role
    role_manager: Role
    login_user: Employee

    def setup_method(self, method: Callable):
        self.client = Client(schema=schema)

    @classmethod
    def setup_class(cls):
        cls._clear_db()

        cls.current_org = OrgFactory.create()

        cls._setup_roles()
        cls._setup_login_user()

    @classmethod
    @run_once
    def _clear_db(cls):
        assert db.database == "study_python"

        with db.transaction():
            for table in db.get_tables():
                if table != "alembic_version":
                    db.execute_sql(f"alter table {table} disable trigger all")
                    db.execute_sql(f"truncate table {table} restart identity cascade")
                    db.execute_sql(f"alter table {table} enable trigger all")

    @classmethod
    def _setup_roles(cls):
        with context.with_tenant_context(cls.current_org):
            cls.role_manager = RoleFactory.create(name="manager")
            cls.role_member = RoleFactory.create(name="member")

    @classmethod
    def _setup_login_user(cls):
        with context.with_tenant_context(cls.current_org):
            root_department = DepartmentFactory.create(level=0)
            cls.login_user = EmployeeFactory.create(
                department=root_department,
                role=cls.role_manager
            )
            root_department.manager = cls.login_user
            root_department.save()

    @pytest.fixture(scope="class", autouse=True)
    def org_context(self):
        with context.with_tenant_context(self.current_org):
            with context.with_login_user(self.login_user):
                yield
