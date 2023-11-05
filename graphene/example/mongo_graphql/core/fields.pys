from copy import deepcopy
from typing import (Optional, Type, Any, Union)

from bson import (ObjectId, DBRef)
from mongoengine import Document
from mongoengine.base import LazyReference, BaseField
from mongoengine.fields import LazyReferenceField, StringField


class ProxyLazyReference(LazyReference):
    __slots__ = ("_document_type", "_cached_doc", "_pk")

    # noinspection PyMissingConstructor
    def __init__(self, document_type: Type, pk: ObjectId, doc: Optional[Document] = None) -> None:
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
        # noinspection PyProtectedMember
        return self._document_type._get_collection_name()

    @property
    def database(self) -> Any:
        return None

    @property
    def document_type(self) -> Type[Document]:
        return self._document_type

    @property
    def passthrough(self) -> bool:
        return True

    def __getitem__(self, name) -> Any:
        doc: Document = self.fetch()
        return doc[name]

    def __getattr__(self, name) -> Any:
        return getattr(self.fetch(), name)

    def __setattr__(self, name, value) -> None:
        doc: Document = self.fetch()
        doc[name] = value

    def __repr__(self) -> str:
        return f"<ProxyLazyReference doc_cls={self.document_type.__name__} id={self._pk}>"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DBRef):
            return self.collection == other.collection and self._pk == other.id
        elif self._document_type == type(other):
            return self._pk == other.id  # type: ignore
        else:
            return False

    def __hash__(self) -> int:
        return hash(self._pk)

    def __deepcopy__(self, memo) -> DBRef:
        """Support function for `copy.deepcopy()`."""
        # noinspection PyArgumentList
        return DBRef(
            deepcopy(self.collection, memo),
            deepcopy(self.id, memo),
            deepcopy(self.database, memo),
            deepcopy({}, memo),
        )

    @staticmethod
    def create(doc_cls: Type, pk: ObjectId) -> "ProxyLazyReference":
        return ProxyLazyReference(doc_cls, pk)


LazyRefValueType = Union[ProxyLazyReference, LazyReference, Document, DBRef, ObjectId]


class ProxyLazyReferenceField(LazyReferenceField):
    def __init__(self, document_type, passthrough=True, **kwargs: Any) -> None:
        super().__init__(document_type, passthrough, **kwargs)

    def build_lazyref(self, value: LazyRefValueType) -> ProxyLazyReference:
        if value is None or isinstance(value, ProxyLazyReference):
            return value

        if isinstance(value, LazyReference):
            return ProxyLazyReference(value.document_type, value.pk)
        elif isinstance(value, self.document_type):
            return ProxyLazyReference(self.document_type, value.pk, value)
        elif isinstance(value, DBRef):
            return ProxyLazyReference(self.document_type, value.id)
        else:
            # value is the primary key of the referenced document
            return ProxyLazyReference(self.document_type, value)


class EnumField(BaseField):
    def __init__(self, enum, *args, **kwargs) -> None:
        self.enum = enum
        super().__init__(*args, **kwargs)

    @staticmethod
    def _get_value(enum) -> Any:
        return enum.value if hasattr(enum, "value") else enum

    def to_python(self, value) -> Any:
        return self.enum(super().to_python(value))

    def to_mongo(self, value) -> Any:
        return self._get_value(value)

    def prepare_query_value(self, op, value):
        return super().prepare_query_value(op, self._get_value(value))

    def validate(self, value, clean=True):
        return super().validate(self._get_value(value))

    def _validate(self, value, **kwargs):
        return super()._validate(self.enum(self._get_value(value)), **kwargs)


class StringEnumField(EnumField, StringField):
    # pylint: disable=useless-super-delegation
    def __set__(self, instance, value: Any) -> None:
        super().__set__(instance, value)
