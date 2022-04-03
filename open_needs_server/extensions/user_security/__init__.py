import logging
from fastapi_users import FastAPIUsers

from open_needs_server.extensions.base_extension import ONSExtension
from open_needs_server.version import VERSION
from .security import auth_backend, get_user_manager
from .schemas import UserSchema, UserCreateSchema, UserUpdateSchema, UserDBSchema

log = logging.getLogger(__name__)

USER_EVENTS = []


class UserSecurityExtension(ONSExtension):
    """Cares about User handling, Authentication and Authorization"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = VERSION

        fastapi_users = FastAPIUsers(
            get_user_manager,
            [auth_backend],
            UserSchema,
            UserCreateSchema,
            UserUpdateSchema,
            UserDBSchema,
        )

        for event in USER_EVENTS:
            self.register_event(*event)

        self.current_active_user = fastapi_users.current_user(active=True)

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
