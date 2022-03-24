from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from open_needs_server import api, schemas
from open_needs_server.dependencies import get_db


organizations = APIRouter(
    prefix="/api/organizations",
    tags=["organizations"],
    dependencies=[],
    responses={"404": {"description": "Not found"}}
)


@organizations.post("/", response_model=schemas.Organization)
async def create_organization(organization: schemas.OrganizationCreate, db: AsyncSession = Depends(get_db)):
    organization_json = jsonable_encoder(organization)
    db_organization = await api.get_organization_by_title(db, organization_title=organization.title)
    if db_organization:
        raise HTTPException(status_code=400, detail="organization already registerd")

    db_organization = await api.create_organization(db, organization=organization_json)
    return db_organization


@organizations.get("/", response_model=list[schemas.Organization])
async def read_organizations(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    db_organizations = await api.get_organizations(db, skip=skip, limit=limit)
    return db_organizations


@organizations.get("/{organization_id}", response_model=schemas.Organization)
async def read_organization(organization_id: int, db: AsyncSession = Depends(get_db)):
    db_organization = await api.get_organization(db, organization_id=organization_id)
    if db_organization is None:
        raise HTTPException(status_code=404, detail="organization not found")
    return db_organization


