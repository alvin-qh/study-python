from typing import Callable

import pytest
from graphene.test import Client
from mongoengine import get_db

from mongo_graphql.core.context import run_once, context
from mongo_graphql.models import Org
from mongo_graphql.schemas import schema
from tests.mongo_graphql.factories import OrgFactory, RoleFactory


class BaseTest:
    client: Client
    current_org: Org

    def setup_method(self, method: Callable):
        self.client = Client(schema=schema)

    @classmethod
    def setup_class(cls):
        cls._clear_db()
        cls._ensure_indexes()

        cls.current_org = OrgFactory.create()
        cls._setup_roles()

    @classmethod
    @run_once
    def _clear_db(cls):
        db = get_db("default")
        for coll in db.list_collection_names():
            db[coll].drop()

    @classmethod
    @run_once
    def _ensure_indexes(cls):
        db = get_db("default")
        for coll in db.list_collection_names():
            db[coll].ensure_indexes()

    @classmethod
    def _setup_roles(cls):
        with context.with_tenant_context(cls.current_org):
            RoleFactory.create(name="manager")
            RoleFactory.create(name="member")

    @pytest.fixture(scope="class", autouse=True)
    def org_context(self):
        with context.with_tenant_context(self.current_org):
            yield
