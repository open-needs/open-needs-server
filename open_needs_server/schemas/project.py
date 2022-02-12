from pydantic import BaseModel
from .need import Need


class ProjectBase(BaseModel):
    title: str
    organization_id: int


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    needs: list[Need] = []

    class Config:
        orm_mode = True
