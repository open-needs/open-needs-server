from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from open_needs_server.dependencies import get_db
from open_needs_server.extensions.base import ONSExtension
from open_needs_server.extensions.user_security.dependecies import current_active_user, RoleChecker
from open_needs_server.extensions.user_security.schemas import UserDBSchema

from .schemas import OrganizationReturnSchema, OrganizationCreateSchema, OrganizationShortSchema
from .api import OnsOrganizationNotFound, get_organization_by_title, create_organization, get_organization, \
    get_organizations, update_organization, delete_organization

organizations_router = APIRouter(
    prefix="/api/organizations",
    tags=["organizations"],
    dependencies=[],
    responses={"404": {"description": "Not found"}}
)


async def get_extension(request: Request):
    return request.app.ons_extensions['OrganizationExtension']

read_organizations = RoleChecker(['view_org_all'])
change_organizations = RoleChecker(['change_org_all'])
delete_organizations = RoleChecker(['delete_org_all'])


@organizations_router.get("/",
                          response_model=list[OrganizationShortSchema],
                          summary='List all organizations',
                          dependencies=[Depends(read_organizations)],
                          description='Needed roles: view_org_all')
async def rest_read_organizations(skip: int = 0, limit: int = 100,
                                  db: AsyncSession = Depends(get_db),
                                  ext: ONSExtension = Depends(get_extension),
                                  user: UserDBSchema = Depends(current_active_user)):

    ext.print(f'user: {user.email} - {user.is_active}')
    db_organizations = await get_organizations(ext, db, skip=skip, limit=limit)
    return db_organizations


@organizations_router.post("/",
                           response_model=OrganizationReturnSchema,
                           summary='Create a new organization',
                           dependencies=[Depends(change_organizations)])
async def rest_create_organization(organization: OrganizationCreateSchema, db: AsyncSession = Depends(get_db),
                                   ext: ONSExtension = Depends(get_extension)):
    organization_json = jsonable_encoder(organization)
    db_organization = await get_organization_by_title(ext, db, organization_title=organization.title)
    if db_organization:
        raise HTTPException(status_code=400, detail="organization already registered")

    db_organization = await create_organization(ext, db, organization=organization_json)
    return db_organization


@organizations_router.get("/{organization_id}",
                          response_model=OrganizationReturnSchema,
                          summary='Retrieve a organisation',
                          dependencies=[Depends(read_organizations)])
async def rest_read_organization(organization_id: int, db: AsyncSession = Depends(get_db),
                                 ext: ONSExtension = Depends(get_extension)):
    db_organization = await get_organization(ext, db, organization_id=organization_id)
    if db_organization is None:
        raise HTTPException(status_code=404, detail="organization not found")
    return db_organization


@organizations_router.put("/{organization_id}",
                          response_model=OrganizationReturnSchema,
                          summary='Update a organization',
                          dependencies=[Depends(change_organizations)])
async def rest_update_organization(organization: OrganizationCreateSchema, organization_id: int,
                                   db: AsyncSession = Depends(get_db),
                                   ext: ONSExtension = Depends(get_extension)):
    organization_json = jsonable_encoder(organization)
    db_organization = await get_organization(ext, db, organization_id=organization_id)
    if not db_organization:
        raise HTTPException(status_code=404, detail="organization not found")

    db_organization = await update_organization(ext, db,
                                                organization_id=organization_id,
                                                organization=organization_json)
    return db_organization


@organizations_router.delete("/{organization_id}",
                             response_model=OrganizationReturnSchema,
                             summary='Delete organization',
                             dependencies=[Depends(delete_organizations)])
async def rest_delete_organization(organization_id: int, db: AsyncSession = Depends(get_db),
                                   ext: ONSExtension = Depends(get_extension)):
    """Deletes a selected organizations by its ID"""
    try:
        db_organization = await delete_organization(ext, db, organization_id=organization_id)
    except OnsOrganizationNotFound as e:
        raise HTTPException(status_code=404, detail=e.msg)

    return db_organization
