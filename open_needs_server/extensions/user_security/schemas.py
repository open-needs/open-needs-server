from pydantic import BaseModel
from fastapi_users import models
from typing import List, Optional


# BASE

class RoleBaseSchema(BaseModel):
    name: str


# RETURN / GENERIC

class RoleReturnSchema(RoleBaseSchema):
    id: int
    users: list[str] = None

    class Config:
        orm_mode = True


class UserReturnSchema(models.BaseUser):
    roles: Optional[List[RoleReturnSchema]] = []

    class Config:
        orm_mode = True


# CREATE

class UserCreateSchema(models.BaseUserCreate):
    pass


# UPDATE

class RoleUpdateSchema(BaseModel):
    users: List[str]


class UserUpdateSchema(models.BaseUserUpdate):
    pass


# DB

class UserDBSchema(UserReturnSchema, models.BaseUserDB):
    pass


