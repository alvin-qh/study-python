from datetime import date
from enum import Enum
from multiprocessing import RLock
from typing import Annotated, Any, Dict, Optional, TypeVar

from fastapi import Response, status
from pydantic import BaseModel as BModel
from pydantic import Field, SerializationInfo, field_serializer, field_validator

from .app import app


class Gender(str, Enum):
    """性别枚举"""

    MALE = "male"
    FEMALE = "female"


class BaseModel(BModel):
    """所有模型的基类"""

    id: Optional[int] = Field(
        default=None,
        title="ID",
        description="ID of model",
    )


class User(BaseModel):
    """表示用户的模型类型

    模型类型的字段可以通过三种方式进行类型定义:

    - 通过 Python 的 Type hits 进行类型定义
    - 通过 Pydantic 的 Field 作为字段值, 其中指定了字段的类型和其它信息
    - 通过 `Annotated` 进行字段类型定义, 并在其中指定 Field 对象类型
    """

    name: str = Field(
        title="Name",
        description="User's name",
        example="Alvin",
        min_length=2,
        max_length=20,
    )

    gender: Gender = Field(
        title="Gender",
        description="User's gender",
        example=Gender.MALE,
        pattern=r"^(male|female)$",
    )

    birthday: Annotated[
        Optional[date],
        Field(
            title="Birthday",
            description="User's birthday",
        ),
    ] = None

    email: Annotated[
        Optional[str],
        Field(
            title="Email",
            description="User's email address",
        ),
    ] = None

    @field_serializer("birthday")
    def serialize_birthday(self, birthday: date, _info: SerializationInfo) -> str:
        """自定义 `birthday` 字段的序列号

        当调用 `model_dump` 方法时，将会调用此方法将 `birthday` 字段序列化为字符串。

        Args:
            - `birthday` (`date`): 用户的生日
            - `_info` (`SerializationInfo`): 序列化信息

        Returns:
            `str`: 序列化后的字符串
        """
        return birthday.isoformat()

    @field_validator("birthday")
    @classmethod
    def validate_birthday(cls, birthday: date) -> date:
        """自定义 `birthday` 字段的验证器

        当验证模型对象时, 调用此方法对 `birthday` 字段进行验证

        Args:
            - `birthday` (`date`): 用户的生日

        Returns:
            `date`: 验证后正确的用户生日值
        """
        assert birthday <= date.today(), "Birthday cannot be in the future"
        assert birthday.year >= 1910, "Birthday cannot be less than 1910"
        return birthday


# 定义模型泛型类型
_ModelType = TypeVar("_ModelType", bound=BaseModel)


class Storage:
    """模型存储类型"""

    def __init__(self) -> None:
        self._lock = RLock()
        # 用于存储模型的字典
        self._store: Dict[int, BaseModel] = {}
        self._last_id = 1

    def create(self, model: _ModelType) -> _ModelType:
        """存储模型对象

        Args:
            - `model` (`_ModelType`): 新模型对象

        Returns:
            `_ModelType`: 已存储的模型对象
        """
        if model.id is not None:
            raise ValueError("Model already persisted")

        with self._lock:
            model.id = self._last_id
            self._store[model.id] = model
            self._last_id += 1

        return model

    def get(self, id: int) -> Optional[BaseModel]:
        """根据 `id` 查询对应的模型对象

        Args:
            - `id` (`int`): 模型 id 属性值

        Returns:
            `Optional[BaseModel]`: 返回模型的查询结果
        """
        return self._store.get(id)


_storage = Storage()


@app.get(
    "/api/user/{id}",
    summary="Model Demo",
    description="Get User Model",
    tags=["Model"],
)
async def get_user(response: Response, id: int) -> Dict[str, Any]:
    may_user = _storage.get(id)

    if not may_user or not isinstance(may_user, User):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "status": "error",
            "payload": {"message": "User not found"},
        }

    return {
        "status": "success",
        "payload": {
            "user": may_user.model_dump(),
        },
    }


@app.post(
    "/api/user",
    summary="Model Demo",
    description="Create User Model",
    tags=["Model"],
)
async def create_user(response: Response, user: User) -> Dict[str, Any]:
    try:
        user = _storage.create(user)
        return {
            "status": "success",
            "payload": {
                "user": user.model_dump(),
            },
        }
    except ValueError:
        response.status_code = status.HTTP_409_CONFLICT
        return {
            "status": "error",
            "payload": {"message": "User already exists"},
        }
