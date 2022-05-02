from pydantic import BaseModel
from open_needs_server.extensions.need.schemas import NeedReturnSchema


class ProjectBaseSchema(BaseModel):
    title: str


class ProjectCreateSchema(ProjectBaseSchema):
    organization_id: int


class ProjectChangeSchema(ProjectBaseSchema):
    title: str | None
    organization_id: int | None


class ProjectSchema(ProjectBaseSchema):
    id: int
    needs: list[NeedReturnSchema] = []

    class Config:
        orm_mode = True
