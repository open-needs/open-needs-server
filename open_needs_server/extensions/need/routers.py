from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from open_needs_server.extensions.base import ONSExtension
from open_needs_server.extensions.user_security.dependencies import current_active_user, RoleChecker
from open_needs_server.extensions.user_security.models import UserModel

from .schemas import NeedReturnSchema, NeedCreateSchema, NeedUpdateSchema
from .api import *

from open_needs_server.dependencies import get_db

needs_router = APIRouter(
    prefix="/api/needs",
    tags=["needs"],
    dependencies=[],
    responses={"404": {"description": "Not found"}}
)


async def get_extension(request: Request):
    return request.app.ons_extensions['NeedExtension']


read_needs = RoleChecker(['view_needs_all'])
change_needs = RoleChecker(['change_needs_all'])
delete_needs = RoleChecker(['delete_needs_all'])


@needs_router.get("/",
                  response_model=list[NeedReturnSchema],
                  dependencies=[Depends(read_needs)],
                  summary='List all needs')
async def rest_read_items(skip: int = 0,
                          limit: int = 100,
                          db: Session = Depends(get_db),
                          ext: ONSExtension = Depends(get_extension),
                          user: UserModel = Depends(current_active_user)
                          ):
    """Needed roles: view_organizations_all"""
    needs = await get_needs(ext, db, skip=skip, limit=limit)
    return needs


@needs_router.post("/",
                   response_model=NeedReturnSchema,
                   dependencies=[Depends(change_needs)],
                   summary='Create new need')
async def rest_create_need(need: NeedCreateSchema,
                           db: Session = Depends(get_db),
                           ext: ONSExtension = Depends(get_extension),
                           user: UserModel = Depends(current_active_user)
                           ):
    need_json = jsonable_encoder(need)

    try:
        need_db = await create_need(ext, db, need=need_json)
    except OnsApiNeedException as e:
        raise HTTPException(400, str(e))

    return need_db


@needs_router.get("/{need_id}",
                  response_model=NeedReturnSchema,
                  summary='Retrieve a need',
                  dependencies=[Depends(read_needs)])
async def rest_read_need(need_id: int,
                         db: AsyncSession = Depends(get_db),
                         ext: ONSExtension = Depends(get_extension),
                         user: UserModel = Depends(current_active_user)):
    db_need = await get_need(ext, db, need_id=need_id)
    if db_need is None:
        raise HTTPException(status_code=404, detail="Need not found")
    return db_need


@needs_router.put("/{need_id}",
                  response_model=NeedReturnSchema,
                  summary='Update a need',
                  dependencies=[Depends(change_needs)])
async def rest_update_need(need: NeedUpdateSchema,
                           need_id: int,
                           db: AsyncSession = Depends(get_db),
                           ext: ONSExtension = Depends(get_extension)):
    need_json = jsonable_encoder(need)
    db_need = await get_need(ext, db, need_id=need_id)
    if not db_need:
        raise HTTPException(status_code=404, detail="Need not found")

    db_need = await update_need(ext, db,
                                need_id=need_id,
                                need=need_json)
    return db_need


@needs_router.delete("/{need_id}",
                     response_model=NeedReturnSchema,
                     summary='Delete need',
                     dependencies=[Depends(delete_needs)])
async def rest_delete_need(need_id: int, db: AsyncSession = Depends(get_db),
                           ext: ONSExtension = Depends(get_extension)):
    """Deletes a selected needs by its ID"""
    try:
        db_need = await delete_need(ext, db, need_id=need_id)
    except OnsNeedNotFound as e:
        raise HTTPException(status_code=404, detail=e.msg)

    return db_need
