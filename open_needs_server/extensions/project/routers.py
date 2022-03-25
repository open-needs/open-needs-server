from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession


from .schemas import ProjectSchema, ProjectCreateSchema
from .api import get_project, get_projects, get_organization_project_by_title, create_project

from open_needs_server.dependencies import get_db


projects_router = APIRouter(
    prefix="/api/projects",
    tags=["projects"],
    dependencies=[],
    responses={"404": {"description": "Not found"}}
)


@projects_router.get("/", response_model=list[ProjectSchema])
async def rest_read_projects(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    db_projects = await get_projects(db, skip=skip, limit=limit)
    return db_projects


@projects_router.post("/", response_model=ProjectSchema)
async def rest_create_project(project: ProjectCreateSchema, db: AsyncSession = Depends(get_db)):
    project_json = jsonable_encoder(project)
    db_project = await get_organization_project_by_title(db, organization_id=project.organization_id,
                                                       project_title=project.title)
    if db_project:
        raise HTTPException(status_code=400, detail="Project already registered for organization")

    db_project = await create_project(db, project=project_json)
    return db_project


@projects_router.get("/{project_id}", response_model=ProjectSchema)
async def rest_read_project(project_id: int, db: AsyncSession = Depends(get_db)):
    db_project = await get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project



