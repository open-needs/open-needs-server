from pydantic import BaseModel
from typing import Dict, Union, Optional


class NeedBase(BaseModel):
    title: str
    description: str | None = None
    project_id: int
    meta: Dict[str, Union[float, str]] | None = None


class NeedFilter(NeedBase):
    title: Optional[str]
    description: Optional[str] | None = None
    project_id: Optional[int]
    meta: Dict[str, Union[float, str]] | None = None


class NeedCreate(NeedBase):
    title: str
    description: str | None = None
    project_id: int
    meta: Dict[str, Union[float, str]] | None = None


class Need(NeedBase):
    id: int

    class Config:
        orm_mode = True

