import logging
from fastapi import Depends, HTTPException
from fastapi_users import FastAPIUsers
from pydantic.types import List

from .security import auth_backend, get_user_manager
from .schemas import UserReturnSchema, UserCreateSchema, UserUpdateSchema, UserDBSchema


log = logging.getLogger(__name__)

fastapi_users_ext = FastAPIUsers(
            get_user_manager,
            [auth_backend],
            UserReturnSchema,
            UserCreateSchema,
            UserUpdateSchema,
            UserDBSchema,
        )

current_user = fastapi_users_ext.current_user()
current_active_user = fastapi_users_ext.current_user(active=True)
current_active_verified_user = fastapi_users_ext.current_user(active=True, verified=True)
current_superuser = fastapi_users_ext.current_user(active=True, superuser=True)


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: UserDBSchema = Depends(current_active_user)):
        user_roles = [role.name for role in user.roles]
        if not set(self.allowed_roles).issubset(user_roles):
            log.debug(f'User {user.email} has no role for {self.allowed_roles}')
            raise HTTPException(status_code=403, detail='Operation not permitted')
        else:
            log.debug(f'User {user.email} has needed roles')
