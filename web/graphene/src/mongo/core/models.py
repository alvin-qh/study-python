from datetime import datetime, UTC
from typing import Any, Type

from mongoengine import Document, Q, QuerySet, signals
from mongoengine.fields import DateTimeField, LazyReferenceField
from pymongo.collection import Collection

from .context import context


class TenantAwareQuerySet(QuerySet):
    """定义支持多租户的查询集合类型"""

    def __init__(self, doc: Type[Document], collection: Collection[Any]) -> None:
        super().__init__(doc, collection)

        q = Q()

        # 加入租户查询条件
        if issubclass(doc, MultiTenantMixin):
            q &= Q(org=context.get_current_tenant())

        self._query_obj = q


class BaseModel(Document):
    """定义所有文档模型的超类"""

    meta = {
        "allow_inheritance": True,  # 允许继承
        "abstract": True,  # 抽象类型
        "strict": False,  # 非严格模式
        "index_cls": False,  # 无索引类型
        "auto_create_index": False,  # 不会自动创建索引
    }

    def __str__(self) -> str:
        if hasattr(self, "name"):
            return "{}<id={} name={}>".format(type(self).__name__, self.id, self.name)
        else:
            return "{}<id={}>".format(type(self).__name__, self.id)


class AuditedMixin(Document):
    """定义文档审计功能的混入类型"""

    meta = {
        "allow_inheritance": True,
        "abstract": True,
        "strict": False,
    }

    # 为文档引入审计属性
    created_at: datetime = DateTimeField()
    updated_at: datetime = DateTimeField()


class MultiTenantMixin(Document):
    """定义文档多租户的混入类型"""

    meta = {
        "allow_inheritance": True,
        "abstract": True,
        "strict": False,
        "queryset_class": TenantAwareQuerySet,
    }

    # 定义租户属性
    org = LazyReferenceField("Org", required=True)


def _set_document_audited(
    doc_cls: Type[Document],
    document: Document,
    *args: Any,
    **kwargs: Any,
) -> None:
    """在文档更新前, 为文档加入审计属性

    Args:
        - `doc_cls` (`Type[Document]`): 文档类型
        - `document` (`Document`): 文档对象
    """
    if isinstance(document, AuditedMixin):
        if not document.created_at:
            document.created_at = datetime.now(UTC)

        document.updated_at = datetime.now(UTC)


def _set_document_tenant(
    doc_cls: Type[Document],
    document: Document,
    *args: Any,
    **kwargs: Any,
) -> None:
    """为文档加入租户属性

    Args:
        - `doc_cls` (`Type[Document]`): 文档类型
        - `document` (`Document`): 文档对象
    """
    if isinstance(document, MultiTenantMixin):
        org = context.get_current_tenant()
        if org:
            document.org = org


# 监听 mongoengine 的事件信号
signals.pre_save.connect(_set_document_audited)
signals.pre_save.connect(_set_document_tenant)
