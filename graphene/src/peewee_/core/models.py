from datetime import datetime
from typing import Any, List, Optional, cast

from peewee import (
    BigAutoField,
    BigIntegerField,
    DateTimeField,
    Field,
    Model,
    ModelDelete,
    ModelSelect,
    ModelUpdate,
)

from .context import context
from .db import pg_db


class BaseModel(Model):
    """模型超类, 其它模型类都必须从该类继承"""

    class Meta:
        """模型元数据"""

        database = pg_db  # 定义数据库连接

    # 定义主键字段
    id = BigAutoField(primary_key=True)


class AuditByMixin(Model):
    # 记录创建人字段
    created_by: int = BigIntegerField(null=True)

    # 记录更新人字段
    updated_by: int = BigIntegerField(null=True)

    def save(self, force_insert: bool = False, only: Any = None) -> int:
        """将当前模型对象作为记录插入数据表

        Args:
            - `force_insert` (`bool`, optional): 是否执行强制 `insert` 操作. Defaults to `False`.
            - `only` (`Optional[List[Field]]`, optional): 本次存储指定的字段集合. Defaults to `None`.

        Returns:
            `int`: 操作影响的数据表行数
        """
        user = context.get_current_user()
        if user:
            self.created_by = user._get_id()
            self.updated_by = user._get_id()

        return cast(int, super().save(force_insert, only))

    @classmethod
    def create(cls, **query: Any) -> Model:
        """插入一条新纪录并返回模型对象

        Args:
            - `query` (`Dict[str, Any]`, optional): 要创建的数据字段和值

        Returns:
            `Model`: 表示插入记录的模型对象
        """
        user = context.get_current_user()
        if user:
            query.update(created_by=user._get_id(), updated_by=user._get_id())

        return super().create(**query)

    @classmethod
    def update(cls, __data: Optional[Any] = None, **update: Any) -> ModelUpdate:
        """创建一个 `update` 查询对象

        Args:
            - `__data` (`Optional[Any]`, optional): 字典对象, 表示要更新的字段和值. Defaults to `None`.
            - `update` (`Dict[str, Any]`): 表示要更新的字段名称和值

        Returns:
            `ModelUpdate`: `update` 查询对象
        """
        user = context.get_current_user()
        if user:
            update.update(updated_by=user._get_id())

        return cast(ModelUpdate, super().update(__data, **update))


class AuditAtMixin(Model):
    """审计附件类型, 为目标模型加入审计字段"""

    # 记录创建时间
    created_at: datetime = DateTimeField()

    # 记录更新时间
    updated_at: datetime = DateTimeField()

    def save(
        self, force_insert: bool = False, only: Optional[List[Field]] = None
    ) -> int:
        """将当前模型对象作为记录插入数据表

        Args:
            - `force_insert` (`bool`, optional): 是否执行强制 `insert` 操作. Defaults to `False`.
            - `only` (`Optional[List[Field]]`, optional): 本次存储指定的字段集合. Defaults to `None`.

        Returns:
            `int`: 操作影响的数据表行数
        """
        if not self.created_at:
            # 设置记录的创建时间
            self.created_at = datetime.utcnow()

        # 设置记录的更新时间
        self.updated_at = datetime.utcnow()
        return cast(int, super().save(force_insert, only))

    @classmethod
    def create(cls, **query: Any) -> Model:
        """插入一条新纪录并返回模型对象

        Args:
            - `query` (`Dict[str, Any]`, optional): 要创建的数据字段和值

        Returns:
            `Model`: 表示插入记录的模型对象
        """
        # 设置记录的审计时间字段
        query.update(created_at=datetime.utcnow(), updated_at=datetime.utcnow())

        # 创建记录并返回模型对象
        return cast(Model, super().create(**query))

    @classmethod
    def update(cls, __data: Optional[Any] = None, **update: Any) -> ModelUpdate:
        """创建一个 `update` 查询对象

        Args:
            - `__data` (`Optional[Any]`, optional): 字典对象, 表示要更新的字段和值. Defaults to `None`.
            - `update` (`Dict[str, Any]`): 表示要更新的字段名称和值

        Returns:
            `ModelUpdate`: `update` 查询对象
        """
        # 在更新数据中加入 `updated_at` 字段值
        update.update(updated_at=datetime.utcnow())
        return cast(ModelUpdate, super().update(__data, **update))


class MultiTenantMixin(Model):
    """多租户附加类型, 为目标类型引入多租户字段"""

    # 租户 id 字段
    org_id: int = BigIntegerField()

    @classmethod
    def select(cls, *fields: str) -> ModelSelect:
        """创建一个 `select` 查询对象

        Args:
            - `fields` (`Tuple[str]`): 要查询的字段名称

        Returns:
            `ModelSelect`: `select` 查询对象
        """
        # 获取查询对象
        select: ModelSelect = super().select(*fields)

        # 在查询对象中加入租户查询条件
        tenant = context.get_current_tenant()
        if tenant:
            select = select.where(cls.org_id == tenant._get_id())

        return select

    def save(self, force_insert: bool = False, only: Any = None) -> int:
        """将当前模型对象作为记录插入数据表

        Args:
            - `force_insert` (`bool`, optional): 是否执行强制 `insert` 操作. Defaults to `False`.
            - `only` (`Optional[List[Field]]`, optional): 本次存储指定的字段集合. Defaults to `None`.

        Returns:
            `int`: 操作影响的数据表行数
        """
        # 获取上下文租户对象
        tenant = context.get_current_tenant()
        if tenant:
            # 为查询加入租户 id 值
            self.org_id = tenant._get_id()

        return cast(int, super().save(force_insert, only))

    @classmethod
    def create(cls, **query: Any) -> Model:
        """创建实体时, 加入租户信息

        Returns:
            Model: 被创建的实体对象
        """
        # 获取上下文租户对象
        tenant = context.get_current_tenant()
        if tenant:
            # 为查询加入租户 id 值
            query.update(org_id=tenant._get_id())

        # 创建实体
        return cast(Model, super().create(**query))

    @classmethod
    def update(cls, __data: Optional[Any] = None, **update: Any) -> ModelUpdate:
        """更新实体时, 加入租户筛选条件

        Args:
            - `__data` (`Optional[Any]`, optional): 字典对象, 表示要更新的字段和值. Defaults to `None`.
            - `update` (`Dict[str, Any]`): 表示要更新的字段名称和值

        Returns:
            `ModelUpdate`: `update` 查询对象
        """
        query: ModelUpdate = super().update(__data, **update)

        org = context.get_current_tenant()
        if org:
            query = query.where(cls.org_id == org._get_id())

        return query

    @classmethod
    def delete(cls) -> ModelDelete:
        """为删除语句加入租户筛选条件

        Returns:
            `ModelDelete`: `delete` 查询对象
        """
        query: ModelDelete = super().delete()

        tenant = context.get_current_tenant()
        if tenant:
            query = query.where(org_id=tenant._get_id())

        return query
