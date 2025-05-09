import enum
import json
from datetime import date
from typing import Any, Dict, List

from sqlalchemy import Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .encoder import ObjectEncoder
from .mixin import BaseModel, SoftDeleteMixin


class Gender(enum.Enum):
    MALE = "M"
    FEMALE = "F"


class User(BaseModel, SoftDeleteMixin):
    """表示用户的实体类"""

    # 对应的表名称
    __tablename__ = "user"

    # 身份证字段
    id_num: Mapped[str] = mapped_column(String(length=50), nullable=False)

    # 姓名字段
    name: Mapped[str] = mapped_column(String(length=50), nullable=False)

    # 性别字段
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False)

    # 生日字段
    birthday: Mapped[date] = mapped_column(Date, nullable=True)

    # 连接到 `UserGroup` 类，外键 `user.id`, 在 `UserGroup` 对象添加 user 字段
    user_groups: Mapped[List["UserGroup"]] = relationship(
        "UserGroup",
        # backref="user",  # `backref` 表示在 `UserGroup` 实体中自动创建 `user` 属性
        back_populates="user",
        # uselist=True,
    )

    # 以 `user_group` 为中间表，连接到 Group 类, 在 `Group` 对象添加 users 字段
    groups: Mapped[List["Group"]] = relationship(
        "Group",
        secondary="user_group",
        back_populates="users",  # `back_populates` 表示显式对应 `Group` 实体中的 `users` 属性
    )

    def jsonify(self) -> Dict[str, Any]:
        """当前对象转为字段

        Returns:
            `Dict[str, Any]`: 返回的字典对象
        """

        return {
            **super().jsonify(),
            "id_num": self.id_num,
            "name": self.name,
            "gender": self.gender,
            "birthday": self.birthday,
        }

    def __str__(self) -> str:
        """当前对象转为字符串

        Returns:
            `str`: json 字符串
        """
        return json.dumps(self.jsonify(), cls=ObjectEncoder, indent=2)


class Group(BaseModel):
    """表示用户组的实体类"""

    # 对应的表名称
    __tablename__ = "`group`"

    # 组名称
    name: Mapped[str] = mapped_column(String(length=50), nullable=False)

    # 连接到 UserGroup 类，外键 `user.id`, 在 `UserGroup` 对象添加 `group` 字段
    user_groups: Mapped[List["UserGroup"]] = relationship(
        "UserGroup",
        # backref="group",  # `backref` 表示在 `UserGroup` 实体中自动创建 `group` 属性
        back_populates="group",
        # uselist=True,
    )

    # 以 `user_group` 为中间表，连接到 User 类, 在 `User` 对象添加 groups 字段
    users: Mapped[List[User]] = relationship(
        "User",
        secondary="user_group",
        back_populates="groups",  # `back_populates` 表示显式对应 `User` 实体中的 `groups` 属性
    )

    def jsonify(self) -> Dict[str, Any]:
        """当前对象转为字段

        Returns:
            `Dict[str, Any]`: 返回的字典对象
        """

        return {
            **super().jsonify(),
            "name": self.name,
        }

    def __str__(self) -> str:
        """当前对象转为字符串

        Returns:
            `str`: json 字符串
        """
        return json.dumps(self.jsonify(), cls=ObjectEncoder, indent=2)


class UserGroup(BaseModel):
    """表示用户和分组的关系类"""

    # 对应的表名称
    __tablename__ = "user_group"

    # 组成员 ID
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)

    # 组 ID
    group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("`group`.id"), nullable=False
    )

    user: Mapped[User] = relationship("User", back_populates="user_groups")
    group: Mapped[Group] = relationship("Group", back_populates="user_groups")

    def __str__(self) -> str:
        return json.dumps(self.jsonify(), cls=ObjectEncoder, indent=2)
