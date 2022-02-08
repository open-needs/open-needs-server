from pydantic import BaseModel
from .need import Need


class ProjectBase(BaseModel):
    title: str


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    organization_id: int
    needs: list[Need] = []

    class Config:
        orm_mode = True
