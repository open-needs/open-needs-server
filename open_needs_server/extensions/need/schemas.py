from pydantic import BaseModel
from typing import Dict, Union, Optional


class NeedBaseSchema(BaseModel):
    title: str
    description: str | None
    project_id: int
    meta: Dict[str, Union[float, str]] | None


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


class NeedUpdateSchema(NeedBaseSchema):
    title: Optional[str]
    description: Optional[str]
    project_id: Optional[int] | None
    meta: Optional[Dict[str, Union[float, str]]]


class NeedReturnSchema(NeedBaseSchema):
    id: int

    class Config:
        orm_mode = True

