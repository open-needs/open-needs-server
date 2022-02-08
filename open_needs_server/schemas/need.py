from pydantic import BaseModel


class NeedBase(BaseModel):
    title: str
    description: str | None = None


class NeedCreate(NeedBase):
    pass


class Need(NeedBase):
    id: int
    project_id: int

    class Config:
        orm_mode = True
