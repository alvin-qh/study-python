from copy import deepcopy
from enum import Enum
from typing import Any, Dict, Mapping, Optional, Type, Union, cast

from bson import DBRef, ObjectId
from mongoengine import Document
from mongoengine.base import BaseField, LazyReference
from mongoengine.fields import LazyReferenceField, StringField


class ProxyLazyReference(LazyReference):
    __slots__ = ("_document_type", "_cached_doc", "_pk")

    _document_type: Type[Document]
    _pk: ObjectId
    _cached_doc: Document

    def __init__(
        self,
        document_type: Type[Document],
        pk: ObjectId,
        doc: Optional[Document] = None,
    ) -> None:
        object.__setattr__(self, "_document_type", document_type)
        object.__setattr__(self, "_pk", pk)
        object.__setattr__(self, "_cached_doc", doc)

    def fetch(self, force: bool = False) -> Document:
        doc = self._cached_doc
        if not doc:
            document_type = self._document_type
            doc = document_type.objects.get(id=self._pk)
            object.__setattr__(self, "_cached_doc", doc)
        return doc

    @property
    def id(self) -> ObjectId:
        return self._pk

    @property
    def collection(self) -> str:
        return str(self._document_type._get_collection_name())

    @property
    def database(self) -> Any:
        return None

    @property
    def document_type(self) -> Type[Document]:
        return self._document_type

    @property
    def passthrough(self) -> bool:
        return True

    def __getitem__(self, name: str) -> Any:
        doc: Document = self.fetch()
        return doc[name]

    def __getattr__(self, name: str) -> Any:
        return getattr(self.fetch(), name)

    def __setattr__(self, name: str, value: Any) -> None:
        doc: Document = self.fetch()
        doc[name] = value

    def __repr__(self) -> str:
        return (
            f"<ProxyLazyReference doc_cls={self.document_type.__name__} id={self._pk}>"
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DBRef):
            return self.collection == other.collection and self._pk == other.id
        elif isinstance(other, self._document_type):
            return self._pk == other.id  # type: ignore
        else:
            return False

    def __hash__(self) -> int:
        return hash(self._pk)

    def __deepcopy__(self, memo: Dict[int, Any]) -> DBRef:
        return DBRef(
            deepcopy(self.collection, memo),
            deepcopy(self.id, memo),
            deepcopy(self.database, memo),
            deepcopy(cast(Mapping[str, Any], {}), memo),
        )

    @staticmethod
    def create(doc_cls: Type[Document], pk: ObjectId) -> "ProxyLazyReference":
        return ProxyLazyReference(doc_cls, pk)


LazyRefValueType = Union[ProxyLazyReference, LazyReference, Document, DBRef, ObjectId]


class ProxyLazyReferenceField(LazyReferenceField):
    def __init__(
        self,
        document_type: Union[str, Type[Document]],
        passthrough: bool = True,
        **kwargs: Any,
    ) -> None:
        super().__init__(document_type, passthrough, **kwargs)

    def build_lazyref(self, value: LazyRefValueType) -> Optional[ProxyLazyReference]:
        if value is None or isinstance(value, ProxyLazyReference):
            return value

        if isinstance(value, LazyReference):
            return ProxyLazyReference(value.document_type, value.pk)
        elif isinstance(value, self.document_type):
            return ProxyLazyReference(self.document_type, value.pk, value)
        elif isinstance(value, DBRef):
            return ProxyLazyReference(self.document_type, value.id)
        else:
            return ProxyLazyReference(self.document_type, value)


class EnumField(BaseField):
    def __init__(self, enum: Type[Enum], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.enum = enum

    @staticmethod
    def _get_value(enum: Any) -> Any:
        return enum.value if hasattr(enum, "value") else enum

    def to_python(self, value: Any) -> Any:
        return self.enum(super().to_python(value))

    def to_mongo(self, value: Any) -> Any:
        return self._get_value(value)

    def prepare_query_value(self, op: Any, value: Any) -> Any:
        return super().prepare_query_value(op, self._get_value(value))

    def validate(self, value: Any, clean: bool = True) -> Any:
        return super().validate(self._get_value(value))

    def _validate(self, value: Any, **kwargs: Any) -> Any:
        return super()._validate(self.enum(self._get_value(value)), **kwargs)


class StringEnumField(EnumField, StringField):
    def __set__(self, instance: Any, value: Any) -> None:
        super().__set__(instance, value)
