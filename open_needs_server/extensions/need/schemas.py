from pydantic import BaseModel
from typing import Dict, Union, Optional


class NeedBaseSchema(BaseModel):
    key: str
    type: str
    title: str
    description: str | None
    format: str | None
    project_id: int
    options: Dict[str, Union[float, str]] | None
    references: Dict[str, list[str]] | None


class NeedFilterSchema(NeedBaseSchema):
    title: Optional[str]
    description: Optional[str] | None = None
    project_id: Optional[int]
    options: Dict[str, Union[float, str]] | None = None
    references: Dict[str, list[str]] | None = None


class NeedCreateSchema(NeedBaseSchema):
    title: str
    description: str | None = None
    project_id: int
    options: Dict[str, Union[float, str]] | None = {}
    references: Dict[str, list[str]] | None = {}


class NeedUpdateSchema(NeedBaseSchema):
    title: Optional[str]
    description: Optional[str]
    project_id: Optional[int] | None
    options: Optional[Dict[str, Union[float, str]]]
    references: Optional[Dict[str, list[str]]]


class NeedReturnSchema(NeedBaseSchema):
    options: Dict[str, Union[float, str]]
    references: Dict[str, list[str]]

    class Config:
        orm_mode = True

