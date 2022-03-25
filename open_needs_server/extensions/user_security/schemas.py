from fastapi_users import models


class UserSchema(models.BaseUser):
    pass


class UserCreateSchema(models.BaseUserCreate):
    pass


class UserUpdateSchema(models.BaseUserUpdate):
    pass


class UserDBSchema(UserSchema, models.BaseUserDB):
    pass
