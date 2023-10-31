from typing import Any, Self, Tuple, Type

from sqlalchemy import create_engine, pool
from sqlalchemy.orm import Query, scoped_session, sessionmaker

from .mixin import SoftDeleteMixin


class ExtQuery(Query[Any]):
    """
    扩展查询类, 继承原查询类
    """

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """
        实例化查询对象

        Returns:
            ExtQuery: 实例化的查询对象
        """
        query = super().__new__(cls)

        # 判断是否携带参数
        if args and len(args) > 0:
            # 对 soft delete 进行处理
            query = query._add_soft_delete_filter(args[0])

        return query

    def _add_soft_delete_filter(self, query_types: Tuple[Type[Any]]) -> Self:
        """
        尝试增加 soft delete 查询条件

        Args:
            query_types (Tuple[Type]): 要查询的实体类型

        Returns:
            ExtQuery: 返回查询对象
        """
        for t in query_types:
            # 判断实体类型是否支持 soft delete
            if isinstance(t, type) and issubclass(t, SoftDeleteMixin):
                # 增加 soft delete 查询条件
                return self.filter(t.deleted == False)  # noqa

        return self


# 创建数据库连接引擎
engine = create_engine(
    "sqlite:///:memory:",
    echo=True,
    pool_size=5,
    max_overflow=0,
    poolclass=pool.QueuePool,
)

# 创建 Session, scoped_session 函数用于在 Locale 范围中创建 session 对象
# 指定查询类为 ExtQuery, 对原查询做扩展
session = scoped_session(
    sessionmaker(bind=engine, autocommit=False, query_cls=ExtQuery)
)


""" 以下代码演示了如何增加监听器, 在语句执行前执行处理
@listens_for(Session, identifier="do_orm_execute")
def execution_listener(state: ORMExecuteState):
    if not state.is_select:
        return

    # Rewrite the statement
    adapted = soft_delete_rewriter(state.statement)

    # Replace the statement
    state.statement = adapted
"""
