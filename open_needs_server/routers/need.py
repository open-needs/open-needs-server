from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from open_needs_server import api, schemas
from open_needs_server.dependencies import get_db


needs = APIRouter(
    prefix="/api/needs",
    tags=["needs"],
    dependencies=[],
    responses={"404": {"description": "Not found"}}
)


@needs.get("/", response_model=list[schemas.Need])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    needs = api.get_needs(db, skip=skip, limit=limit)
    return needs


@needs.post("/", response_model=schemas.Need)
def create_need(need: schemas.NeedCreate, db: Session = Depends(get_db)):
    need_json = jsonable_encoder(need)

    try:
        need_db = api.create_need(db=db, need=need_json)
    except api.OnApiNeedException as e:
        raise HTTPException(e)

    return need_db
