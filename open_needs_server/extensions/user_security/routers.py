from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from open_needs_server.dependencies import get_db
from open_needs_server.exceptions import ONSExtensionException

from .schemas import RoleReturnSchema, RoleUpdateSchema
from .api import get_roles, get_role_by_name, update_role
from .dependencies import RoleChecker, current_active_user

roles_router = APIRouter(
    prefix="/api/roles",
    tags=["roles"],
    dependencies=[],
    responses={"404": {"description": "Not found"}}
)


read_roles = RoleChecker(['view_roles_all'])


@roles_router.get("/", response_model=list[RoleReturnSchema],
                  dependencies=[Depends(read_roles)])
async def rest_read_roles(skip: int = 0, limit: int = 100,
                          user: UserWarning = Depends(current_active_user),
                          db: AsyncSession = Depends(get_db)):
    db_projects = await get_roles(db, skip=skip, limit=limit)
    return db_projects


@roles_router.put("/{role_name}", response_model=RoleReturnSchema)
async def rest_create_role(
        role_name: str,
        role: RoleUpdateSchema,
        db: AsyncSession = Depends(get_db)):
    role_json = jsonable_encoder(role)
    db_role = await get_role_by_name(db, role_name=role_name)
    if not db_role:
        raise HTTPException(status_code=404, detail="Unknown role")

    try:
        db_role = await update_role(db, role_name=role_name, role=role_json)
    except ONSExtensionException as e:
        raise HTTPException(status_code=400, detail=e.msg)
    return db_role
