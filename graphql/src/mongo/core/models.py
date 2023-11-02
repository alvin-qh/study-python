from datetime import datetime
from typing import Any, Type

from mongoengine import Document, Q, QuerySet, signals
from mongoengine.fields import DateTimeField
from pymongo.collection import Collection

from .context import context
from .fields import ProxyLazyReferenceField


class TenantAwareQuerySet(QuerySet):
    def __init__(self, doc: Type[Document], collection: Collection[Any]) -> None:
        super().__init__(doc, collection)

        q = Q()
        if issubclass(doc, MultiTenantMixin):
            q &= Q(org=context.get_current_org())

        self._query_obj = q


class BaseModel(Document):
    meta = {
        "allow_inheritance": True,
        "abstract": True,
        "strict": False,
        "index_cls": False,
        "auto_create_index": False,
    }

    def __str__(self) -> str:
        if hasattr(self, "name"):
            return "{}<id={} name={}>".format(type(self).__name__, self.id, self.name)
        else:
            return "{}<id={}>".format(type(self).__name__, self.id)


class AuditedMixin(Document):
    meta = {"allow_inheritance": True, "abstract": True, "strict": False}

    created_at: datetime = DateTimeField()
    updated_at: datetime = DateTimeField()


class MultiTenantMixin(Document):
    meta = {
        "allow_inheritance": True,
        "abstract": True,
        "strict": False,
        "queryset_class": TenantAwareQuerySet,
    }

    org = ProxyLazyReferenceField("Org", required=True)


def _set_document_audited(
    doc_cls: Type[Document], document: Document, *args: Any, **kwargs: Any
) -> None:
    if isinstance(document, AuditedMixin):
        if not document.created_at:
            document.created_at = datetime.utcnow()

        document.updated_at = datetime.utcnow()


def _set_document_tenant(
    doc_cls: Type[Document], document: Document, *args: Any, **kwargs: Any
) -> None:
    if isinstance(document, MultiTenantMixin):
        org = context.get_current_org()
        if org:
            document.org = org  # type: ignore


signals.pre_save.connect(_set_document_audited)
signals.pre_save.connect(_set_document_tenant)
