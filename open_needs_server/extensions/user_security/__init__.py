import logging
from fastapi import Depends, HTTPException
from fastapi_users import FastAPIUsers
from pydantic.types import List

from open_needs_server.extensions.base import ONSExtension
from open_needs_server.version import VERSION
from open_needs_server.database import engine

from .security import auth_backend, get_user_manager
from .schemas import UserReturnSchema, UserCreateSchema, UserUpdateSchema
from .routers import roles_router
from .api import create_role, get_role_by_name
from .dependencies import fastapi_users_ext

log = logging.getLogger(__name__)

USER_EVENTS = []


class UserSecurityExtension(ONSExtension):
    """Cares about User handling, Authentication and Authorization"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = VERSION

        for event in USER_EVENTS:
            self.register_event(*event)

        self.register_router(roles_router)

        self.register_router(
            fastapi_users_ext.get_auth_router(auth_backend),
            prefix="/auth/jwt",
            tags=["auth"],
        )

        self.register_router(
            fastapi_users_ext.get_register_router(UserReturnSchema, UserCreateSchema),
            prefix="/auth",
            tags=["auth"],
        )

        self.register_router(
            fastapi_users_ext.get_verify_router(UserReturnSchema),
            prefix="/auth",
            tags=["auth"],
        )

        self.register_router(
            fastapi_users_ext.get_reset_password_router(), prefix="/auth", tags=["auth"]
        )

        self.register_router(
            fastapi_users_ext.get_users_router(UserReturnSchema, UserUpdateSchema),
            prefix="/users",
            tags=["users"],
        )

        self.register_role("view_projects_all", "Can read all projects")
        self.register_role("view_roles_all", "Can read all roles")

        @self.ons_app.on_event("startup")
        async def load_roles():
            await self._load_roles()

    async def _load_roles(self):
        """Create role objects in database based on the registered roles by extensions"""
        async with engine.connect() as db:
            for name, role in self.ons_app.ons_roles.items():
                role_db = await get_role_by_name(db, role["name"])
                if not role_db:
                    await create_role(db, role["name"], role["description"])
