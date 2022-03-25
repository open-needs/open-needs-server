from pydantic import BaseModel
from typing import Dict, Union, Optional


class NeedBaseSchema(BaseModel):
    title: str
    description: str | None = None
    project_id: int
    meta: Dict[str, Union[float, str]] | None = None


class NeedFilterSchema(NeedBaseSchema):
    title: Optional[str]
    description: Optional[str] | None = None
    project_id: Optional[int]
    meta: Dict[str, Union[float, str]] | None = None


class NeedCreateSchema(NeedBaseSchema):
    title: str
    description: str | None = None
    project_id: int
    meta: Dict[str, Union[float, str]] | None = None


class NeedSchema(NeedBaseSchema):
    id: int

    class Config:
        orm_mode = True

