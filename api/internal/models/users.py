from __future__ import annotations
from decimal import Decimal
from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    name: str
    email: str
    balance: Decimal

class BaseResponse(BaseModel):
    detail: str

class UserModel(BaseModel):
    id: int
    name: str
    email: str
    balance: Decimal

    class Config:
        from_attributes = True

class UsersResponse(BaseModel):
    users: list[UserModel]
