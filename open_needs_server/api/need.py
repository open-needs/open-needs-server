from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from open_needs_server import models
from open_needs_server import schemas


async def get_need(db: AsyncSession, need_id: int):
    result = await db.execute(select(models.Need).filter(models.Need.id == need_id))
    return result.scalars().first()


async def get_needs(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Need).offset(skip).limit(limit))
    return result.scalars().all()


async def create_need(db: AsyncSession, need: schemas.Need):
    project_id = need['project_id']
    result = await db.execute(select(models.Project).filter(models.Project.id == project_id))
    db_project = result.scalars().first()

    if not db_project:
        raise OnApiNeedException(f"Referenced project_id {project_id} not found")

    cursor = await db.execute(insert(models.Need), need)
    await db.commit()
    need_id = cursor.inserted_primary_key[0]
    return {**need, "id": need_id}


class OnApiNeedException(BaseException):
    pass
