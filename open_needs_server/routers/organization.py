from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from open_needs_server import api, schemas
from open_needs_server.dependencies import get_db


organizations = APIRouter(
    prefix="/api/organizations",
    tags=["organizations"],
    dependencies=[],
    responses={"404": {"description": "Not found"}}
)


@organizations.post("/", response_model=schemas.Organization)
def create_organization(organization: schemas.OrganizationCreate, db: Session = Depends(get_db)):
    db_organization = api.get_organization_by_title(db, organization_title=organization.title)
    if db_organization:
        raise HTTPException(status_code=400, detail="organization already registerd")

    db_organization = api.create_organization(db, organization=organization)
    return db_organization


@organizations.get("/", response_model=list[schemas.Organization])
def read_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_organizations = api.get_organizations(db, skip=skip, limit=limit)
    return db_organizations


@organizations.get("/{organization_id}", response_model=schemas.Organization)
def read_organization(organization_id: int, db: Session = Depends(get_db)):
    db_organization = api.get_organization(db, organization_id=organization_id)
    if db_organization is None:
        raise HTTPException(status_code=404, detail="organization not found")
    return db_organization


