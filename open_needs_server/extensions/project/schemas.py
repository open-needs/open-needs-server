from pydantic import BaseModel
from open_needs_server.extensions.need.schemas import NeedSchema


class ProjectBaseSchema(BaseModel):
    title: str
    organization_id: int


class ProjectCreateSchema(ProjectBaseSchema):
    pass


class ProjectSchema(ProjectBaseSchema):
    id: int
    needs: list[NeedSchema] = []

    class Config:
        orm_mode = True
