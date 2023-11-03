from copy import deepcopy
from enum import Enum
from typing import Any, Dict, Mapping, Optional, Type, Union, cast

from bson import DBRef, ObjectId
from mongoengine import Document, get_db
from mongoengine.base import BaseField, LazyReference
from mongoengine.fields import LazyReferenceField, StringField


class ProxyLazyReference(LazyReference):
    """代理模式懒加载引用类型"""

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
        # 通过 `object.__setattr__` 方法设置属性, 跳过 `self.__setattr__` 方法执行
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
        """获取文档 id

        Returns:
            ObjectId: 文档 id 值
        """
        return self._pk

    @property
    def collection(self) -> str:
        """获取文档集合名称

        Returns:
            str: 文档集合名称
        """
        return str(self._document_type._get_collection_name())

    @property
    def database(self) -> Any:
        """获取数据库对象

        Returns:
            Any: 数据库对象
        """
        return get_db()

    @property
    def document_type(self) -> Type[Document]:
        """获取文档类型

        Returns:
            Type[Document]: 文档类型
        """
        return self._document_type

    @property
    def passthrough(self) -> bool:
        """是否透传

        Returns:
            bool: 是否透传
        """
        return True

    def __getitem__(self, name: str) -> Any:
        """以下标形式获取属性值

        Args:
            name (str): 属性名称

        Returns:
            Any: 属性值
        """
        doc: Document = self.fetch()
        return doc[name]

    def __getattr__(self, name: str) -> Any:
        """获取属性值

        Args:
            name (str): 属性名称

        Returns:
            Any: 属性值
        """
        return getattr(self.fetch(), name)

    def __setattr__(self, name: str, value: Any) -> None:
        """设置属性值

        Args:
            name (str): 属性名称
            value (Any): 属性值
        """
        doc: Document = self.fetch()
        doc[name] = value

    def __repr__(self) -> str:
        """获取对象的字符串形式

        Returns:
            str: 对象的字符串形式值
        """
        return (
            f"<ProxyLazyReference doc_cls={self.document_type.__name__} id={self._pk}>"
        )

    def __eq__(self, other: object) -> bool:
        """对象比较

        Args:
            other (object): 待比较对象

        Returns:
            bool: 比较结果
        """
        if isinstance(other, DBRef):
            return self.collection == other.collection and self._pk == other.id
        elif isinstance(other, self._document_type):
            return self._pk == other.id  # type: ignore
        else:
            return False

    def __hash__(self) -> int:
        """计算对象的 Hash 值

        Returns:
            int: Hash 值
        """
        return hash(self._pk)

    def __deepcopy__(self, memo: Dict[int, Any]) -> DBRef:
        """复制当前对象

        Args:
            memo (Dict[int, Any]): 用于进行深度拷贝的"备忘录"对象

        Returns:
            DBRef: 引用对象
        """
        return DBRef(
            deepcopy(self.collection, memo),
            deepcopy(self.id, memo),
            deepcopy(self.database, memo),
            deepcopy(cast(Mapping[str, Any], {}), memo),
        )

    @staticmethod
    def create(doc_cls: Type[Document], pk: ObjectId) -> "ProxyLazyReference":
        """创建引用对象

        Args:
            doc_cls (Type[Document]): 文档类型
            pk (ObjectId): 文档 id

        Returns:
            ProxyLazyReference: 引用对象
        """
        return ProxyLazyReference(doc_cls, pk)


# 定义懒加载模式引用类型
LazyRefValueType = Union[ProxyLazyReference, LazyReference, Document, DBRef, ObjectId]


class ProxyLazyReferenceField(LazyReferenceField):
    """代理模式的懒加载引用字段类型"""

    def __init__(
        self,
        document_type: Union[str, Type[Document]],
        passthrough: bool = True,
        **kwargs: Any,
    ) -> None:
        super().__init__(document_type, passthrough, **kwargs)

    def build_lazyref(self, value: LazyRefValueType) -> Optional[ProxyLazyReference]:
        """构建一个懒加载代理模式引用对象

        Args:
            value (LazyRefValueType): 引用值

        Returns:
            Optional[ProxyLazyReference]: 代理模式引用对象
        """
        if value is None or isinstance(value, ProxyLazyReference):
            return value

        # 根据各种值类型产生代理引用对象
        if isinstance(value, LazyReference):
            return ProxyLazyReference(value.document_type, value.pk)
        elif isinstance(value, self.document_type):
            return ProxyLazyReference(self.document_type, value.pk, value)
        elif isinstance(value, DBRef):
            return ProxyLazyReference(self.document_type, value.id)
        else:
            return ProxyLazyReference(self.document_type, value)


class EnumField(BaseField):
    """定义枚举字段类型"""

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
    """定义字符串形式的每句字段类型"""

    def __set__(self, instance: Any, value: Any) -> None:
        super().__set__(instance, value)
