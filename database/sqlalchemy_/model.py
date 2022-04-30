import json
from datetime import date, datetime
from typing import Any, Dict, Optional, Tuple, Type

from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer,
                        String, create_engine, func, orm, pool)
from sqlalchemy.ext.declarative import declarative_base

# 创建数据库连接引擎
engine = create_engine(
    "sqlite:///:memory:",
    echo=True,
    pool_size=5,
    max_overflow=0,
    poolclass=pool.QueuePool,
)


class ExtQuery(orm.Query):
    """
    扩展查询类, 继承原查询类
    """
    def __new__(cls, *args, **kwargs) -> "ExtQuery":
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

    def _add_soft_delete_filter(self, query_types: Tuple[Type]) -> "ExtQuery":
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
                return self.filter(t.deleted == False)

        return self


# 创建 Session, scoped_session 函数用于在 Locale 范围中创建 session 对象
# 指定查询类为 ExtQuery, 对原查询做扩展
Session = orm.scoped_session(
    orm.sessionmaker(bind=engine, autocommit=False, query_cls=ExtQuery)
)

# 创建模型基类
Base = declarative_base()


class ObjectEncoder(json.JSONEncoder):
    """
    Json 序列化扩展类
    """

    def default(self, obj: Any) -> Optional[str]:
        """
        默认转换规则

        Args:
            obj (Any): 任意对象

        Returns:
            Optional[str]: None 或字符串
        """

        s: Optional[str] = None

        # 判断如果对象是日期或时间按日期类型, 则将其转为字符串
        if isinstance(obj, (date, datetime)):
            s = obj.isoformat()

        # 其它类型不做转换
        return s


class CommonMixin:
    """
    公共混入类, 为数据实体添加 ID 和 created_at 字段
    """

    # 抽象类
    __abstract__ = True

    # 表参数, 允许自增 ID
    __table_args__ = {
        "sqlite_autoincrement": True,
    }

    # 主键, ID 字段
    id = Column(Integer, primary_key=True)

    # 记录创建时间戳
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    def jsonify(self) -> Dict[str, Any]:
        """
        当前对象转为字段

        Returns:
            Dict[str, Any]: 返回的字典对象
        """

        return {
            "id": self.id,
            "created_at": self.created_at,
        }


class SoftDeleteMixin:
    """
    软删除混入类, 为数据实体添加软删除能力
    """
    # 表示删除的字段
    deleted = Column(Boolean, nullable=False, default=False)

    def soft_delete(self) -> None:
        """
        软删除当前实体
        """
        self.deleted = True


# 以下注释代码演示了如何监听查询 SqlAlchemy 的事件
#
# @event.listens_for(Query, "before_compile", retval=True)
# def _soft_delete_handler(query: Query) -> Query:
#     """
#     执行查询时的事件处理函数, "before_compile" 表示在生成 SQL 语句前执行
#
#     Args:
#         query(Query): 被监听的查询对象
#
#     Returns:
#         Query: 做过处理的 Query 对象
#     """
#
#     # 遍历查询对象的字段描述
#     for desc in query.column_descriptions:
#         # 获取查询的实体对象类型
#         type_ = desc["type"]
#         # 判断实体对象是否支持软删除
#         if type_ and issubclass(type_, SoftDeleteMixin):
#             # 添加软删除检索条件
#             entity = desc["entity"]
#             query = query.filter(entity.deleted == False)
#
#     return query


class User(Base, CommonMixin, SoftDeleteMixin):
    """
    表示用户的实体类
    """

    # 对应的表名称
    __tablename__ = "core_users"

    # 身份证字段
    id_num = Column(String(length=50), nullable=False)
    # 姓名字段
    name = Column(String(length=50), nullable=False)
    # 性别字段
    gender = Column(String(length=1), nullable=False)
    # 生日字段
    birthday = Column(Date, nullable=True)

    # 连接到 UserGroup 类，外键 `core_users.id`, 在 `UserGroup` 对象添加 user 字段
    user_group = orm.relationship("UserGroup", backref="user")
    # 以 `core_user_groups` 为中间表，连接到 Group 类, 在 `Group` 对象添加 users 字段
    groups = orm.relationship(
        "Group", secondary="core_user_groups", back_populates="users",
    )

    def jsonify(self) -> Dict[str, Any]:
        """
        当前对象转为字段

        Returns:
            Dict[str, Any]: 返回的字典对象
        """

        return {
            **super().jsonify(),
            "id_num": self.id_num,
            "name": self.name,
            "gender": self.gender,
            "birthday": self.birthday,
        }

    def __str__(self) -> str:
        """
        当前对象转为字符串

        Returns:
            str: json 字符串
        """
        return json.dumps(self.jsonify(), cls=ObjectEncoder, indent=2)


class Group(Base, CommonMixin):
    """
    表示用户组的实体类
    """

    # 对应的表名称
    __tablename__ = "core_groups"

    # 组名称
    name = Column(String(length=50), nullable=False)

    # 连接到 UserGroup 类，外键 `core_users.id`, 在 `UserGroup` 对象添加 group 字段
    user_group = orm.relationship("UserGroup", backref="group")
    # 以 `core_user_groups` 为中间表，连接到 User 类, 在 `User` 对象添加 groups 字段
    users = orm.relationship(
        "User", secondary="core_user_groups", back_populates="groups",
    )

    def jsonify(self) -> Dict[str, Any]:
        """
        当前对象转为字段

        Returns:
            Dict[str, Any]: 返回的字典对象
        """

        return {
            **super().jsonify(),
            "name": self.name,
        }

    def __str__(self) -> str:
        """
        当前对象转为字符串

        Returns:
            str: json 字符串
        """
        return json.dumps(self.jsonify(), cls=ObjectEncoder, indent=2)


class UserGroup(Base, CommonMixin):
    """
    表示用户和分组的关系类
    """

    # 对应的表名称
    __tablename__ = "core_user_groups"

    # 组成员 ID
    user_id = Column(Integer, ForeignKey("core_users.id"), nullable=False)
    # 组 ID
    group_id = Column(Integer, ForeignKey("core_groups.id"), nullable=False)

    # user - backref by User.user_group
    # user = relationship("User", back_populates="user_group")

    # group - backref by Group.user_group
    # group = relationship("Group", back_populates="user_group")

    def jsonify(self):
        return {
            **super().jsonify(),
            "user": self.user.jsonify(),
            "group": self.group.jsonify(),
        }

    def __str__(self):
        return json.dumps(self.jsonify(), cls=ObjectEncoder, indent=2)
