from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from open_needs_server.extensions.base import ONSExtension
from open_needs_server.extensions.user_security.schemas import UserDBSchema
from open_needs_server.extensions.user_security.dependencies import current_active_user, RoleChecker

from .schemas import DomainSchema, DomainCreateSchema, DomainChangeSchema
from .api import *

from open_needs_server.dependencies import get_db

domains_router = APIRouter(
    prefix="/api/domains",
    tags=["domains"],
    dependencies=[],
    responses={"404": {"description": "Not found"}}
)


async def get_extension(request: Request):
    return request.app.ons_extensions['ProjectExtension']


read_domains = RoleChecker(['view_domains_all'])
write_domains = RoleChecker(['change_domains_all'])
delete_domains = RoleChecker(['delete_domains_all'])


@domains_router.get("/",
                    response_model=list[DomainSchema],
                    dependencies=[Depends(read_domains)],
                    summary="List all domains",
                    description="Needed roles: view_domain_all")
async def rest_read_domains(skip: int = 0, limit: int = 100,
                            db: AsyncSession = Depends(get_db),
                            ext: ONSExtension = Depends(get_extension),
                            user: UserDBSchema = Depends(current_active_user)
                            ):
    db_domains = await get_domains(db, skip=skip, limit=limit)
    return db_domains


@domains_router.post("/",
                     response_model=DomainSchema,
                     dependencies=[Depends(write_domains)],
                     summary="Create new domain",
                     description="Needed roles: create_domain_all"
                     )
async def rest_create_domain(domain: DomainCreateSchema,
                             db: AsyncSession = Depends(get_db),
                             ext: ONSExtension = Depends(get_extension),
                             user: UserDBSchema = Depends(current_active_user)
                             ):
    domain_json = jsonable_encoder(domain)
    db_domain = await get_organization_domain_by_title(db, organization_id=domain.organization_id,
                                                       domain_title=domain.title)
    if db_domain:
        raise HTTPException(status_code=400, detail="Project already registered for organization")

    db_domain = await create_domain(db, domain=domain_json)
    return db_domain


@domains_router.get("/{domain_id}",
                    response_model=DomainSchema,
                    dependencies=[Depends(read_domains)],
                    summary="Get single domain",
                    description="Needed roles: read_domain_all"
                    )
async def rest_read_domain(domain_id: int,
                           db: AsyncSession = Depends(get_db),
                           ext: ONSExtension = Depends(get_extension),
                           user: UserDBSchema = Depends(current_active_user)
                           ):
    db_domain = await get_domain(db, domain_id=domain_id)
    if db_domain is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_domain


@domains_router.put("/{domain_id}",
                    response_model=DomainSchema,
                    dependencies=[Depends(write_domains)],
                    summary="Update single domain",
                    description="Needed roles: change_domain_all"
                    )
async def rest_update_domain(domain_id: int,
                             domain: DomainChangeSchema,
                             db: AsyncSession = Depends(get_db),
                             ext: ONSExtension = Depends(get_extension),
                             user: UserDBSchema = Depends(current_active_user)
                             ):
    domain_json = jsonable_encoder(domain)
    db_domain = await get_domain(db, domain_id=domain_id)
    if db_domain is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db_domain = await update_domain(ext, db,
                                    domain_id=domain_id,
                                    domain=domain_json)
    return db_domain


@domains_router.delete("/{domain_id}",
                       response_model=DomainSchema,
                       dependencies=[Depends(delete_domains)],
                       summary="Delete single domain",
                       description="Needed roles: delete_domain_all"
                       )
async def rest_delete_domain(domain_id: int,
                             db: AsyncSession = Depends(get_db),
                             ext: ONSExtension = Depends(get_extension),
                             user: UserDBSchema = Depends(current_active_user)
                             ):
    """Deletes a selected organizations by its ID"""
    try:
        db_domain = await delete_domain(ext, db, domain_id=domain_id)
    except OnsProjectNotFound as e:
        raise HTTPException(status_code=404, detail=e.msg)

    return db_domain
