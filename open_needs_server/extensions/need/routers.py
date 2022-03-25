from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session


from .schemas import NeedSchema, NeedCreateSchema
from .api import get_needs, get_need, create_need, OnsApiNeedException


from open_needs_server.dependencies import get_db


needs_router = APIRouter(
    prefix="/api/needs",
    tags=["needs"],
    dependencies=[],
    responses={"404": {"description": "Not found"}}
)


@needs_router.get("/", response_model=list[NeedSchema])
async def rest_read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    needs = await get_needs(db, skip=skip, limit=limit)
    return needs


@needs_router.post("/", response_model=NeedSchema)
async def rest_create_need(need: NeedCreateSchema, db: Session = Depends(get_db)):
    need_json = jsonable_encoder(need)

    try:
        need_db = await create_need(db=db, need=need_json)
    except OnsApiNeedException as e:
        raise HTTPException(e)

    return need_db
