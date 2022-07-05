import logging
import uuid

from fastapi import Depends, HTTPException
from fastapi_users import FastAPIUsers
from pydantic.types import List
from sqlalchemy import select

from open_needs_server.dependencies import get_db

from .security import auth_backend, get_user_manager
from .models import RoleModel, UserModel

log = logging.getLogger(__name__)

fastapi_users_ext = FastAPIUsers[UserModel, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users_ext.current_user()
current_active_user = fastapi_users_ext.current_user(active=True)
current_active_verified_user = fastapi_users_ext.current_user(
    active=True, verified=True
)
current_superuser = fastapi_users_ext.current_user(active=True, superuser=True)


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    async def __call__(
        self, db=Depends(get_db), user: UserModel = Depends(current_active_user)
    ):
        result = await db.execute(
            select(RoleModel).filter(RoleModel.users.any(UserModel.email == user.email))
        )
        user_roles = [role.name for role in result.scalars().all()]

        if not set(self.allowed_roles).issubset(user_roles):
            log.debug(f"User {user.email} has no role for {self.allowed_roles}")
            raise HTTPException(status_code=403, detail="Operation not permitted")
        else:
            log.debug(
                f'User {user.email} has needed roles: {",".join(self.allowed_roles)}'
            )
