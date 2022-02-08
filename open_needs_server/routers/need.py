from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from open_needs_server import api, schemas
from open_needs_server.dependencies import get_db


needs = APIRouter(
    prefix="/api/needs",
    tags=["needs"],
    dependencies=[],
    responses={"404": {"description": "Not found"}}
)


@needs.get("/needs/", response_model=list[schemas.Need])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    needs = api.get_needs(db, skip=skip, limit=limit)
    return needs
