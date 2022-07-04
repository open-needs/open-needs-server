from pydantic import BaseModel


class DomainBaseSchema(BaseModel):
    title: str
    description: str
    jsonschema: dict


class DomainCreateSchema(DomainBaseSchema):
    pass


class DomainChangeSchema(DomainBaseSchema):
    title: str | None
    description: str | None


class DomainSchema(DomainBaseSchema):
    id: int

    class Config:
        orm_mode = True


class DomainReturnSchema(DomainBaseSchema):
    id: int

    class Config:
        orm_mode = True
