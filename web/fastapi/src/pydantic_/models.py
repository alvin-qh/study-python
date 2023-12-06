from typing import Annotated
from pydantic import BaseModel, Field


class Org(BaseModel):
    id: int
    name: str


class User(BaseModel):
    id: int
    org_id: int
    name: str = Field(min_length=2, max_length=10)
    email: Annotated[str, Field(default=None, )]
    phone: str
    address: str
    city: str
    state: str
    zip: str
    country: str
    website: str
    lat: float
    lng: float
    created_at: str
    updated_at: str
    deleted_at: str
    is_active: bool
    is_admin: bool
    is_super_admin: bool
    is_verified: bool
    is_locked: bool
    is_deleted: bool
    is_banned: bool
    is_suspended: bool
    is_public: bool
    is_public_profile: bool
    is_public_email: bool
    is_public_phone: bool
    is_public_address: bool
    is_public_city: bool
    is_public_state: bool
    is_public_zip: bool
    is_public_country: bool
    is_public_website: bool
    is_public_lat: bool
    is_public_lng: bool
