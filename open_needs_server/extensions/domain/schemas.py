from pydantic import BaseModel


class DomainBaseSchema(BaseModel):
    title: str
    description: str
    jsonschema: dict
    project_id: int


class DomainCreateSchema(DomainBaseSchema):
    pass


class DomainChangeSchema(DomainBaseSchema):
    title: str | None
    description: str | None
    project_id: int | None


class DomainSchema(DomainBaseSchema):
    id: int

    class Config:
        orm_mode = True
