from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from open_needs_server.extensions.need.schemas import NeedReturnSchema
from .api import filter_needs, OnApiFilterException
from .schemas import FilterSchema

from open_needs_server.dependencies import get_db


filter_router = APIRouter(
    prefix="/api/filter",
    tags=["filter"],
    dependencies=[],
    responses={"404": {"description": "Not found"}}
)


@filter_router.post("/needs", response_model=list[NeedReturnSchema])
async def rest_filter_needs(filters: FilterSchema, db: Session = Depends(get_db)):
    filters_json = jsonable_encoder(filters, exclude_unset=True)
    try:
        need_db = await filter_needs(db=db, filters=filters_json)
    except OnApiFilterException as e:
        raise HTTPException(e)

    return need_db
