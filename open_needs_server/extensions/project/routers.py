from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from open_needs_server.extensions.base import ONSExtension
from open_needs_server.extensions.user_security.models import UserModel
from open_needs_server.extensions.user_security.dependencies import (
    current_active_user,
    RoleChecker,
)

from .schemas import ProjectSchema, ProjectCreateSchema, ProjectChangeSchema
from .api import *

from open_needs_server.dependencies import get_db

projects_router = APIRouter(
    prefix="/api/projects",
    tags=["projects"],
    dependencies=[],
    responses={"404": {"description": "Not found"}},
)


async def get_extension(request: Request):
    return request.app.ons_extensions["ProjectExtension"]


read_projects = RoleChecker(["view_projects_all"])
write_projects = RoleChecker(["change_projects_all"])
delete_projects = RoleChecker(["delete_projects_all"])


@projects_router.get(
    "/",
    response_model=list[ProjectSchema],
    dependencies=[Depends(read_projects)],
    summary="List all projects",
    description="Needed roles: view_project_all",
)
async def rest_read_projects(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    ext: ONSExtension = Depends(get_extension),
    user: UserModel = Depends(current_active_user),
):
    db_projects = await get_projects(db, skip=skip, limit=limit)
    return db_projects


@projects_router.post(
    "/",
    response_model=ProjectSchema,
    dependencies=[Depends(write_projects)],
    summary="Create new project",
    description="Needed roles: create_project_all",
)
async def rest_create_project(
    project: ProjectCreateSchema,
    db: AsyncSession = Depends(get_db),
    ext: ONSExtension = Depends(get_extension),
    user: UserModel = Depends(current_active_user),
):
    project_json = jsonable_encoder(project)
    db_project = await get_organization_project_by_title(
        db, organization_id=project.organization_id, project_title=project.title
    )
    if db_project:
        raise HTTPException(
            status_code=400, detail="Project already registered for organization"
        )

    db_project = await create_project(db, project=project_json)
    return db_project


@projects_router.get(
    "/{project_id}",
    response_model=ProjectSchema,
    dependencies=[Depends(read_projects)],
    summary="Get single project",
    description="Needed roles: read_project_all",
)
async def rest_read_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    ext: ONSExtension = Depends(get_extension),
    user: UserModel = Depends(current_active_user),
):
    db_project = await get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@projects_router.put(
    "/{project_id}",
    response_model=ProjectSchema,
    dependencies=[Depends(write_projects)],
    summary="Update single project",
    description="Needed roles: change_project_all",
)
async def rest_update_project(
    project_id: int,
    project: ProjectChangeSchema,
    db: AsyncSession = Depends(get_db),
    ext: ONSExtension = Depends(get_extension),
    user: UserModel = Depends(current_active_user),
):
    project_json = jsonable_encoder(project)
    db_project = await get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db_project = await update_project(
        ext, db, project_id=project_id, project=project_json
    )
    return db_project


@projects_router.delete(
    "/{project_id}",
    response_model=ProjectSchema,
    dependencies=[Depends(delete_projects)],
    summary="Delete single project",
    description="Needed roles: delete_project_all",
)
async def rest_delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    ext: ONSExtension = Depends(get_extension),
    user: UserModel = Depends(current_active_user),
):
    """Deletes a selected organizations by its ID"""
    try:
        db_project = await delete_project(ext, db, project_id=project_id)
    except OnsProjectNotFound as e:
        raise HTTPException(status_code=404, detail=e.msg)

    return db_project
