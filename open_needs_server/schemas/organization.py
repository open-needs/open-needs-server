from pydantic import BaseModel
from .project import Project


class OrganizationBase(BaseModel):
    title: str


class OrganizationCreate(OrganizationBase):
    pass


class Organization(OrganizationBase):
    id: int
    projects: list[Project] = []

    class Config:
        orm_mode = True
