from pydantic import BaseModel
from open_needs_server.extensions.need.schemas import NeedReturnSchema
from open_needs_server.extensions.domain.schemas import DomainReturnSchema


class ProjectBaseSchema(BaseModel):
    title: str


class ProjectCreateSchema(ProjectBaseSchema):
    organization_id: int
    domains: list[int] = []


class ProjectChangeSchema(ProjectBaseSchema):
    title: str | None
    organization_id: int | None
    domains: list[int] = []


class ProjectSchema(ProjectBaseSchema):
    id: int
    needs: list[NeedReturnSchema] = []
    domains: list[DomainReturnSchema | None] = []

    class Config:
        orm_mode = True
