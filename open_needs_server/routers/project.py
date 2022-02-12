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


@projects.post("/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):

    db_project = api.get_organization_project_by_title(db, organization_id=project.organization_id,
                                                       project_title=project.title)
    if db_project:
        raise HTTPException(status_code=400, detail="Project already registered for organization")

    db_project = api.create_organization_project(db, project=project)
    return db_project


@projects.get("/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = api.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project



