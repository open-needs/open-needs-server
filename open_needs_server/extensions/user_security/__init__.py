import logging
from fastapi import Depends, HTTPException
from fastapi_users import FastAPIUsers
from pydantic.types import List

from open_needs_server.extensions.base import ONSExtension
from open_needs_server.version import VERSION
from .security import auth_backend, get_user_manager
from .schemas import UserReturnSchema, UserCreateSchema, UserUpdateSchema, UserDBSchema
from .routers import roles_router

log = logging.getLogger(__name__)

USER_EVENTS = []


fastapi_users = FastAPIUsers(
            get_user_manager,
            [auth_backend],
            UserReturnSchema,
            UserCreateSchema,
            UserUpdateSchema,
            UserDBSchema,
        )

current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: UserDBSchema = Depends(current_active_user)):
        if user.roles not in self.allowed_roles:
            log.debug(f'User {user.email} has no role for {self.allowed_roles}')
            raise HTTPException(status_code=403, detail='Operation not permitted')


class UserSecurityExtension(ONSExtension):
    """Cares about User handling, Authentication and Authorization"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = VERSION

        for event in USER_EVENTS:
            self.register_event(*event)

        self.register_router(roles_router)

        self.register_router(fastapi_users.get_auth_router(auth_backend),
                             prefix="/auth/jwt",
                             tags=["auth"])

        self.register_router(fastapi_users.get_register_router(),
                             prefix="/auth",
                             tags=["auth"])

        self.register_router(fastapi_users.get_verify_router(),
                             prefix="/auth",
                             tags=["auth"])

        self.register_router(fastapi_users.get_reset_password_router(),
                             prefix="/auth",
                             tags=["auth"])

        self.register_router(fastapi_users.get_users_router(),
                             prefix="/users",
                             tags=["users"])

