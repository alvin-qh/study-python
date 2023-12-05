from typing import Generator

import pytest
from peewee_ import OrgModel, context, initialize_tables, pg_db, schema

from graphene.test import Client

from .factories import OrgModelFactory, RoleModelFactory


class BaseTest:
    """测试超类"""

    # graphene 测试客户端
    client: Client

    # 当前组织
    current_org: OrgModel

    @classmethod
    def setup_class(cls) -> None:
        """测试初始化"""

        # 初始化数据表
        initialize_tables()

        with pg_db.atomic():
            # 创建当前组织
            cls.current_org = OrgModelFactory.create()

            # 创建角色
            cls._setup_roles()

    def setup_method(self) -> None:
        """在每次测试前执行"""

        # 创建 graphene 测试客户端
        self.client = Client(schema=schema)

    @classmethod
    def _setup_roles(cls) -> None:
        """创建角色"""
        with context.with_tenant_context(cls.current_org):
            RoleModelFactory.create(name="manager")
            RoleModelFactory.create(name="member")

    @pytest.fixture(scope="class", autouse=True)
    def build_test_context(self) -> Generator[None, None, None]:
        """创建测试上下文"""
        with context.with_tenant_context(self.current_org):
            yield
