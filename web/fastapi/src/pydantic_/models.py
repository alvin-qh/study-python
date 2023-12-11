from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel as BModel
from pydantic import Field


class BaseModel(BModel):
    id: Optional[int] = Field(
        default=None,
        gt=0,
    )


class AuditMixin:
    created_at: Annotated[
        Optional[datetime],
        Field(default=None),
    ] = None
    created_by: Annotated[
        Optional[int],
        Field(
            default=None,
            gt=0,
        ),
    ] = None
    updated_at: Annotated[
        Optional[datetime],
        Field(default=None),
    ] = None
    updated_by: Annotated[
        Optional[int],
        Field(
            default=None,
            gt=0,
        ),
    ]


class TenantMixin:
    org_id: Annotated[
        Optional[int],
        Field(
            default=None,
            gt=0,
        ),
    ]


class Org(BaseModel, AuditMixin):
    name: Annotated[
        str,
        Field(
            min_length=2,
            max_length=20,
            pattern=r"^[a-zA-Z0-9\.\-_]+$",
        ),
    ]


class User(BaseModel, TenantMixin):
    org_id: int = Field(gt=0)
    name: Annotated[
        str,
        Field(
            min_length=2,
            max_length=20,
            pattern=r"^[a-zA-Z0-9\.\-_]+$",
        ),
    ]
    email: Annotated[
        Optional[str],
        Field(
            default=None,
        ),
    ] = None
    phone: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=10,
            max_length=20,
            pattern=r"^[0-9\-]+$",
        ),
    ] = None
    created_at: Annotated[
        Optional[datetime],
        Field(default=None),
    ] = None
    updated_at: Annotated[
        Optional[datetime],
        Field(default=None),
    ] = None
