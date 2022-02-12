from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from open_needs_server import api, schemas
from open_needs_server.dependencies import get_db


filters = APIRouter(
    prefix="/api/filter",
    tags=["filter"],
    dependencies=[],
    responses={"404": {"description": "Not found"}}
)


@filters.post("/needs", response_model=list[schemas.Need])
def filter_needs(filters: schemas.Filter, db: Session = Depends(get_db)):
    filters_json = jsonable_encoder(filters, exclude_unset=True)
    try:
        need_db = api.filter_needs(db=db, filters=filters_json)
    except api.OnApiNeedException as e:
        raise HTTPException(e)

    return need_db
