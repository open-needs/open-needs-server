import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import StatementError
from sqlalchemy import select, insert

from open_needs_server.exceptions import ONSExtensionException
from .models import RoleModel, UserModel
from .schemas import RoleUpdateSchema

log = logging.getLogger(__name__)


async def get_roles(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(RoleModel).offset(skip).limit(limit))
    roles = result.scalars().all()

    roles_clean = []
    for role in roles:
        role = role.to_dict()
        users_ids = [str(user.id) for user in role['users']]
        role['users'] = users_ids
        roles_clean.append(role)

    return roles_clean


async def get_role_by_name(db: AsyncSession, role_name: int):
    result = await db.execute(select(RoleModel).filter(RoleModel.name == role_name))
    return result.scalars().first()


async def create_role(db: AsyncSession, role_name: str, description: str):

    role = {
        'name': role_name,
        'description': description
    }

    cursor = await db.execute(insert(RoleModel), role)
    await db.commit()

    # Get the just created role object
    role_obj = await get_role_by_name(db, role['name'])
    return role_obj


async def update_role(db: AsyncSession, role_name: str, role: RoleUpdateSchema):

    # Be sure that the given users exist
    try:
        result = await db.execute(select(UserModel).filter(UserModel.id.in_(role['users'])))
    except StatementError as e:
        log.error(f'Invalid statement to update role: {e}')
        raise ONSExtensionException(f'Invalid statement to update role: {e}')

    role_users = result.scalars().all()

    if not role_users:
        raise ONSExtensionException(f'Referenced users not found: {role["users"]}')

    if len(role_users) != len(role['users']):
        found_ids = [str(ruser.id) for ruser in role_users]
        missing_users = [ruser for ruser in role['users'] if ruser not in found_ids]

        raise ONSExtensionException(f'Referenced users not found: {missing_users}')

    # Get the just created role object
    db_role = await get_role_by_name(db, role_name)

    for key, value in role.items():
        if key != 'users':
            setattr(db_role, key, value)
        else:
            # Now add the users to the role_obj
            db_role.users = []
            for user in role_users:
                if user not in db_role.users:
                    db_role.users.append(user)
    await db.commit()

    # Update the role_return value just by the user_ids and not the complete user object.
    role = db_role.to_dict()
    role = {**role, "users": [str(user.id) for user in db_role.users]}

    return role
