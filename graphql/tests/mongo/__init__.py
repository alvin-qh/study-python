from typing import Any, Generator

import pytest
from graphene.test import Client
from mongo.core.context import context, run_once
from mongo.models import Org
from mongo.schemas import schema
from mongoengine import get_db

from .helper.factories import OrgFactory, RoleFactory


class BaseTest:
    client: Client
    current_org: Org

    def setup_method(self) -> None:
        self.client = Client(schema=schema)

    @classmethod
    def setup_class(cls) -> None:
        cls._clear_db()
        cls._ensure_indexes()

        cls.current_org = OrgFactory.create()
        cls._setup_roles()

    @classmethod
    @run_once
    def _clear_db(cls) -> None:
        db = get_db("default")
        for coll in db.list_collection_names():
            db[coll].drop()

    @classmethod
    @run_once
    def _ensure_indexes(cls) -> None:
        db = get_db("default")
        for coll in db.list_collection_names():
            db[coll].ensure_indexes()

    @classmethod
    def _setup_roles(cls) -> None:
        with context.with_tenant_context(cls.current_org):
            RoleFactory.create(name="manager")
            RoleFactory.create(name="member")

    @pytest.fixture(scope="class", autouse=True)
    def org_context(self) -> Generator[None, Any, None]:
        with context.with_tenant_context(self.current_org):
            yield
