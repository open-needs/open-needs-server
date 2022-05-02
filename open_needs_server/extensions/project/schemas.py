from pydantic import BaseModel
from open_needs_server.extensions.need.schemas import NeedSchema


class ProjectBaseSchema(BaseModel):
    title: str


class ProjectCreateSchema(ProjectBaseSchema):
    organization_id: int


class ProjectChangeSchema(ProjectBaseSchema):
    title: str | None
    organization_id: int | None


class ProjectSchema(ProjectBaseSchema):
    id: int
    needs: list[NeedSchema] = []

    class Config:
        orm_mode = True
