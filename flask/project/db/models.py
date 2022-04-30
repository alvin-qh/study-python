from datetime import date, datetime
from typing import Any, Dict, List

from sqlalchemy import Date, DateTime, Integer, String

from db import db
from forms import Page


def to_dict(obj: Any) -> Dict[str, Any]:
    """
    将实体对象转为字典
    """
    return {item[0]: item[1] for item in obj.__dict__.items()
            if not item[0].startswith('_') and not callable(item[1])}


class User(db.Model):
    """
    用户实体，对应 core_users 表
    """
    __tablename__ = "core_users"  # 实体对应的表
    __table_args__ = {"sqlite_autoincrement": True}  # 使用自增 ID

    # ID 字段
    id: int = db.Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    # 身份证号码字段
    id_num: str = db.Column(
        String(50),
        nullable=False,
    )
    # 用户名字段
    name: str = db.Column(
        String(50),
        nullable=False,
    )
    # 性别字段
    gender: str = db.Column(
        String(1),
        nullable=False,
    )
    # 生日字段
    birthday: date = db.Column(
        Date,
        nullable=True,
    )
    # 创建时间字段
    created_at: datetime = db.Column(
        DateTime,
        nullable=False,
        server_default=db.func.now(),
    )
    # 用户组关系，对应 UserGroup 实体
    user_groups: "UserGroup" = db.relationship(
        "UserGroup",
        backref="user",
    )
    # 用户所在的组，对应 Group 实体
    groups: "Group" = db.relationship(
        "Group",
        secondary="core_user_groups",
        back_populates="users",
    )

    @classmethod
    def find_all(cls, page: Page = None) -> List["User"]:
        """
        查找所有用户
        """
        # 如果有分页对象，则返回一页结果
        if page:
            return cls.query.paginate(page.page_index, per_page=page.page_size)

        # 返回所有查询结果
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id_: int) -> "User":
        """
        通过 ID 查询一个用户
        """
        return cls.query.filter(cls.id == id_).first()

    def delete(self, flush: bool = True) -> None:
        """
        删除当前用户
        """
        db.session.delete(self)

        if flush:
            db.session.flush()

    def create(self, flush: bool = True) -> None:
        """
        持久化当前用户
        """
        db.session.add(self)

        if flush:
            db.session.flush()

    def update(self, **kwargs: Dict[str, Any]) -> None:
        """
        更新用户属性
        """
        self.id_num = kwargs.get("id_num", self.id_num)
        self.name = kwargs.get("name", self.name)
        self.gender = kwargs.get("gender", self.gender)
        self.birthday = kwargs.get("birthday", self.birthday)

        if kwargs.get("flush", True):
            db.session.flush()

    def jsonify(self) -> Dict[str, Any]:
        """
        对象转为字典
        """
        return {
            "id": self.id,
            "id_num": self.id_num,
            "name": self.name,
            "gender": self.gender,
            "birthday": self.birthday,
            "created_at": self.created_at,
            "groups": [g.jsonify() for g in self.groups]
        }


class Group(db.Model):
    """
    用户组实体
    """
    __tablename__ = "core_groups"  # 实体对应的表
    __table_args__ = {"sqlite_autoincrement": True}  # 使用自增 ID

    # 自增 ID
    id: int = db.Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    # 组名称
    name: str = db.Column(
        String(50),
        nullable=False,
    )
    # 创建时间
    created_at: datetime = db.Column(
        DateTime,
        nullable=False,
        server_default=db.func.now(),
    )
    # 用户和组关系，对应 UserGroup 实体
    user_groups: "UserGroup" = db.relationship(
        "UserGroup",
        backref="group",
    )
    # 组中的用户，对应 User 实体
    users: List[User] = db.relationship(
        "User",
        secondary="core_user_groups",
        back_populates="groups",
    )

    @classmethod
    def find_all(cls) -> List["Group"]:
        """
        查询所有的组
        """
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id_: int) -> "Group":
        """
        根据 ID 查询组
        """
        return cls.query.filter(cls.id == id_).first()

    def delete(self, flush: bool = True) -> None:
        """
        删除当前组
        """
        db.session.delete(self)

        if flush:
            db.session.flush()

    def create(self, flush: bool = True) -> None:
        """
        持久化当前组
        """
        db.session.add(self)

        if flush:
            db.session.flush()

    def jsonify(self) -> Dict[str, Any]:
        """
        实体转为字典
        """
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at
        }


class UserGroup(db.Model):
    """
    用户和组关系
    """
    __tablename__ = "core_user_groups"  # 对应的表名称
    __table_args__ = {"sqlite_autoincrement": True}  # 使用自增 ID

    # 自增 ID
    id: int = db.Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    # 关联的 User 实体 ID
    user_id: int = db.Column(
        Integer,
        db.ForeignKey("core_users.id"),
        nullable=False,
    )
    # 关联的 Group 实体 ID
    group_id: int = db.Column(
        Integer,
        db.ForeignKey("core_groups.id"),
        nullable=False,
    )
    # 创建时间
    created_at: datetime = db.Column(
        DateTime,
        nullable=False,
        server_default=db.func.now(),
    )

    # user - backref by User.user_group
    # group - backref by Group.user_group

    @classmethod
    def find_all(cls) -> List["UserGroup"]:
        """
        查找所有
        """
        return cls.query.all()

    @classmethod
    def find_by_users_with_group(cls, user_ids: List[int]) -> List["UserGroup"]:
        """
        根据用户 ID 查询用户和组关系
        """
        return (
            cls.query
            .filter(cls.user_id.in_(user_ids))
            .join(User, db.and_(User.id == cls.user_id))
            .all()
        )

    @classmethod
    def delete_by_user(cls, user) -> None:
        """
        根据用户信息删除关系
        """
        cls.query.filter(cls.user_id == user.id).delete()

    def create(self, flush: bool = True) -> None:
        """
        持久化当前实体
        """
        db.session.add(self)

        if flush:
            db.session.flush()

    def delete(self, flush: bool = True) -> None:
        """
        删除当前实体
        """
        db.session.delete(self)

        if flush:
            db.session.flush()


def clear_tables() -> None:
    """
    删除相关表内容
    """
    for table in [User, Group, UserGroup]:
        db.session.execute(f"DELETE FROM {table.__tablename__}")
        db.session.commit()
