import uuid

from pydantic import BaseModel
from fastapi_users import schemas
from typing import List, Optional


# BASE

class RoleBaseSchema(BaseModel):
    name: str


# RETURN / GENERIC

class RoleReturnSchema(RoleBaseSchema):
    id: int
    name: str
    users: list[str] = None  # Throws error during login: greenlet_spawn has not been called; can't call await_() here. Was IO attempted in an unexpected place? (Background on this error at: https://sqlalche.me/e/14/xd2s)

    class Config:
        orm_mode = True


class UserReturnSchema(schemas.BaseUser[uuid.UUID]):
    # roles: Optional[List[RoleReturnSchema]] | None = []

    class Config:
        orm_mode = True


# CREATE

class UserCreateSchema(schemas.BaseUserCreate):
    pass


# UPDATE

class RoleUpdateSchema(BaseModel):
    users: List[str]


class UserUpdateSchema(schemas.BaseUserUpdate):
    pass
