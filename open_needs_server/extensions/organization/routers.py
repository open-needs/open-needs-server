from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from open_needs_server.dependencies import get_db

from .schemas import OrganizationSchema, OrganizationCreateSchema
from .api import get_organization_by_title, create_organization, get_organization, get_organizations


organizations_router = APIRouter(
    prefix="/api/organizations",
    tags=["organizations"],
    dependencies=[],
    responses={"404": {"description": "Not found"}}
)


@organizations_router.post("/", response_model=OrganizationSchema)
async def rest_create_organization(organization: OrganizationCreateSchema, db: AsyncSession = Depends(get_db)):
    organization_json = jsonable_encoder(organization)
    db_organization = await get_organization_by_title(db, organization_title=organization.title)
    if db_organization:
        raise HTTPException(status_code=400, detail="organization already registered")

    db_organization = await create_organization(db, organization=organization_json)
    return db_organization


@organizations_router.get("/", response_model=list[OrganizationSchema])
async def rest_read_organizations(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    db_organizations = await get_organizations(db, skip=skip, limit=limit)
    return db_organizations


@organizations_router.get("/{organization_id}", response_model=OrganizationSchema)
async def rest_read_organization(organization_id: int, db: AsyncSession = Depends(get_db)):
    db_organization = await get_organization(db, organization_id=organization_id)
    if db_organization is None:
        raise HTTPException(status_code=404, detail="organization not found")
    return db_organization
