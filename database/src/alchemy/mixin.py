from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Boolean, DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    """
    模型基类
    """

    # 抽象类
    __abstract__ = True

    # 表参数, 允许自增 ID
    __table_args__ = {
        "sqlite_autoincrement": True,
    }

    # 主键, ID 字段
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # 记录创建时间戳
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),  # noqa
    )

    def jsonify(self) -> Dict[str, Any]:
        """
        当前对象转为字段

        Returns:
            `Dict[str, Any]`: 返回的字典对象
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
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def soft_delete(self) -> None:
        """
        软删除当前实体
        """
        self.deleted = True
