import json
from datetime import date
from typing import Any, Dict, List

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .encoder import ObjectEncoder
from .mixin import CommonMixin, SoftDeleteMixin


class Base(DeclarativeBase):
    """
    创建模型基类
    """


class User(Base, CommonMixin, SoftDeleteMixin):
    """
    表示用户的实体类
    """

    # 对应的表名称
    __tablename__ = "core_users"

    # 身份证字段
    id_num: Mapped[str] = mapped_column(String(length=50), nullable=False)

    # 姓名字段
    name: Mapped[str] = mapped_column(String(length=50), nullable=False)

    # 性别字段
    gender: Mapped[str] = mapped_column(String(length=1), nullable=False)

    # 生日字段
    birthday: Mapped[date] = mapped_column(Date, nullable=True)

    # 连接到 UserGroup 类，外键 `core_users.id`, 在 `UserGroup` 对象添加 user 字段
    user_group: Mapped[List["UserGroup"]] = relationship(
        "UserGroup",
        backref="user",
        # uselist=True,
    )

    # 以 `core_user_groups` 为中间表，连接到 Group 类, 在 `Group` 对象添加 users 字段
    groups: Mapped[List["Group"]] = relationship(
        "Group",
        secondary="core_user_groups",
        back_populates="users",
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
    name: Mapped[str] = mapped_column(String(length=50), nullable=False)

    # 连接到 UserGroup 类，外键 `core_users.id`, 在 `UserGroup` 对象添加 group 字段
    user_group: Mapped[List["UserGroup"]] = relationship(
        "UserGroup",
        backref="group",
        # uselist=True,
    )

    # 以 `core_user_groups` 为中间表，连接到 User 类, 在 `User` 对象添加 groups 字段
    users: Mapped[List[User]] = relationship(
        "User",
        secondary="core_user_groups",
        back_populates="groups",
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
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("core_users.id"), nullable=False
    )

    # 组 ID
    group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("core_groups.id"), nullable=False
    )

    # user - backref by User.user_group
    # user = relationship("User", back_populates="user_group")

    # group - backref by Group.user_group
    # group = relationship("Group", back_populates="user_group")

    def __str__(self) -> str:
        return json.dumps(self.jsonify(), cls=ObjectEncoder, indent=2)