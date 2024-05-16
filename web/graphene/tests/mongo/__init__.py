from typing import Generator

import pytest
from mongo import OrgModel, clear_db, context, ensure_indexes, schema

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

        # 清空数据库
        clear_db()
        # 重建文档索引
        ensure_indexes()

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
