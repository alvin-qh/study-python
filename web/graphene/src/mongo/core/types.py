from typing import Any, Generic, List, Optional, Tuple, TypeVar, Union, cast

from graphql import GraphQLError
from graphql_relay import from_global_id, to_global_id
from mongoengine import Document

from graphene import Connection, Int, PageInfo, ResolveInfo


def make_global_id(doc: Document) -> str:
    """根据 mongo 文档对象创建 Graphql 统一 id

    Args:
        - `doc` (`Document`): mongo 文档对象

    Returns:
        `str`: 统一 id
    """
    # 利用文档类名称作为类型计算统一 id
    return to_global_id(doc.__class__.__name__, doc.id)


def parse_global_id(global_id: str, doc: Optional[Document] = None) -> Tuple[str, str]:
    """从 Graphql 统一 id 还原其类型以及实际 id

    Args:
        - `global_id` (`str`): 统一 id
        - `doc` (`Optional[Document]`, optional): mongo 文档对象, 如果传递该参数, 则会验证统一 id 中的类型部分. Defaults to `None`.

    Raises:
        `GraphQLError`: 如果传递了 `doc` 参数, 且统一 id 中的类型和文档类型不匹配, 则抛出此异常

    Returns:
        `Tuple[str, str]`: 返回 `(原始 id, 类型)` 两部分值
    """
    # 解析统一 id, 返回原始信息
    src = from_global_id(global_id)

    # 如果原始信息中的文档类型不匹配, 则抛出异常
    if doc and src.type != doc.__class__.__name__:
        raise GraphQLError("invalid_global_id_type")

    # 返回原始 id 和类型
    return src.id, src.type


def make_cursor(cursor: Union[int, str]) -> str:
    """产生游标标识字符串, 为一个 Graphql 统一 id

    Args:
        - `cursor` (`Union[int, str]`): 游标原始值

    Returns:
        `str`: 转换为统一 id 的游标值
    """
    # 以 `__cursor__` 为类型, 编码原始游标值
    return to_global_id("__cursor__", cursor)


def parse_cursor(global_id: str) -> str:
    """解析编码为统一 id 的游标标识

    Args:
        - `global_id` (`str`): 统一 id 值

    Raises:
        `GraphQLError`: 如果解析后类型不正确, 则抛出此异常

    Returns:
        `str`: 解码后的原始游标值
    """
    id_ = from_global_id(global_id)
    if id_.type != "__cursor__":
        # 如果类型不正确, 则抛出异常
        raise GraphQLError("invalid_cursor_type")

    return id_.id


T = TypeVar("T")


class QueryResult(PageInfo, Generic[T]):
    """保存查询结果的类型, 记录一页的数据以及分页信息"""

    # 为继承 `Generic` 类打的补丁
    __parameters__ = ("~T",)

    def __init__(self, data: List[T], start: int, end: int, count: int) -> None:
        self._data = data
        self.start = start
        self.end = end
        self.count = count

    @property
    def start_cursor(self) -> str:
        """获取起始游标值

        Returns:
            int: 游标值
        """
        return make_cursor(self.start)

    @property
    def end_cursor(self) -> str:
        """获取终止游标值

        Returns:
            int: 游标值
        """
        return make_cursor(self.end)

    @property
    def has_next_page(self) -> bool:
        """是否有下一页

        Returns:
            bool: 是否有下一页
        """
        return self.end < self.count

    @property
    def has_previous_page(self) -> bool:
        """是否有上一页

        Returns:
            bool: 是否有上一页
        """
        return self.start > 0

    @property
    def data(self) -> List[T]:
        """获取一页的数据

        Returns:
            ListType[T]: 一页数据的集合
        """
        return self._data


class BaseConnection(Connection, Generic[T]):
    """连接类型超类"""

    # 为继承 `Generic` 类打的补丁
    __parameters__ = ("~T",)

    class Meta:
        abstract = True

    class Edge:
        """设置 `Connection` 中的元素"""

        def __init__(self, **kwargs: Any) -> None:
            """占位方法, 不会被调用"""

    # 表示全部数据数量的属性
    total_count = Int()

    def resolve_total_count(self, info: ResolveInfo) -> int:
        """解析总记录数属性

        Args:
            info (ResolveInfo): 解析上下文对象

        Returns:
            int: 总记录数
        """
        return cast(QueryResult[Any], self.page_info).count

    def resolve_edges(self, info: ResolveInfo) -> List[Edge]:
        """解析 `edges` 属性

        Args:
            info (ResolveInfo): 解析上下文对象

        Returns:
            ListType[Edge]: Edge 对象集合
        """
        start = self.page_info.start
        return [
            self.Edge(cursor=start + n, node=data)
            for n, data in enumerate(self.page_info.data)
        ]
