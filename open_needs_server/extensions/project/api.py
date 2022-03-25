from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from .models import ProjectModel
from .schemas import ProjectSchema


async def get_project(db: AsyncSession, project_id: int):
    result = await db.execute(select(ProjectModel).filter(ProjectModel.id == project_id))
    return result.scalars().first()


async def get_project_by_title(db: AsyncSession, project_title: int):
    result = await db.execute(select(ProjectModel).filter(ProjectModel.title == project_title))
    return result.scalars().first()


async def get_projects(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(ProjectModel).offset(skip).limit(limit))
    return result.scalars().all()


async def create_project(db: AsyncSession, project: ProjectSchema):
    cursor = await db.execute(insert(ProjectModel), project)
    await db.commit()
    project_id = cursor.inserted_primary_key[0]
    return {**project, "id": project_id}

# Orga specific

async def get_organization_project_by_title(db: AsyncSession, organization_id: int, project_title: int):
    result = await db.execute(select(ProjectModel).filter(ProjectModel.title == project_title,
                                                          ProjectModel.organization_id == organization_id))
    return result.scalars().first()
