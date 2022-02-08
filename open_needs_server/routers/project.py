from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from open_needs_server import api, schemas
from open_needs_server.dependencies import get_db


projects = APIRouter(
    prefix="/api/projects",
    tags=["projects"],
    dependencies=[],
    responses={"404": {"description": "Not found"}}
)


@projects.get("/", response_model=list[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_projects = api.get_projects(db, skip=skip, limit=limit)
    return db_projects


@projects.get("/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = api.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@projects.post("/{project_id}/needs/", response_model=schemas.Need)
def create_need_for_project(project_id: int, need: schemas.NeedCreate, db: Session = Depends(get_db)):
    return api.create_need(db=db, project_id=project_id, need=need)
