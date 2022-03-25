from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from .models import OrganizationModel
from .schemas import OrganizationCreateSchema


async def get_organization(db: AsyncSession, organization_id: int):
    result = await db.execute(select(OrganizationModel).filter(OrganizationModel.id == organization_id))
    return result.scalars().first()


async def get_organization_by_title(db: AsyncSession, organization_title: int):
    result = await db.execute(select(OrganizationModel).filter(OrganizationModel.title == organization_title))
    return result.scalars().first()


async def get_organizations(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(OrganizationModel).offset(skip).limit(limit))
    return result.scalars().all()


async def create_organization(db: AsyncSession, organization: OrganizationCreateSchema):
    cursor = await db.execute(insert(OrganizationModel), organization)
    await db.commit()
    organization_id = cursor.inserted_primary_key[0]
    return {**organization, "id": organization_id}
