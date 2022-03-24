from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from open_needs_server import models
from open_needs_server import schemas


async def get_organization(db: AsyncSession, organization_id: int):
    result = await db.execute(select(models.Organization).filter(models.Organization.id == organization_id))
    return result.scalars().first()


async def get_organization_by_title(db: AsyncSession, organization_title: int):
    result = await db.execute(select(models.Organization).filter(models.Organization.title == organization_title))
    return result.scalars().first()


async def get_organizations(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Organization).offset(skip).limit(limit))
    return result.scalars().all()


async def create_organization(db: AsyncSession, organization: schemas.organization):
    cursor = await db.execute(insert(models.Organization), organization)
    await db.commit()
    organization_id = cursor.inserted_primary_key[0]
    return {**organization, "id": organization_id}
