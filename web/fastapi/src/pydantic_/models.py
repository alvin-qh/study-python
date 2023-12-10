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
